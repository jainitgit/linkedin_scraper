import sqlite3
import pandas as pd 

df = pd.read_csv('C:/Users/Jainit/Desktop/internship/scraper/jobs_bhubaneswar2.csv')

df.columns = df.columns.str.strip()

connection = sqlite3.connect('demo1.db')

df.to_sql ('jobs_bhubaneswar_1', connection, if_exists='replace')
