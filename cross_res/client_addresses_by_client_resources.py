from models.db_models.models import ClientAddresses
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging

# PARAMS
ENTITY_NAME = "Client Addresses by Client"
MODEL = ClientAddresses
ROUTE = "/clientAddressesByClient"
END_POINT = "client-addresses-by-client"

# NESTED SCHEMA FIELDS
area_data_fields = {
    'id': fields.Integer,
    'name': fields.String,

}
city_data_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'area_id': fields.Integer,
    'area_data': fields.Nested(area_data_fields)
}

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'client_id': fields.Integer,
    'address': fields.String,
    'is_default': fields.Boolean,
    'name': fields.String,
    'confirmed': fields.Boolean,
    'tobacco_alcohol_license': fields.Boolean,
    'code': fields.String,
    'city_id': fields.Integer,
    'city_data': fields.Nested(city_data_fields),
    'phone_number': fields.String
}


# API METHODS FOR SINGLE ENTITY
class ClientAddressesByClientResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self):
        try:

            action_type = 'GET'
            parser = reqparse.RequestParser()
            parser.add_argument('user_id')
            parser.add_argument('client_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            client_id = args['client_id']
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)
            client_addresses = session.query(ClientAddresses).filter(ClientAddresses.client_id == client_id).all()

            if not client_addresses:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            return client_addresses
        except Exception as e:
            if (hasattr(e, 'data')):
                if (e.data != None and "message" in e.data):
                    abort(400, message=e.data["message"])
            abort(400, message="Неопознанная ошибка")
