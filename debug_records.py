# debug_records.py
import pickle

with open("chatbot/rag/index/records.pkl", "rb") as f:
    records = pickle.load(f)

for record in records:
    print(record)