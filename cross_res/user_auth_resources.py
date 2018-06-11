from models.db_models.models import UserLogins, Orders,Settings
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
from sqlalchemy import and_
import base64
import datetime
import models.app_models.setting_models.setting_model as settings
import urllib.parse

# PARAMS
ENTITY_NAME = "User Auth"
ROUTE = "/userAuth"
END_POINT = "user-auth"

# NESTED SCHEMA FIELDS
user_role_route_access_fields = {
    'user_role_id': fields.Integer,
    'admin_route_access': fields.Boolean,
    'data_settings_route_access': fields.Boolean,
    'catalog_route_access': fields.Boolean,
    'requests_route_access': fields.Boolean
}
user_role_data = {
    'id': fields.Integer,
    'name': fields.String,
    'title': fields.String,
    'user_role_route_access': fields.Nested(user_role_route_access_fields)
}

login_user_client_data = {
    'id': fields.Integer,
    'name': fields.String,
    'registration_number': fields.String
}

login_user_data = {
    'id': fields.Integer,
    'name': fields.String,
    'client_data': fields.Nested(login_user_client_data),
    'user_role_data': fields.Nested(user_role_data),
}
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'login': fields.String,
    'password': fields.String,
    'user_data': fields.Nested(login_user_data),
    'orders_count':fields.Integer,
    'last_login_date':fields.DateTime,
    'no_image_url': fields.String


}


# API METHODS FOR SINGLE ENTITY
class UserAuthResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('login')
            parser.add_argument('password')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            login = args['login']
            password = args['password']

            encrypted_password = str(base64.b64encode(bytes(password, "utf-8")))


            # check login
            user_login = session.query(UserLogins).filter(and_(
                UserLogins.login == login,
                UserLogins.password == encrypted_password)) \
                .first()

            if not user_login:
                abort(400, message='Ошибка авторизации. Пользователь с такими данными не найден!')

            if (user_login.user_data.lock_state==True):
                abort(400, message='Ошибка авторизации. Пользователь заблокирован!')

            if (user_login.user_data.client_data.lock_state==True):
                abort(400, message='Ошибка авторизации. Клиент (компания) заблокирован!')

            user_login.last_login_date =datetime.datetime.now(datetime.timezone.utc)
            session.add(user_login)
            session.commit()
            # get to additional params

            orders = session.query(Orders).filter(Orders.order_state_id==1).all()
            if (orders!=None):
                user_login.orders_count = len(orders)


            #no image url
            setting = session.query(Settings).filter(Settings.name=='no_image_url').first()
            if (not setting):
                return user_login
            api_url = settings.API_URL
            user_login.no_image_url=urllib.parse.urljoin(api_url, setting.value)
            return user_login
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

