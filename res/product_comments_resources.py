from models.db_models.models import ProductComments
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import models.app_models.setting_models.setting_model as settings
import urllib.parse
#PARAMS
ENTITY_NAME = "Product Comments"
MODEL = ProductComments
ROUTE ="/productComments"
END_POINT = "product-comments"

#NESTED SCHEMA FIELDS
user_data_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name")
}

product_data_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name")
}
#OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'user_id':fields.Integer,
    'creation_date': fields.DateTime,
    'comment_text':fields.String,
    'rate':fields.Float,
    'is_delete':fields.Boolean,
    'product_id':fields.Integer,
    'comment_user_data':fields.Nested(user_data_fields),
    'comment_product_data': fields.Nested(product_data_fields),
}


#API METHODS FOR SINGLE ENTITY
class ProductCommentsResource(Resource):
    def __init__(self):
        self.route = ROUTE+'/<int:id>'
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self, id):
        entity = session.query(MODEL).filter(MODEL.id == id).first()

        return entity

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
class ProductCommentsListResource(Resource):
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

