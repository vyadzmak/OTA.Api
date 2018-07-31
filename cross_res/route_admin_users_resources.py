from models.db_models.models import AdminSettings, Log, Users,UserLogins, UserInfo
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
import models.app_models.setting_models.setting_model as settings
from sqlalchemy import and_
import base64
import datetime

# PARAMS
ENTITY_NAME = "Route Admin Users"
ROUTE = "/routeAdminUsers"
END_POINT = "route-admin-users"

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



# API METHODS FOR SINGLE ENTITY
class RouteAdminUsersResource(Resource):
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
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']

            user_action_logging.log_user_actions(ROUTE,user_id, action_type)

            # check login
            owner_users = session.query(Users).filter(Users.client_id==settings.OWNER_CLIENT_ID).order_by(Users.id.desc()).all()
            for user in owner_users:
                u_id = user.id
                login = session.query(UserLogins).filter(UserLogins.user_id==u_id).first()
                if not login:
                    continue

                user.user_login = login

            for user in owner_users:
                u_id = user.id

                user_info = session.query(UserInfo).filter(UserInfo.user_id == user.id).first()

                if not user_info:
                    continue

                user.user_info_data = user_info

            if not owner_users:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            return owner_users
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

