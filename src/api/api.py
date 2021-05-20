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
    links_list = ["https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2018.zip",
    "https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2014.zip"]
    
    for link in links_list:
        r = requests.get(link)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path)

    csv_list = glob.glob(path + "/consulta_*.csv")
    #Verifcar cada tabela de csv
    for csv_file in csv_list:
        print(csv_file.title(), flush=True)
        deputies_json_csv = read_csv_file(csv_file)
        #O retorno da tabela é uma lista com o nome e id de cada deputado
        for deputy_json in deputies_json_csv:
            deputy = Deputy.objects(full_name__iexact = deputy_json["csv_deputy_name"]).first()

            if not deputy:
                deputy = Deputy.objects(name__iexact = deputy_json["csv_fake_name"]).first()

            if deputy:
                if "2014" in csv_file.title():
                    print(f"Arrombed : {deputy.name}", flush=True)
                #deputado encontrado, criar a classe com ele e o id
                CsvDeputy(
                    csv_id = deputy_json["csv_deputy_id"],
                    deputy_name = deputy.name,
                    deputy_id = deputy.id
                ).save()

    return "Done. Use /csv_deputies to get all csv deputy in database."

def read_csv_file(file):
    csv_list = []
    with open(file, 'r', encoding='utf-8', errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        next(csv_reader)

        for line in csv_reader:
            temp_json = {}
            temp_json["csv_deputy_name"] = line[17]
            temp_json["csv_deputy_id"] = line[15]
            temp_json["csv_fake_name"] = line[18]
            csv_list.append(temp_json)
        
        return csv_list

@api.route('/update_deputies_equity')
def update_deputies_equity():
    path = os.path.dirname(__file__) + "/temp"
    csv_links = ["https://cdn.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_2018.zip",
    "https://cdn.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_2014.zip"]
    
    #baixar todas as planilhas corretas.
    for link in csv_links:
        r = requests.get(link)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(path)

    csv_list = glob.glob(path + "/bem_candidato_*.csv")
    #Verifcar cada tabela de csv
    for csv_file in csv_list:
        csv_json_list = get_deputy_infos_in_csv(csv_file)

        for csv_json in csv_json_list:
            deputy = CsvDeputy.objects(csv_id=csv_json["csv_deputy_id"]).first()

            if not deputy:
                continue

            DeputyEquity(
                id = str(deputy.deputy_id) + "-" + str(csv_json["csv_year"]) + "-" + csv_json["csv_order_number"],
                csv_id = str(csv_json["csv_deputy_id"]),
                deputy_name = deputy.deputy_name,
                deputy_id = int(deputy.deputy_id),
                value = str(csv_json["csv_value"]), 
                description = str(csv_json["csv_description"]) if not "#NULO#" in csv_json["csv_description"] else None,
                type = str(csv_json["csv_equity_type"]),
                year = int(csv_json["csv_year"])
            ).save()
        
    return "Done. Use /get_all_deputies_equity to get all deputies equity in database."

def get_deputy_infos_in_csv(file):
    csv_list = []
    with open(file, 'r', encoding='utf-8', errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        next(csv_reader)

        for line in csv_reader:
            temp_json = {}
            temp_json["csv_equity_type"] = line[14]
            temp_json["csv_description"] = line[15]
            temp_json["csv_value"] = line[16]
            temp_json["csv_deputy_id"] = line[11]
            temp_json["csv_year"] = line[2]
            temp_json["csv_order_number"] = line[12]
            csv_list.append(temp_json)
        
        return csv_list

@api.route('/delete_deputies_equity')
def delete_deputies_equity():
    DeputyEquity.objects.all().delete() 
    return "All deputies equity in database was deleted! Use api/update_deputies_equity to update database."

@api.route('/get_all_deputies_equity')
def get_all_deputies_equity():
    json_list = []
    for item in DeputyEquity.objects():
        json_list.append(item.to_json())

    return jsonify(json_list)

@api.route('/get_deputies_equity/<id>')
def get_deputies_equity(id):
    equities = DeputyEquity.objects(deputy_id=id).all()
    json_list = []

    for item in equities:
        json_list.append(item.to_json())

    return jsonify(json_list)

@api.route('/get_filtered_deputies_equity', methods=['POST'])
def get_filtered_deputies_equity():
    #json {"id" e "year"}
    requested_json = request.get_json()
    deputy_equity_list = []

    if not requested_json["id"]:
        deputy_equity_list = list(DeputyEquity.objects().all())
    else:
        deputy_equity_list = list(DeputyEquity.objects(deputy_id=requested_json["id"]).all())

    json_list = []
    
    if not deputy_equity_list:
        return jsonify(json_list)

    for item in deputy_equity_list:
        if requested_json["year"]:
            if (int(item.year) == int(requested_json["year"])):
                json_list.append(item.to_json())
        else:
            json_list.append(item.to_json())

    return jsonify(json_list)

@api.route('/get_total_value_deputies_equity/<id>')
def get_total_value_deputies_equity(id):
    equities = DeputyEquity.objects(deputy_id=id).all()
    json_value = {}
    amount = 0.0
    deputy = Deputy.objects(id=id).first()
    
    if not deputy:
        return json_value
    
    if not equities:
        return json_value

    for item in equities:
        float_value = item.value.replace(",", ".")
        amount = amount + float(float_value)

    json_value["value"] = amount
    json_value["deputy_id"] = deputy.id
    json_value["deputy_name"] = deputy.name
    return json_value

@api.route('/get_total_value_deputies_equity_by_year/<id>')
def get_total_value_deputies_equity_by_year(id):
    equities = DeputyEquity.objects(deputy_id=id).all()
    list_json = []

    amount_2018 = 0.0
    amount_2014 = 0.0
    deputy = Deputy.objects(id=id).first()
    
    if not deputy:
        return list_json
    
    if not equities:
        return list_json

    for item in equities:
        float_value = item.value.replace(",", ".")
        if item.year == 2018:
            amount_2018 = amount_2018 + float(float_value)
        else:
            amount_2014 = amount_2014 + float(float_value)
    
    
    if amount_2014 > 0:
        json_value = {}
        json_value["value"] = float("{:.2f}".format(amount_2014))
        json_value["year"] = 2014
        list_json.append(json_value)
    if amount_2018 > 0:
        json_value = {}
        json_value["value"] = float("{:.2f}".format(amount_2018))
        json_value["year"] = 2018
        list_json.append(json_value)
    
    return jsonify(list_json)

@api.route('/update_all_equity')
def update_all_equity():
    update_csv_deputies()
    update_deputies_equity()
    return "Done."
