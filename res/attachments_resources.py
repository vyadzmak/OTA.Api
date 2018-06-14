from models.db_models.models import Attachments
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import models.app_models.setting_models.setting_model as settings
import urllib.parse

#PARAMS
ENTITY_NAME = "Attachments"
MODEL = Attachments
ROUTE ="/attachments"
END_POINT = "attachments"

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


#API METHODS FOR SINGLE ENTITY
class AttachmentsResource(Resource):
    def __init__(self):
        self.route = ROUTE+'/<int:id>'
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self, id):
        try:
            # session.autocommit = False
            # session.autoflush = False
            entity = session.query(MODEL).filter(MODEL.id == id).first()
            if not entity:
                abort(404, message=ENTITY_NAME+" {} doesn't exist".format(id))
            # api_url = settings.API_URL
            # if (entity.file_path!=None):
            #     entity.file_path=urllib.parse.urljoin(api_url, entity.file_path)
            #
            # if (entity.thumb_file_path!=None):
            #     entity.thumb_file_path=urllib.parse.urljoin(api_url, entity.thumb_file_path)
            #
            # if (entity.optimized_size_file_path!=None):
            #     entity.optimized_size_file_path=urllib.parse.urljoin(api_url, entity.optimized_size_file_path)
            return entity
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update " + ENTITY_NAME)
        finally:
            pass
            #session.rollback()

    def delete(self, id):
        try:
            entity = session.query(MODEL).filter(MODEL.id == id).first()
            if not entity:
                abort(404, message=ENTITY_NAME+" {} doesn't exist".format(id))
            session.delete(entity)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove "+ENTITY_NAME)

    @marshal_with(output_fields)
    def put(self, id):
        try:
            # session.autocommit = False
            # session.autoflush = False
            json_data = request.get_json(force=True)
            entity = session.query(MODEL).filter(MODEL.id == id).first()
            if not entity:
                abort(404, message=ENTITY_NAME + " {} doesn't exist".format(id))
            db_transformer.transform_update_params(entity,json_data)
            session.add(entity)
            session.commit()
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update "+ENTITY_NAME)

#API METHODS FOR LIST ENTITIES
class AttachmentsListResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT+'-list'
        pass

    @marshal_with(output_fields)
    def get(self):
        entities = session.query(MODEL).all()
        return entities

    @marshal_with(output_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            entity = MODEL(json_data)
            session.add(entity)
            session.commit()
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record "+ENTITY_NAME)

