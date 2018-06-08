from models.db_models.models import Clients, ClientInfo
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import and_
import base64
import datetime

# PARAMS
ENTITY_NAME = "Route Admin Clients"
ROUTE = "/routeAdminClients"
END_POINT = "route-admin-clients"

# NESTED SCHEMA FIELDS
client_type_data_fields={
    'id':fields.Integer,
    'name': fields.String,
    'title': fields.String
}

client_info_fields={
    'id':fields.Integer,
    'email': fields.String,
    'main_info': fields.String,
    'additional_info': fields.String,
    'phone_number': fields.String
}

client_addresses_fields={
    'id':fields.Integer,
    'address': fields.String,
    'is_default': fields.Boolean
}
# OUTPUT SCHEMA
output_fields = {
    'id':fields.Integer,
    'name': fields.String,
    'registration_number': fields.String,
    'lock_state':fields.Boolean,
    'client_type_data':fields.Nested(client_type_data_fields),
    'client_info_data': fields.Nested(client_info_fields),
    'client_addresses_data': fields.Nested(client_addresses_fields)
}


# API METHODS FOR SINGLE ENTITY
class RouteAdminClientsResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self):
        try:
            owner_client_id = 3
            action_type='GET'
            parser = reqparse.RequestParser()
            parser.add_argument('user_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']

            user_action_logging.log_user_actions(ROUTE,user_id, action_type)
            clients = session.query(Clients).filter(Clients.id!=owner_client_id).order_by(Clients.id.desc()).all()
            if not clients:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            return clients
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

