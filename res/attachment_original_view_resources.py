import os
from models.db_models.models import Settings
from db.db import session
from flask import Flask, jsonify, request,send_from_directory
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import models.app_models.setting_models.setting_model as settings
from pathlib import Path
#PARAMS
ENTITY_NAME = "Attachment Original View"
#MODEL = Settings
ROUTE ="/uploads/original"
END_POINT = "attachment-original-view"

#NESTED SCHEMA FIELDS

#OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'name':fields.String,
    'value': fields.String
}


#API METHODS FOR SINGLE ENTITY
class AttachmentOriginalViewResource(Resource):
    def __init__(self):
        self.route = ROUTE+'/<path:folder>/<path:image>'
        self.end_point = END_POINT
        pass

    #@marshal_with(output_fields)
    def get(self, folder,image):
        ttt=0
        s = settings.ROOT_DIR.replace("\\","/")+"/"
        s+=settings.UPLOADS_FOLDER_ORIGINAL+folder
        file_path =s
        return send_from_directory(file_path,image)

