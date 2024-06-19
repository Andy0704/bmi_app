import psycopg2
import pandas as pd
import plotly.express as px
import os

# 配置数据库连接
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    port=os.getenv("DB_PORT")
)

# 读取数据
df = pd.read_sql_query('SELECT * FROM health_data', conn)

# 生成图表
fig = px.histogram(df, x='bmi', title='BMI Distribution')
fig.show()

fig2 = px.scatter(df, x='height', y='weight', color='gender', title='Height vs Weight')
fig2.show()
