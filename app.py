from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
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
    return jsonify({"message": "Data saved successfully"}), 200

@app.route('/plot')
def plot():
    # Read data from database
    df = pd.read_sql_table('health_data', con=db.engine)

    # Generate 3D scatter plot for height, weight, and BMI
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=df['height'],
        y=df['weight'],
        z=df['bmi'],
        mode='markers',
        marker=dict(size=5)
    )])
    fig_3d.update_layout(scene=dict(
        xaxis_title='Height',
        yaxis_title='Weight',
        zaxis_title='BMI'
    ))

    # Generate histograms for other data fields
    hist_figs = []
    for col in df.columns.difference(['id', 'gender', 'height', 'weight', 'bmi']):
        fig = px.histogram(df, x=col, title=f'{col.capitalize()} Distribution')
        hist_figs.append(fig)

    # Convert figures to HTML
    fig_3d_html = fig_3d.to_html(full_html=False)
    hist_figs_html = [fig.to_html(full_html=False) for fig in hist_figs]

    # Combine all HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Plot Results</title>
    </head>
    <body>
        <div>
            <h1>3D Scatter Plot (Height, Weight, BMI)</h1>
            <div>{fig_3d_html}</div>
        </div>
    """

    for i, fig_html in enumerate(hist_figs_html):
        html_content += f"""
        <div>
            <h1>{df.columns.difference(['id', 'gender', 'height', 'weight', 'bmi'])[i].capitalize()} Distribution</h1>
            <div>{fig_html}</div>
        </div>
        """

    html_content += """
    </body>
    </html>
    """

    return html_content

if __name__ == '__main__':
    app.run(debug=True)
