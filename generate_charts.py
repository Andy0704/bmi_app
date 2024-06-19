import psycopg2
import pandas as pd
import plotly.express as px
import os

# 配置数据库连接
conn = psycopg2.connect(
    host=os.getenv("dpg-cppa8huehbks73bueno0-a"),
    database=os.getenv("data_record"),
    user=os.getenv("data_record_user"),
    password=os.getenv("XXFgzgwnpUJLUrU6SRmXLq5w08sB0TJT"),
    port=os.getenv("5432")
)

# 读取数据
df = pd.read_sql_query('SELECT * FROM health_data', conn)

# 生成图表
fig = px.histogram(df, x='bmi', title='BMI Distribution')
fig.show()

fig2 = px.scatter(df, x='height', y='weight', color='gender', title='Height vs Weight')
fig2.show()
