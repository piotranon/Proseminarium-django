from pymongo import MongoClient
import pandas as pd
import json
import time

myclient = MongoClient("mongodb://root:root@localhost:27017/")
mydb = myclient["test"]
collection = mydb["collection"]


def timconv(time, time1):
    return (time1-time)/1e9


time1 = time.time_ns()
print("Start Time: ", time1)

names = ["anzsic06", "Area", "year", "geo_count", "ec_count"]

data = pd.read_csv('dataset.csv')
payload = json.loads(data.to_json(orient='records'))

collection.insert_many(payload)

time3 = time.time_ns()
print("Time After Insert:", time3)

print("Total time:", timconv(time1, time3))
