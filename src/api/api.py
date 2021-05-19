from flask import Blueprint, request, jsonify
from models import *
from operator import attrgetter
import requests, zipfile
import json
import io
import os
import glob
import csv


api = Blueprint('api', __name__, url_prefix='/api')

#Retornar um json com todos os jsons de deputados ordenados por nome
@api.route('/deputies')
def index():
    full_json = []
    sorted_list = sorted(Deputy.objects, key=attrgetter('name'))

    for deputy in sorted_list:
        full_json.append( deputy.to_json())

    return jsonify(full_json)

@api.route('/update_equity_growth')
def update_equity_growth():
    path = os.path.dirname(__file__) + "/temp"
    
    # r = requests.get("https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2018.zip")
    # z = zipfile.ZipFile(io.BytesIO(r.content))
    # z.extractall(path)

    csv_list = glob.glob(path + "/consulta_*.csv")
    for item in csv_list:
        csv_header = read_csv_file(item)
        return str(item)
        return jsonify(csv_header)

    return str(csv_list)

def read_csv_file(file):
    csv_list = []
    with open(file, 'r', encoding='utf-8', errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        next(csv_reader)

        for line in csv_reader:
            temp_json = {}
            temp_json["deputy_name"] = line[17]
            temp_json["deputy_id"] = line[15]
            csv_list.append(temp_json)
        
        return csv_list