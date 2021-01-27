from pymongo import MongoClient
import pandas as pd
import time
from bson.json_util import dumps
import json
myclient = MongoClient("mongodb://root:root@localhost:27017/")
mydb = myclient["test"]
collection = mydb["collection"]


def timconv(time, time1):
    return (time1-time)/1e9


time1 = time.time_ns()
print("Start Time: ", time1)

cursor = collection.find({})
print("Start Time: ")

# Converting cursor to the list
# of dictionaries
list_cur = list(cursor)
print("Start Time: ")

# Converting to the JSON
json_data = dumps(list_cur, indent=2)

print("Start Time: ")

# Writing data to file data.json
with open('data.json', 'w') as file:
    file.write(json_data)
print("Start Time: ")


# data = pd.read_csv("dataset.csv", header=0, dtype='unicode')
# records = data.to_dict('records')

time2 = time.time_ns()
print("Time After Load To Memory before insert:", time2)

# collection.insert_many(records)

time3 = time.time_ns()
print("Time After Insert:", time3)

print("Total time:", timconv(time1, time3))
