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

@api.route('/csv_deputies')
def csv_deputies():
    full_json = []
    for item in CsvDeputy.objects:
        full_json.append(item.to_json())

    return jsonify(full_json)

@api.route('/delete_csv_deputies')
def delete_csv_deputies():
    CsvDeputy.objects.all().delete() 
    return "All csv deputies in database was deleted! Use api/update_equity_growth to update database."

@api.route('/update_csv_deputies')
def update_csv_deputies():
    path = os.path.dirname(__file__) + "/temp"
    
    r = requests.get("https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2018.zip")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path)

    csv_list = glob.glob(path + "/consulta_*.csv")
    #Verifcar cada tabela de csv
    for csv_file in csv_list:
        deputies_json_csv = read_csv_file(csv_file)

        #O retorno da tabela é uma lista com o nome e id de cada deputado
        for deputy_json in deputies_json_csv:
            name = deputy_json["csv_deputy_name"].lower()

            for deputy in Deputy.objects:
                old_deputy = CsvDeputy.objects(deputy_id=deputy.id).first()
                if old_deputy:
                    continue

                if name in deputy.full_name.lower():
                    #deputado encontrado, criar a classe com ele e o id
                    CsvDeputy(
                        csv_id = deputy_json["csv_deputy_id"],
                        deputy_name = deputy.name,
                        deputy_id = deputy.id
                    ).save()

    return csv_deputies()

def read_csv_file(file):
    csv_list = []
    with open(file, 'r', encoding='utf-8', errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        next(csv_reader)

        for line in csv_reader:
            temp_json = {}
            temp_json["csv_deputy_name"] = line[17]
            temp_json["csv_deputy_id"] = line[15]
            csv_list.append(temp_json)
        
        return csv_list