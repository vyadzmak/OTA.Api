from models.db_models.models import PartnersCatalog, Attachments, Products
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import models.app_models.setting_models.setting_model as settings
import urllib.parse
from sqlalchemy import func, any_

# PARAMS
ENTITY_NAME = "Partners Catalog"
MODEL = PartnersCatalog
ROUTE = "/partnersCatalog"
END_POINT = "partners-catalog"

# NESTED SCHEMA FIELDS
default_image_data_partners = {
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
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'images': fields.List(fields.Integer),
    'description': fields.String(default=''),
    'short_description': fields.String(default=''),
    'default_image_id': fields.Integer,
    'default_image_data_partners': fields.Nested(default_image_data_partners),
    'images_data': fields.Nested(default_image_data_partners),
    'products_count': fields.Integer,
    'minimum_order_amount': fields.Float
}


# API METHODS FOR SINGLE ENTITY
class PartnersResource(Resource):
    def __init__(self):
        self.route = ROUTE + '/<int:id>'
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self, id):
        try:
            # session.autocommit = False
            # session.autoflush = False

            entity = session.query(MODEL).filter(MODEL.id == id).first()
            if not entity:
                abort(404, message=ENTITY_NAME + " {} doesn't exist".format(id))

            return entity
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update " + ENTITY_NAME)
        finally:
            pass
            # session.rollback()

    def delete(self, id):
        try:
            entity = session.query(MODEL).filter(MODEL.id == id).first()
            if not entity:
                abort(404, message=ENTITY_NAME + " {} doesn't exist".format(id))
            session.query(Products).filter(Products.partner_id == entity.id).update({Products.partner_id: None})
            session.commit()
            session.delete(entity)
            session.commit()
            session.query(Attachments).filter(Attachments.id.in_(entity.images)).delete(
                synchronize_session=False)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove " + ENTITY_NAME)

    @marshal_with(output_fields)
    def put(self, id):
        try:
            # session.autocommit = False
            # session.autoflush = False

            json_data = request.get_json(force=True)
            entity = session.query(MODEL).filter(MODEL.id == id).first()
            if not entity:
                abort(404, message=ENTITY_NAME + " {} doesn't exist".format(id))
            db_transformer.transform_update_params(entity, json_data)

            session.add(entity)
            session.commit()

            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update " + ENTITY_NAME)
        finally:
            pass
            # session.rollback()


# API METHODS FOR LIST ENTITIES
class PartnersListResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT + '-list'
        pass

    @marshal_with(output_fields)
    def get(self):
        try:
            # session.autocommit = False
            # session.autoflush = False

            entities = session.query(MODEL).order_by(MODEL.name).all()

            return entities
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update " + ENTITY_NAME)
        finally:
            pass
            # session.rollback()

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
            abort(400, message="Error while adding record " + ENTITY_NAME)
