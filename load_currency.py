import requests                           
import pandas as pd                           
from dotenv import load_dotenv              
import os                                     
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import text



API_url="https://www.cbr-xml-daily.ru/daily_json.js"

response = requests.get(API_url)
response.raise_for_status()
data= response.json()

список = []
rate_date = pd.to_datetime(data['Date']).date()
for key, словарь in data['Valute'].items():
    currency_code = словарь['CharCode']
    nominal = словарь['Nominal']
    rate = словарь['Value']
    список.append([rate_date, currency_code, nominal, rate])


таблица =  pd.DataFrame(список, columns=['rate_date', 'currency_code', 'nominal', 'rate'])

print(rate_date)
print(len(таблица))



load_dotenv() 
neon_password = os.getenv("neon_password")
neon_host=os.getenv("neon_host")

url_db=URL.create(
    drivername="postgresql+psycopg",
    username="neondb_owner",
    password=neon_password,
    host=neon_host,
    port=5432,
    database="neondb",
    query={"sslmode":"require"})

engine=create_engine(url_db)




record = таблица.to_dict(orient="records")

with engine.begin() as connection:
    result = connection.execute(text("""
    INSERT INTO currency_rates(rate_date, currency_code, nominal, rate)
    VALUES(:rate_date, :currency_code, :nominal, :rate)
    ON CONFLICT (rate_date, currency_code)
    DO NOTHING
    """), record)

    added_rows = result.rowcount

print(f"Добавлено строк: {added_rows}")
    



    







