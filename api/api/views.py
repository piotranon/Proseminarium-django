from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from bson.json_util import dumps
import pymongo
import pandas as pd
from csv import DictReader
import clickhouse_driver
import requests
import json
import time
import os
import paramiko
import asyncio


ip = "192.168.1.200"


def timconv(time, time1):
    return (time1-time)/1e9


def home(request):
    response = requests.get('http://freegeoip.net/json/')
    # geodata = response.json()
    return JsonResponse({"XD": "elo"}, safe=False)


def clickhouse(request, method):
    clic = ClickHouse()

    # if(clic.client)

    if(method == "xd"):
        return JsonResponse({"time": "xd"}, safe=False)

    if(method == "createDatabase"):
        return JsonResponse({"time": clic.tworzeniebazy(False)}, safe=False)

    if(method == "importDatabase"):
        return JsonResponse({"time": clic.importdanych(False)}, safe=False)
        # return JsonResponse({"time": os.getcwd()}, safe=False)

    if(method == "dropDatabase"):
        return JsonResponse({"time": clic.usuwaniebazy(False)}, safe=False)

    if(method == "records"):
        return JsonResponse({"records": clic.iloscdanych(False)[0], "time": clic.zapytanie5(False)}, safe=False)

    if(method == "test1"):
        return JsonResponse({"time": clic.zapytanie1(False)}, safe=False)
    if(method == "test2"):
        return JsonResponse({"time": clic.zapytanie2(False)}, safe=False)
    if(method == "test3"):
        return JsonResponse({"time": clic.zapytanie3(False)}, safe=False)
    if(method == "test4"):
        return JsonResponse({"time": clic.zapytanie4(False)}, safe=False)
    if(method == "test5"):
        return JsonResponse({"time": clic.zapytanie5(False)}, safe=False)
    if(method == "test6"):
        return JsonResponse({"time": clic.zapytanie6(False)}, safe=False)
    if(method == "test7"):
        return JsonResponse({"time": clic.zapytanie7(False)}, safe=False)

    print(request)
    # return JsonResponse({"data": json.loads(request)}, safe=False)
    return HttpResponse('XD : {}'.format(method))


def mongo(request, method):
    clic = MongoClientConnection()

    if(method == "xd"):
        return JsonResponse({"time": "xd"}, safe=False)

    if(method == "importDatabase"):
        return JsonResponse({"time": clic.importdanych()}, safe=False)
        # return JsonResponse({"time": os.getcwd()}, safe=False)

    if(method == "dropDatabase"):
        return JsonResponse({"time": clic.usuwaniebazy()}, safe=False)

    if(method == "records"):
        return JsonResponse({"records": clic.iloscdanych(), "time": clic.zapytanie5()}, safe=False)

    if(method == "test1"):
        return JsonResponse({"time": clic.zapytanie1()}, safe=False)
    if(method == "test2"):
        return JsonResponse({"time": clic.zapytanie2()}, safe=False)
    if(method == "test3"):
        return JsonResponse({"time": clic.zapytanie3()}, safe=False)
    if(method == "test4"):
        return JsonResponse({"time": clic.zapytanie4()}, safe=False)
    if(method == "test5"):
        return JsonResponse({"time": clic.zapytanie5()}, safe=False)
    if(method == "test6"):
        return JsonResponse({"time": clic.zapytanie6()}, safe=False)
    if(method == "test7"):
        return JsonResponse({"time": clic.zapytanie7()}, safe=False)

    return HttpResponse('XD : {}'.format(method))


def iter_csv(filename):
    converters = {
        'year': int,
        'geo_count': int,
        'ec_count': int,
    }
    with open(filename, 'r') as f:
        reader = DictReader(f)
        for line in reader:
            yield {k: (converters[k](v) if k in converters else v) for k, v in line.items()}


class MongoClientConnection:
    def disc(self):
        self.myclient.close()

    def __init__(self):
        self.client = pymongo.MongoClient(
            "mongodb://root:root@"+ip+":27017")
        mydb = self.client["test"]
        self.col = mydb["collection"]

    def usuwaniebazy(self):
        time1 = time.time_ns()
        self.col.drop()
        time2 = time.time_ns()
        return timconv(time1, time2)

    def importdanych(self):
        time1 = time.time_ns()
        print("start import")
        data = pd.read_csv('dataset.csv')
        payload = json.loads(data.to_json(orient='records'))
        self.col.insert_many(payload)
        time2 = time.time_ns()
        print("end import")

        return timconv(time1, time2)

    def iloscdanych(self):
        result = self.col.count_documents({})
        return int(result)

    def zapytanie1(self):
        time1 = time.time_ns()
        result = self.col.find()
        time2 = time.time_ns()
        return timconv(time1, time2)

    def zapytanie2(self):
        time1 = time.time_ns()
        myquery = {"anzsic06": {"$regex": "^A"}}
        result = self.col.find(myquery)
        time2 = time.time_ns()
        return timconv(time1, time2)

    def zapytanie3(self):
        time1 = time.time_ns()
        myquery = {"anzsic06": {"$regex": "^A"}}
        result = self.col.find(myquery).sort([('geo_count', 1)])
        time2 = time.time_ns()
        return timconv(time1, time2)

    def zapytanie4(self):
        time1 = time.time_ns()
        myquery = {"anzsic06": {"$regex": "^A"}}
        result = self.col.count_documents(myquery)
        time2 = time.time_ns()
        return timconv(time1, time2)

    def zapytanie5(self):
        time1 = time.time_ns()
        self.col.count_documents({})
        time2 = time.time_ns()
        return timconv(time1, time2)

    def zapytanie6(self):
        time1 = time.time_ns()
        self.col.aggregate(
            [{"$group": {"_id": "null", "sum": {"$sum": "$geo_count"}}}])
        time2 = time.time_ns()
        return timconv(time1, time2)

    def zapytanie7(self):
        return "~ 387.1104171"


