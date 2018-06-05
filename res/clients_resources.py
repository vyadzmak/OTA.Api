from models.db_models.models import Clients
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse

#PARAMS
ENTITY_NAME = "Clients"
MODEL = Clients

#OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'registration_date': fields.DateTime,
    'registration_number': fields.String,
    'lock_state': fields.Boolean,
    'client_type_id': fields.Integer,
}


#API METHODS FOR SINGLE ENTITY
class ClientResource(Resource):
    @marshal_with(output_fields)
    def get(self, id):
        entity = session.query(MODEL).filter(MODEL.id == id).first()
        if not entity:
            abort(404, message=ENTITY_NAME+" {} doesn't exist".format(id))
        return entity

    def delete(self, id):
        try:
            entity = session.query(MODEL).filter(MODEL.id == id).first()
            if not entity:
                abort(404, message=ENTITY_NAME+" {} doesn't exist".format(id))
            session.delete(entity)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove "+ENTITY_NAME)

    @marshal_with(output_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            model = session.query(MODEL).filter(MODEL.id == id).first()
            model.name = json_data['name']
            model.registration_number = json_data["registration_number"]
            model.lock_state = json_data["lock_state"]
            model.client_type_id = json_data["client_type_id"]
            session.add(model)
            session.commit()
            return model, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update "+ENTITY_NAME)

#API METHODS FOR LIST ENTITIES
class ClientListResource(Resource):
    @marshal_with(output_fields)
    def get(self):
        entities = session.query(MODEL).all()
        return entities

    @marshal_with(output_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            entity = MODEL(name= json_data["name"],client_type_id=json_data["client_type_id"])
            session.add(entity)
            session.commit()
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record "+ENTITY_NAME)
