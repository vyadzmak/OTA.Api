import os
from models.db_models.models import Settings
from db.db import session
from flask import Flask, jsonify, request,send_from_directory
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import models.app_models.setting_models.setting_model as settings
from pathlib import Path
#PARAMS
ENTITY_NAME = "Attachment Thumbs View"
#MODEL = Settings
ROUTE ="/uploads/thumbs"
END_POINT = "attachment-thumbs-view"

#NESTED SCHEMA FIELDS

#OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'name':fields.String,
    'value': fields.String
}


#API METHODS FOR SINGLE ENTITY
class AttachmentThumbsViewResource(Resource):
    def __init__(self):
        self.route = ROUTE+'/<path:image>'
        self.end_point = END_POINT
        pass

    #@marshal_with(output_fields)
    def get(self, image):
        try:
            file_path =settings.ROOT_DIR.replace("\\","/")+"/"+settings.UPLOADS_FOLDER_THUMBS
            return send_from_directory(file_path,image)
        except Exception as e:
            abort(404, message="File not found")