class ClickHouse:
    def disc(self):
        self.client.disconnect()

    def __init__(self):
        self.client = clickhouse_driver.Client(ip)

    def usuwaniebazy(self, log):
        time1 = time.time_ns()
        result = self.client.execute('DROP TABLE test')
        time2 = time.time_ns()
        return timconv(time1, time2)

    def tworzeniebazy(self, log):
        time1 = time.time_ns()
        result = self.client.execute(
            'CREATE TABLE IF NOT EXISTS test (anzsic06 String, Area String, year Int32, geo_count Int32, ec_count Int32) ENGINE = Log')
        time2 = time.time_ns()
        return timconv(time1, time2)

    def importdanych(self, log):
        time1 = time.time_ns()
        self.client.execute('INSERT INTO test VALUES', iter_csv('dataset.csv'))
        time2 = time.time_ns()
        return timconv(time1, time2)

    def iloscdanych(self, log):
        result = self.client.execute("SELECT count() FROM test")
        return result

    def zapytanie1(self, log):
        # pobranie wszystkich rekordów
        time1 = time.time_ns()
        result = self.client.execute("SELECT * FROM test")
        time2 = time.time_ns()
        return timconv(time1, time2)

    def zapytanie2(self, log):
        # pobranie wszystkich rekordów gdzie kolumna "anzsic06" zaczyna się literą "A"
        time1 = time.time_ns()
        result = self.client.execute(
            "SELECT * FROM test WHERE anzsic06 like 'A%'")
        time2 = time.time_ns()
        if log:
            print(time2, " - ", time1, " = ", (time2-time1), "ns = ",
                  ((time2-time1)/1e6), "ms = ", ((time2-time1)/1e9), "s")
            print("Czas wywołania zapytania: ", timconv(time1, time2))
            print("10 pierwszych rekordów")
            i = 0
            for x in result:
                if i < 10:
                    print(x)
                    i += 1
                else:
                    break
        return timconv(time1, time2)

    def zapytanie3(self, log):
        # Pobranie sumy wszystkich rekordów gdzie kolumna "anzsic06" zaczyna się literą "A" pogrupowanych i posortowanych
        time1 = time.time_ns()
        result = self.client.execute(
            "SELECT count() FROM test WHERE anzsic06 like 'A%' GROUP BY geo_count ORDER BY geo_count")
        time2 = time.time_ns()
        if log:
            print("ilosć rekordów: ", result)
            print(time2, " - ", time1, " = ", (time2-time1), "ns = ",
                  ((time2-time1)/1e6), "ms = ", ((time2-time1)/1e9), "s")
            print("Czas wywołania zapytania: ", timconv(time1, time2))
        return timconv(time1, time2)

    def zapytanie4(self, log):
        # suma wszystkich rekordów gdzie kolumna "anzsic06" zaczyna się literą "A"
        time1 = time.time_ns()
        result = self.client.execute(
            "SELECT count() FROM test WHERE anzsic06 like 'A%'")
        time2 = time.time_ns()
        if log:
            print("ilosć rekordów: ", result)
            print(time2, " - ", time1, " = ", (time2-time1), "ns = ",
                  ((time2-time1)/1e6), "ms = ", ((time2-time1)/1e9), "s")
            print("Czas wywołania zapytania: ", timconv(time1, time2))
        return timconv(time1, time2)

    def zapytanie5(self, log):
        # ilosc wszystkich rekordów
        time1 = time.time_ns()
        result = self.client.execute("SELECT count() FROM test")
        time2 = time.time_ns()
        return timconv(time1, time2)

    def zapytanie6(self, log):
        # suma po jednej kolumnie
        time1 = time.time_ns()
        result = self.client.execute('SELECT SUM("geo_count") FROM test')
        time2 = time.time_ns()
        return timconv(time1, time2)

    def zapytanie7(self, log):
        # export
        time1 = time.time_ns()

        host = ip
        port = 2020
        username = "piotranon"
        password = "admin"
        command = 'clickhouse-client --query "SELECT * from test" --format CSV > out.csv'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password, banner_timeout=200)
        ssh.exec_command(command)

        time2 = time.time_ns()
        return timconv(time1, time2)
