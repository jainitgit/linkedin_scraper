import pandas as pd
from pymongo import MongoClient

# 1. Load your CSV file
csv_file = 'C:/Users/Jainit/Desktop/internship/scraper (mongo db)/jobs_bhubaneswar.csv'
df = pd.read_csv(csv_file)

# 2. Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://mongo:mongo123@cluster0.veyicts.mongodb.net/")

# 3. Choose database and collection
db = client["mongodb"]
collection = db["scraperdb"]

# 4. Convert DataFrame to dictionary and insert
data = df.to_dict(orient='records')
collection.insert_many(data)

print("Data inserted successfully.")
