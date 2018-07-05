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
ENTITY_NAME = "Update Client Profile"
ROUTE = "/updateClientProfile"
END_POINT = "update-client-profile"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'status_code': fields.Integer
}


# API METHODS FOR SINGLE ENTITY
class UpdateClientProfileResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            client_id = json_data["client_id"]
            client_name = json_data["client_name"]
            client_registration_number = json_data["client_registration_number"]
            client_phone_number = json_data["client_phone_number"]
            client_email = json_data["client_email"]
            client_main_info = json_data["client_main_info"]
            client_additional_info = json_data["client_additional_info"]

            client = session.query(Clients).filter(Clients.id==client_id).first()

            if (not client):
                abort(400, message ='Client not found')


            client.name = client_name
            client.registration_number = client_registration_number
            session.add(client)
            session.commit()

            client_info = session.query(ClientInfo).filter(ClientInfo.client_id==client_id).first()
            if (not client_info):
                abort(400, message ='Client Info not found')


            client_info.email = client_email
            client_info.phone_number = client_phone_number
            client_info.main_info = client_main_info
            client_info.additional_info = client_additional_info
            session.add(client_info)
            session.commit()


            response = {
                'status_code':200
            }

            return response
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update " + ENTITY_NAME)

