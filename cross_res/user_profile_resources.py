from models.db_models.models import UserLogins, Orders, Settings, UserInfo, Attachments, Clients, ClientAddresses, \
    ClientInfo, UserBonuses
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
ENTITY_NAME = "User Profile"
ROUTE = "/userProfile"
END_POINT = "user-profile"

# NESTED SCHEMA FIELDS
user_bonuses_fields = {
    'id': fields.Integer,
    'order_id': fields.Integer,
    'user_id': fields.Integer,
    'creation_date': fields.DateTime,
    'state': fields.Boolean,
    'amount': fields.Float
}

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
client_addresses_fields = {
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
client_info_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'main_info': fields.String,
    'additional_info': fields.String,
    'phone_number': fields.String
}

login_user_client_data = {
    'id': fields.Integer,
    'name': fields.String,
    'registration_number': fields.String,
    'client_addresses': fields.Nested(client_addresses_fields),
    'client_info': fields.Nested(client_info_fields),
}

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
    "id": fields.Integer,
    "user_id": fields.Integer,
    "email": fields.String,
    "phone_number": fields.String,
    "birthday": fields.String,
    'avatar_id': fields.Integer,
    'avatar_data': fields.Nested(avatar_data_fields)
}
login_user_data = {
    'id': fields.Integer,
    'name': fields.String,
    'client_data': fields.Nested(login_user_client_data),
    'user_info': fields.Nested(user_info_data)
}

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'login': fields.String,
    'password': fields.String,
    'user_data': fields.Nested(login_user_data),
    'last_login_date': fields.DateTime,
    'no_image_url': fields.String,
    'no_avatar_url': fields.String,
    'thumbs_avatar_path': fields.String,
    'user_bonuses': fields.Nested(user_bonuses_fields),
    'total_bonuses_amount': fields.Float,
    'start_bonus_date': fields.String,
    'end_bonus_date': fields.String,

}


# API METHODS FOR SINGLE ENTITY
class UserProfileResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self):
        error_message = ''
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']

            # check login
            user_login = session.query(UserLogins).filter(UserLogins.user_id == user_id).first()

            # no image url
            setting = session.query(Settings).filter(Settings.name == 'no_image_url').first()
            if (not setting):
                return user_login
            # api_url = settings.API_URL
            user_login.no_image_url = setting.value

            setting = session.query(Settings).filter(Settings.name == 'no_avatar_url').first()
            if (not setting):
                return user_login
            # api_url = settings.API_URL
            user_login.no_avatar_url = setting.value

            # getting avatar
            user_info = session.query(UserInfo).filter(UserInfo.user_id == user_login.id).first()
            if user_info:
                attachment = session.query(Attachments).filter(Attachments.id == user_info.avatar_id).first()
                if attachment:
                    user_login.thumbs_avatar_path = attachment.thumb_file_path

            user_login.user_data.user_info = user_info
            client_id = user_login.user_data.client_data.id
            addresses = session.query(ClientAddresses).filter(ClientAddresses.client_id == client_id).all()

            user_login.user_data.client_data.client_addresses = addresses

            client_info = session.query(ClientInfo).filter(ClientInfo.client_id == client_id).first()

            if (not client_info):
                client_info_args = {}
                client_info_args["client_id"] = client_id
                client_info_entity = ClientInfo(client_info_args)
                session.add(client_info_entity)
                session.commit()
                client_info = client_info_entity
            user_login.user_data.client_data.client_info = client_info

            user_bonuses = session.query(UserBonuses).filter(and_(
                UserBonuses.user_id == user_id,
                UserBonuses.state == True)) \
                .all()

            user_login.user_bonuses = []

            if (user_bonuses != None and len(user_bonuses) > 0):
                total_bonuses_amount = 0
                start_bonus_date = user_bonuses[0].creation_date
                end_bonus_date = user_bonuses[len(user_bonuses) - 1].creation_date

                for bonus in user_bonuses:
                    total_bonuses_amount += bonus.amount

                user_login.user_bonuses = user_bonuses
                user_login.start_bonus_date = start_bonus_date.strftime("%Y-%m-%d %H:%M")
                user_login.end_bonus_date = end_bonus_date.strftime("%Y-%m-%d %H:%M")
                user_login.total_bonuses_amount = total_bonuses_amount

            return user_login
        except Exception as e:
            abort(400, message=error_message)
