from models.db_models.models import Users,UserLogins, Orders,Settings,UserInfo, Attachments,Clients, ClientAddresses,ClientInfo
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
ENTITY_NAME = "Update User Profile"
ROUTE = "/updateUserProfile"
END_POINT = "update-user-profile"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'status_code': fields.Integer
}


# API METHODS FOR SINGLE ENTITY
class UpdateUserProfileResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            user_id = json_data["user_id"]
            password = json_data["user_password"]
            user_name = json_data["user_name"]
            user_phone_number = json_data["user_phone_number"]
            user_email = json_data["user_email"]

            user= session.query(Users).filter(Users.id==user_id).first()

            if (not user):
                abort(400, message="User not found")

            user.name = user_name
            session.add(user)
            session.commit()

            user_login = session.query(UserLogins).filter(UserLogins.user_id==user_id).first()

            if (not user_login):
                abort(400, message="User Login not found")

            if (password!=''):
                encrypted_password = str(base64.b64encode(bytes(password, "utf-8")))
                user_login.password = encrypted_password
                session.add(user_login)
                session.commit()

            user_info  = session.query(UserInfo).filter(UserInfo.user_id==user_id).first()
            if (not user_info):
                abort(400, message="User Info not found")

            user_info.phone_number = user_phone_number
            user_info.email = user_email
            session.add(user_info)
            session.commit()

            response = {
                'status_code':200
            }

            return response
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update " + ENTITY_NAME)

