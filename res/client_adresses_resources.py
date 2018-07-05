from models.db_models.models import ClientAddresses
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer

#PARAMS
ENTITY_NAME = "Client Adresses"
MODEL = ClientAddresses
ROUTE ="/clientAddresses"
END_POINT = "client-addresses"

#NESTED SCHEMA FIELDS
area_data_fields ={
    'id': fields.Integer,
    'name': fields.String,

}
city_data_fields = {
    'id':fields.Integer,
    'name':fields.String,
    'area_id':fields.Integer,
    'area_data':fields.Nested(area_data_fields)
}
#OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'client_id':fields.Integer,
    'address': fields.String,
    'is_default': fields.Boolean,
    'name': fields.String,
    'confirmed':fields.Boolean,
    'tobacco_alcohol_license':fields.Boolean,
    'code':fields.String,
    'city_id': fields.Integer,
    'city_data':fields.Nested(city_data_fields)
}


def check_default_address(entity):
    try:
        client_id = entity.client_id
        is_default = entity.is_default
        id = entity.id

        client_addresses = session.query(ClientAddresses).filter(ClientAddresses.client_id == client_id).all()

        if (len(client_addresses) == 1):
            for client_address in client_addresses:
                client_address.is_default = True
                session.add(client_address)
                session.commit()
                return

        if (is_default == False):
            return

        for client_address in client_addresses:
            if (client_address.id == id):
                client_address.is_default = True
            else:
                client_address.is_default = False
            session.add(client_address)
            session.commit()

        pass
    except Exception as e:
        pass

#API METHODS FOR SINGLE ENTITY
class ClientAddressesResource(Resource):
    def __init__(self):
        self.route = ROUTE+'/<int:id>'
        self.end_point = END_POINT
        pass



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
            entity = session.query(MODEL).filter(MODEL.id == id).first()
            if not entity:
                abort(404, message=ENTITY_NAME + " {} doesn't exist".format(id))
            db_transformer.transform_update_params(entity,json_data)
            session.add(entity)
            session.commit()
            check_default_address(entity)
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update "+ENTITY_NAME)

#API METHODS FOR LIST ENTITIES
class ClientAddressesListResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT+'-list'
        pass

    @marshal_with(output_fields)
    def get(self):
        entities = session.query(MODEL).all()
        return entities

    @marshal_with(output_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            entity = MODEL(json_data)
            session.add(entity)
            session.commit()
            check_default_address(entity)
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record "+ENTITY_NAME)

