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


# Create tables within an application context
with app.app_context():
    db.create_all()

def calculate_bmi(height, weight):
    height_meters = height / 100
    bmi = weight / (height_meters ** 2)
    return bmi

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/save', methods=['POST'])
def save_data():
    data = request.json
    bmi = calculate_bmi(data['height'], data['weight'])
    new_data = HealthData(
        gender=data['gender'], height=data['height'], weight=data['weight'],
        hemoglobin=data['hemoglobin'], rbc=data['rbc'], wbc=data['wbc'],
        hct=data['hct'], platelets=data['platelets'], mcv=data['mcv'],
        mch=data['mch'], mchc=data['mchc'], ast=data['ast'], alt=data['alt'],
        bun=data['bun'], creatinine=data['creatinine'], cholesterol=data['cholesterol'],
        triglycerides=data['triglycerides'], glucose=data['glucose'],
        neutrophils=data['neutrophils'], lymphocytes=data['lymphocytes'],
        monocytes=data['monocytes'], eosinophils=data['eosinophils'],
        basophils=data['basophils'], bmi=bmi
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({"message": "Data saved successfully"}), 201

@app.route('/plot')
def plot():
    # Read data from database
    df = pd.read_sql_table('health_data', con=db.engine)

    # Exclude 'gender' column from histograms
    fig_histograms = make_subplots(rows=3, cols=3, subplot_titles=("RBC", "WBC", "HCT", "Platelets", "MCV", "MCH", "MCHC", "AST", "ALT"))

    # Group columns by similar numerical values and create histograms
    columns_to_plot = ['rbc', 'wbc', 'hct', 'platelets', 'mcv', 'mch', 'mchc', 'ast', 'alt']
    for i, col in enumerate(columns_to_plot):
        row = i // 3 + 1
        col = i % 3 + 1
        fig_histograms.add_trace(go.Histogram(x=df[col], name=col.capitalize()), row=row, col=col)

    fig_histograms.update_layout(
        title_text='Health Data Histograms',
        barmode='overlay',
        xaxis_title='Value',
        yaxis_title='Count'
    )

    # Create 3D scatter plot
    fig_3d = go.Figure()
    fig_3d.add_trace(go.Scatter3d(
        x=df['height'],
        y=df['weight'],
        z=df['bmi'],
        mode='markers',
        marker=dict(
            size=5,
            color=df['bmi'],
            colorscale='Viridis',
            opacity=0.8
        ),
        text=df['gender'],
        hoverinfo='text'
    ))

    fig_3d.update_layout(
        title_text="BMI, Height, and Weight Analysis",
        scene=dict(
            xaxis_title='Height (cm)',
            yaxis_title='Weight (kg)',
            zaxis_title='BMI'
        )
    )

    # Convert Plotly figures to div strings
    div_histograms = fig_histograms.to_html(full_html=False)
    div_3d_plot = fig_3d.to_html(full_html=False)

    # Combine Plotly divs into a single HTML content
    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Health Data Analysis</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <div>
                <h1>Health Data Histograms</h1>
                {div_histograms}
            </div>
            <div>
                <h1>BMI, Height, and Weight Analysis</h1>
                {div_3d_plot}
            </div>
        </body>
        </html>
    """
    return html_content


if __name__ == '__main__':
    app.run(debug=True)
