import json
from flask import Blueprint, request
from models import *
from operator import attrgetter

api = Blueprint('api', __name__, url_prefix='/api')

#Retornar um json com todos os jsons de deputados ordenados por nome
@api.route('/deputies')
def index():
    full_json = {}
    sorted_list = sorted(Deputy.objects, key=attrgetter('name'))
    cont = 0

    for deputy in sorted_list:
        temp_json = deputy.to_json(deputy)
        full_json[cont] = temp_json
        cont += 1

    return full_json

