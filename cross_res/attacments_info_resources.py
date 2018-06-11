from models.db_models.models import Attachments
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.image_path_converter_modules.image_path_converter as image_path_converter
from sqlalchemy import and_
import models.app_models.setting_models.setting_model as settings
import base64
import datetime

# PARAMS
ENTITY_NAME = "Attachments Info"
ROUTE = "/attachmentsInfo"
END_POINT = "attachments-info"

#NESTED SCHEMA FIELDS
user_data = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name")
}
#OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'upload_date':fields.DateTime,
    'original_file_name': fields.String,
    'file_size': fields.Integer,
    'file_path': fields.String,
    'user_creator_id': fields.Integer,
    'thumb_file_path': fields.String,
    'optimized_size_file_path': fields.String,
    'uid':fields.String,
    'attachment_user_data':fields.Nested(user_data),
}


# API METHODS FOR SINGLE ENTITY
class AttachmentsInfoResource(Resource):
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
            parser.add_argument('attachments_ids')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            attachments_ids = args['attachments_ids']
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)
            #clients = session.query(Clients).filter(Clients.id!=owner_client_id).order_by(Clients.id.desc()).all()
            attachments =[]
            attachments_ids =[int(s) for s in attachments_ids.split(',')]
            for id in attachments_ids:
                attachment = session.query(Attachments).filter(Attachments.id==id).first()
                if (not attachment):
                    continue

                image_path_converter.convert_path(attachment)
                attachments.append(attachment)

            if not attachments:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            return attachments
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

