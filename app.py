from flask import Flask, request, jsonify, render_template
import psycopg2
import os

app = Flask(__name__)
# 配置数据库连接
conn = psycopg2.connect(
    host=os.getenv("dpg-cppa8huehbks73bueno0-a"),
    database=os.getenv("data_record"),
    user=os.getenv("data_record_user"),
    password=os.getenv("XXFgzgwnpUJLUrU6SRmXLq5w08sB0TJT"),
    port=os.getenv("5432")
)

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
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
            data['gender'], data['height'], data['weight'], data['hemoglobin'], data['rbc'],
            data['wbc'], data['hct'], data['platelets'], data['mcv'], data['mch'], data['mchc'],
            data['ast'], data['alt'], data['bun'], data['creatinine'], data['cholesterol'],
            data['triglycerides'], data['glucose'], data['neutrophils'], data['lymphocytes'],
            data['monocytes'], data['eosinophils'], data['basophils'], data['bmi']
        ))
        conn.commit()
    return jsonify({"message": "Data saved successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)

