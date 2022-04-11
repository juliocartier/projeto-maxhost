from flask import Flask
from flask import Blueprint
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy

from flask_restful import Api, Resource, fields

import sqlite3

from flasgger import Swagger

import os

#from app.resources.api import Create

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.dirname(os.path.abspath(__file__))  + '/banco.db'
app.config['SQLALCHMEY_TRACK_MODIFICATIONS'] = False

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.dirname(os.path.abspath(__file__))  +'/db_users_sessions.db'

app.config['SWAGGER'] = {
    'title': 'Api Zumbie',
    'uiversion': 3
}

SWAGGER_TEMPLATE ={
    "info":{
        "title": "Api Zumbie",
        "description": "Api Zumbie",
        "version": "1.0.0",
        "contact": {
            "name": "Julio Cartier",
            "url": ""
        }
    }
}


db = SQLAlchemy(app)
db.init_app(app)
api = Api(app)

swag = Swagger(app, template=SWAGGER_TEMPLATE)

CORS(app)

from app.models.survivors import Survivors
from app.models.marker import Markers
db.create_all()
#blue_simulacao = Blueprint('api', __name__)

#from app.resources.zombie_apocalypse import api
from app.resources.zombie_apocalypse import Index,\
                                            SurvivorsSearch, \
                                            SurvivorSearch, \
                                            SurvivorCreate, \
                                            SurvivorUpdate, \
                                            SurvivorNext, \
                                            SurvivorMarker

api.add_resource(Index, '/')
api.add_resource(SurvivorsSearch, '/search_survivors')
api.add_resource(SurvivorCreate, '/create')
api.add_resource(SurvivorMarker, '/create_marker')
api.add_resource(SurvivorSearch, '/search_survivor')
api.add_resource(SurvivorUpdate, '/update_survivor')
api.add_resource(SurvivorNext, '/search_survivor_next')



#api_simulacao = Api(blue_simulacao)

#api_simulacao.add_resource(Create, '/create')