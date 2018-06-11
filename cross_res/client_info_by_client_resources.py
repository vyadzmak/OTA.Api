from models.db_models.models import ClientInfo
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging

#PARAMS
ENTITY_NAME = "Client Info by Client"
MODEL = ClientInfo
ROUTE ="/clientInfoByClient"
END_POINT = "client-info-by-client"

#NESTED SCHEMA FIELDS
attachment_data = {
    'id': fields.Integer,
    'original_file_name': fields.String,
    'file_path': fields.String,
    'file_size': fields.Integer,
    'uid': fields.String,
    'user_creator_id': fields.Integer,
    'upload_date': fields.DateTime,
    'thumb_file_path': fields.String,
    'optimized_size_file_path': fields.String
}
#OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'client_id':fields.Integer,
    'logo_attachment_id': fields.Integer,
    'email': fields.String,
    'main_info': fields.String,
    'additional_info': fields.String,
    'attachment_data':fields.Nested(attachment_data)
}


#API METHODS FOR SINGLE ENTITY
class ClientInfoByClientResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self):
        try:

            action_type='GET'
            parser = reqparse.RequestParser()
            parser.add_argument('user_id')
            parser.add_argument('client_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            client_id = args['client_id']
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)
            client_info = session.query(ClientInfo).filter(ClientInfo.client_id==client_id).first()

            if not client_info:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            return client_info
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")



