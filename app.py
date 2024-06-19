from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
import base64
from io import BytesIO

app = Flask(__name__,, template_folder='/template')
# 获取环境变量中的 DATABASE_URL，并确保它是以 'postgresql://' 开头
DATABASE_URL = os.getenv('postgres://data_record_user:XXFgzgwnpUJLUrU6SRmXLq5w08sB0TJT@dpg-cppa8huehbks73bueno0-a/data_record')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 配置数据库连接字符串
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_data():
    data = request.json
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO health_data (
                gender, height, weight, hemoglobin, rbc, wbc, hct, platelets,
                mcv, mch, mchc, ast, alt, bun, creatinine, cholesterol, triglycerides,
                glucose, neutrophils, lymphocytes, monocytes, eosinophils, basophils, bmi
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['gender'], data['height'], data['weight'], data['hemoglobin'], data['rbc'],
            data['wbc'], data['hct'], data['platelets'], data['mcv'], data['mch'], data['mchc'],
            data['ast'], data['alt'], data['bun'], data['creatinine'], data['cholesterol'],
            data['triglycerides'], data['glucose'], data['neutrophils'], data['lymphocytes'],
            data['monocytes'], data['eosinophils'], data['basophils'], data['bmi']
        ))
        conn.commit()
    return jsonify({"message": "Data saved successfully"}), 200

@app.route('/plot')
def plot():
    # 读取数据
    df = pd.read_sql_query('SELECT * FROM health_data', conn)

    # 生成图表
    fig = px.histogram(df, x='bmi', title='BMI Distribution')
    fig2 = px.scatter(df, x='height', y='weight', color='gender', title='Height vs Weight')

    # 将图表转换为 HTML 内联图像
    def fig_to_html(fig):
        buffer = BytesIO()
        fig.write_html(buffer, full_html=False)
        html_bytes = buffer.getvalue()
        return html_bytes.decode('utf8')

    bmi_chart_html = fig_to_html(fig)
    height_weight_chart_html = fig_to_html(fig2)

    return render_template('plot.html', bmi_chart_html=bmi_chart_html, height_weight_chart_html=height_weight_chart_html)

if __name__ == '__main__':
    app.run(debug=True)
