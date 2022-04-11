from flask import jsonify, make_response
from flask_restful import Resource, reqparse

from app.models.survivors import Survivors
from app.models.marker import Markers

argumentos = reqparse.RequestParser()
argumentos.add_argument('name', type=str)
argumentos.add_argument('gender', type=str)
argumentos.add_argument('lat', type=float)
argumentos.add_argument('lon', type=float)

argumentos_update = reqparse.RequestParser()
argumentos_update.add_argument('id', type=int)
argumentos_update.add_argument('name', type=str)
argumentos_update.add_argument('gender', type=str)
argumentos_update.add_argument('lat', type=float)
argumentos_update.add_argument('lon', type=float)

argumentos_search = reqparse.RequestParser()
argumentos_search.add_argument('name', type=str)

argumentos_search_next = reqparse.RequestParser()
argumentos_search_next.add_argument('name', type=str)

argumentos_marker = reqparse.RequestParser()
argumentos_marker.add_argument('name', type=str)
argumentos_marker.add_argument('name_infect', type=str)
cont = 0
name = []

class Index(Resource):
    #@api.route('/')
    def get(self):
        """
        Return welcome
        ---
        tags:
          - Consultas
        parameters:
          - in: body
            name: query
        responses:
          200:
            description: Ok
        """
        return jsonify("Welcome Zombie Apocalypse")

class SurvivorsSearch(Resource):

    def get(self):
        """
        Return the survivors
        ---
        tags:
          - Consultas
        parameters:
          - in: body
            name: query
        responses:
          200:
            description: Ok
        """
        try:
            return {'survivors': [survivors.json() for survivors in Survivors.query.all()]}
        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500

class SurvivorSearch(Resource):
    def post(self):
        """
        Search a survivors
        ---
        tags:
          - Consultas
        parameters:
          - in: body
            name: query
            schema:
              $ref: '#/definitions/search_survivor'
        responses:
          201:
            description: Ok
        definitions:
          search_survivor:
            type: object
            properties:
              name:
                type: string
        """
        try:
            datas = argumentos_search.parse_args()
            survivors = Survivors.find_survivor(datas['name'])

            if survivors:
                return survivors.json()
            return {'message': 'Survivor not found'}, 404 #not found

        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500

class SurvivorCreate(Resource):
    def post(self):
        """
        Create a Survivors
        ---
        tags:
          - Consultas
        parameters:
          - in: body
            name: query
            schema:
              $ref: '#/definitions/create'
        responses:
          201:
            description: Ok
        definitions:
          create:
            type: object
            properties:
              name:
                type: string
              gender:
                type: string
              lat:
                type: number
              lon:
                type: number
        """
        try:

            datas = argumentos.parse_args()
            if Survivors.find_survivors(datas['name']):
                return {"message": "The Survivers '{}' already exists.".format(datas['name'])}

            user = Survivors(**datas)
            user.save_survivors()
            return {"message": 'Survivor create successfully!'}, 201

        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500

class SurvivorMarker(Resource):

    def post(self):
        """
        Add a infected survivors
        ---
        tags:
          - Consultas
        parameters:
          - in: body
            name: query
            schema:
              $ref: '#/definitions/create_marker'
        responses:
          201:
            description: Ok
        definitions:
          create_marker:
            type: object
            properties:
              name:
                type: string
              name_infect:
                type: string
        """
        try:
            global cont, name
            datas = argumentos_marker.parse_args()

            if datas['name'] != datas['name_infect']:

                if Markers.find_marker(datas['name_infect']):
                    return {"message": 'Survivor Marker!'}, 201
                else:
                    if datas['name'] in name:
                        return {"message": 'Survivor already marked!'}, 201
                    else:
                        name.append(datas['name'])
                        cont = cont + 1
                        if cont == 3:
                            cont = 0
                            user = Markers(datas['name_infect'], True)
                            user.save_marker()
                            return {"message": "The Survivers Infect '{}'.".format(datas['name_infect'])}
                        else:
                            return {"message": 'Survivor Marker Infect!'}, 201
            else:
                return {"message": 'Survivor Marker Infect!'}, 201
        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500

class SurvivorNext(Resource):
    def post(self):
        """
        Look for a nearest survivor
        ---
        tags:
          - Consultas
        parameters:
          - in: body
            name: query
            schema:
              $ref: '#/definitions/search_survivor_next'
        responses:
          201:
            description: Ok
        definitions:
          search_survivor_next:
            type: object
            properties:
              name:
                type: string
        """
        try:
            datas = argumentos_search_next.parse_args()
            survivors = Survivors.find_survivors_next(self, datas['name'])
            #print("Entrouu nessa class", survivors)
            if survivors:
                return jsonify(
                        usuario=survivors[0][0],
                        usuario_prox=survivors[0][1],
                        distancia=survivors[0][2],
                    )
            return {'message': 'Survivor not found'}, 404 #not found
        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500

class SurvivorUpdate(Resource):

    def put(self):
        """
        Update a survivors
        ---
        tags:
          - Consultas
        parameters:
          - in: body
            name: query
            schema:
              $ref: '#/definitions/update_survivor'
        responses:
          201:
            description: Ok
        definitions:
          update_survivor:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              gender:
                type: string
              lat:
                type: number
              lon:
                type: number
        """
        try:
            datas = argumentos_update.parse_args()

            if Survivors.find_survivors_id(datas['id']):
                user = Survivors(datas['name'], datas['gender'], datas['lat'], datas['lon'])
                user.update_survivors(**datas)
                return user.json(), 200 # OK
            else:
                return {'message': 'Survivor not found'}, 404 #not found
        except Exception as e:
            return jsonify({'status': 500, 'msg': f'{e}'}), 500