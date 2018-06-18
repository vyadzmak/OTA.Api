from models.db_models.models import Users, UserLogins
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.image_path_converter_modules.image_path_converter as image_path_converter
#PARAMS
ENTITY_NAME = "Users By Client"
MODEL = Users
ROUTE ="/usersByClient"
END_POINT = "users-by-client"

# NESTED SCHEMA FIELDS
user_role_data = {
    'id': fields.Integer,
    'name': fields.String,
    'title': fields.String,

}

user_client_data = {
    'id': fields.Integer,
    'name': fields.String,
    'registration_number': fields.String
}

user_login_data = {
    'id': fields.Integer,
    'login': fields.String,
    'last_login_date': fields.DateTime
}
# OUTPUT SCHEMA
output_fields = {
    'id':fields.Integer,
    'name': fields.String,
    'lock_state':fields.Boolean,
    'client_data': fields.Nested(user_client_data),
    'user_role_data': fields.Nested(user_role_data),
    'user_login':fields.Nested(user_login_data)
}


#API METHODS FOR SINGLE ENTITY
class UsersByClientResource(Resource):
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
            users = session.query(Users).filter(Users.client_id==client_id).all()
            if not users:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            for user in users:
                user.user_login = session.query(UserLogins).filter(UserLogins.user_id==user.id).first()
            return users
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")



