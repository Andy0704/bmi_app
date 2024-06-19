from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# 配置数据库连接
conn = psycopg2.connect(
    host="your_host",
    database="your_database",
    user="your_user",
    password="your_password",
    port="your_port"
)

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

if __name__ == '__main__':
    app.run(debug=True)
