import psycopg as pc
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pandas as pd
import streamlit as st
import numpy as np

load_dotenv()
neon_password=os.getenv("neon_password")
neon_host=os.getenv("neon_host")

url=URL.create(
    drivername="postgresql+psycopg",
    username="neondb_owner",
    password=neon_password,
    host=neon_host,
    port=5432,
    database="neondb",
    query={"sslmode":"require"}
)
engine=create_engine(url)


df=pd.read_sql_query("SELECT rate_date, currency_code, nominal, rate FROM currency_rates where currency_code in ('USD', 'EUR', 'CNY')order by rate_date asc", engine)

df['rate_date'] = pd.to_datetime(df['rate_date'])


new_df = df.pivot(
    index = 'rate_date',
    columns='currency_code',
    values= 'rate'
).reset_index()

st.title("Курсы валют ЦБ РФ")
st.dataframe(new_df)
st.subheader("Динамика курсов валют")
rate = st.selectbox(
    "Выберите валюту",
    new_df.columns[1:]
)

st.line_chart(
    new_df,
    x='rate_date',
    y=rate
)
