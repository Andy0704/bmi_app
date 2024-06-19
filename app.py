from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import base64
from io import BytesIO

app = Flask(__name__)
# 获取环境变量中的 DATABASE_URL，并确保它是以 'postgresql://' 开头
#DATABASE_URL = os.getenv('postgres://data_record_user:XXFgzgwnpUJLUrU6SRmXLq5w08sB0TJT@dpg-cppa8huehbks73bueno0-a/data_record')
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 配置数据库连接字符串
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database model
class HealthData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    hemoglobin = db.Column(db.Float, nullable=False)
    rbc = db.Column(db.Float, nullable=False)
    wbc = db.Column(db.Float, nullable=False)
    hct = db.Column(db.Float, nullable=False)
    platelets = db.Column(db.Float, nullable=False)
    mcv = db.Column(db.Float, nullable=False)
    mch = db.Column(db.Float, nullable=False)
    mchc = db.Column(db.Float, nullable=False)
    ast = db.Column(db.Float, nullable=False)
    alt = db.Column(db.Float, nullable=False)
    bun = db.Column(db.Float, nullable=False)
    creatinine = db.Column(db.Float, nullable=False)
    cholesterol = db.Column(db.Float, nullable=False)
    triglycerides = db.Column(db.Float, nullable=False)
    glucose = db.Column(db.Float, nullable=False)
    neutrophils = db.Column(db.Float, nullable=False)
    lymphocytes = db.Column(db.Float, nullable=False)
    monocytes = db.Column(db.Float, nullable=False)
    eosinophils = db.Column(db.Float, nullable=False)
    basophils = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)

# Create tables based on the defined model
#db.create_all()

# Create tables within an application context
with app.app_context():
    db.create_all()

#if request.method == 'POST':
        #height = float(request.form['height'])
        #weight = float(request.form['weight'])
        #bmi = weight / (height / 100) ** 2  # 计算 BMI
        #record = BMIRecord(height=height, weight=weight, bmi=bmi)
        #db.session.add(record)
        #db.session.commit()
        #return redirect(url_for('index'))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/save', methods=['POST'])
def save_data():
    data = request.json
    new_data = HealthData(
        gender=data['gender'], height=data['height'], weight=data['weight'],
        hemoglobin=data['hemoglobin'], rbc=data['rbc'], wbc=data['wbc'],
        hct=data['hct'], platelets=data['platelets'], mcv=data['mcv'],
        mch=data['mch'], mchc=data['mchc'], ast=data['ast'], alt=data['alt'],
        bun=data['bun'], creatinine=data['creatinine'], cholesterol=data['cholesterol'],
        triglycerides=data['triglycerides'], glucose=data['glucose'],
        neutrophils=data['neutrophils'], lymphocytes=data['lymphocytes'],
        monocytes=data['monocytes'], eosinophils=data['eosinophils'],
        basophils=data['basophils'], bmi=data['bmi']
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({"message": "Data saved successfully"}), 201

@app.route('/plot')
def plot():
    # Read data from database
    df = pd.read_sql_table('health_data', con=db.engine)

    # Generate overlay histogram for all columns except 'id' and 'gender'
    fig_histograms = go.Figure()
    for col in df.columns[2:]:  # Skip 'id' and 'gender'
        fig_histograms.add_trace(go.Histogram(x=df[col], name=col, opacity=0.5))

    fig_histograms.update_layout(
        title_text='Health Data Histograms',
        barmode='overlay',
        xaxis_title='Value',
        yaxis_title='Count'
    )

    # Convert figure to HTML string
    html_content = fig_histograms.to_html(full_html=False)

    return html_content


if __name__ == '__main__':
    app.run(debug=True)
