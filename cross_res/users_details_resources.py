from models.db_models.models import Users, UserLogins,UserInfo
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.image_path_converter_modules.image_path_converter as image_path_converter
#PARAMS
ENTITY_NAME = "Users Details"
MODEL = Users
ROUTE ="/userDetails"
END_POINT = "user-details"

# NESTED SCHEMA FIELDS
avatar_data_fields = {
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
user_info_data = {
    "id":fields.Integer,
    "user_id":fields.Integer,
    "email":fields.String,
    "phone_number":fields.String,
    "birthday":fields.String,
    'avatar_id':fields.Integer,
    'avatar_data':fields.Nested(avatar_data_fields)
}

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
    'id': fields.Integer,
    'name': fields.String,
    'lock_state': fields.Boolean,
    'client_data': fields.Nested(user_client_data),
    'user_role_data': fields.Nested(user_role_data),
    'user_login': fields.Nested(user_login_data),
    'user_info_data':fields.Nested(user_info_data)
}

#API METHODS FOR SINGLE ENTITY
class UsersDetailsResource(Resource):
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
            parser.add_argument('request_user_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            request_user_id = args['request_user_id']
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)
            user = session.query(Users).filter(Users.id==request_user_id).first()
            if not user:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            user.user_login = session.query(UserLogins).filter(UserLogins.user_id==user.id).first()
            user.user_info_data = session.query(UserInfo).filter(UserInfo.user_id == user.id).first()
            return user

        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")



