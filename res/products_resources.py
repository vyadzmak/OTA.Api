from models.db_models.models import Products,Attachments
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import models.app_models.setting_models.setting_model as settings
import urllib.parse
#PARAMS
ENTITY_NAME = "Products"
MODEL = Products
ROUTE ="/products"
END_POINT = "products"

#NESTED SCHEMA FIELDS
default_image_data_products = {
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

product_recomendations_fields = {
    'id': fields.Integer,
    'name':fields.String,
    'category_id':fields.Integer,
    'product_code':fields.String,
    'amount':fields.Float,
}
#OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'name':fields.String,
    'category_id':fields.Integer,
    'user_creator_id':fields.Integer,
    'creation_date':fields.DateTime,
    'gallery_images': fields.List(fields.Integer),
    'product_recomendations': fields.List(fields.Integer),
    'full_description': fields.String,
    'short_description': fields.String,
    'product_code':fields.String,
    'amount':fields.Float,
    'discount_amount':fields.Float,
    'unit_value':fields.Float,
    'is_stock_product':fields.Boolean,
    'is_discount_product':fields.Boolean,
    'not_available':fields.Boolean,
    'not_show_in_catalog':fields.Boolean,
    'stock_text':fields.String,
    'brand_id':fields.Integer,
    'partner_id':fields.Integer,
    'currency_id': fields.Integer,
    'unit_id': fields.Integer,
    'default_image_id': fields.Integer,
    'default_image_data':fields.Nested(default_image_data_products),
    'images_data':fields.Nested(default_image_data_products),
    'product_recomendations_data':fields.Nested(product_recomendations_fields),
    'recommended_amount':fields.Float,
    'bonus_percent':fields.Float
}


#API METHODS FOR SINGLE ENTITY
class ProductsResource(Resource):
    def __init__(self):
        self.route = ROUTE+'/<int:id>'
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self, id):
        # session.autocommit = False
        # session.autoflush = False

        entity = session.query(MODEL).filter(MODEL.id == id).first()
        if not entity:
            abort(404, message=ENTITY_NAME+" {} doesn't exist".format(id))
        # api_url = settings.API_URL
        # if hasattr(entity, 'default_image_data'):
        #     if (entity.default_image_data != None and entity.default_image_data.file_path != None):
        #         entity.default_image_data.file_path = urllib.parse.urljoin(api_url, entity.default_image_data.file_path)
        # if hasattr(entity, 'default_image_data'):
        #     if (entity.default_image_data != None and entity.default_image_data.thumb_file_path != None):
        #         entity.default_image_data.thumb_file_path = urllib.parse.urljoin(api_url,
        #                                                                          entity.default_image_data.thumb_file_path)
        # if hasattr(entity, 'default_image_data'):
        #     if (entity.default_image_data != None and entity.default_image_data.optimized_size_file_path != None):
        #         entity.default_image_data.optimized_size_file_path = urllib.parse.urljoin(api_url,
        #                                                                                   entity.default_image_data.optimized_size_file_path)

        entity.images_data =[]

        if (entity.gallery_images!=None and len(entity.gallery_images)>0):
                for img_id in entity.gallery_images:
                    image =session.query(Attachments).filter(Attachments.id== img_id).first()
                    if not image:
                        continue
                    entity.images_data.append(image)

        entity.product_recomendations_data=[]
        if (entity.product_recomendations!=None and len(entity.product_recomendations)>0):
            for rec_id in entity.product_recomendations:
                recomendation = session.query(Products).filter(Products.id==rec_id).first()
                if not recomendation:
                    continue

                entity.product_recomendations_data.append(recomendation)

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
            # session.autocommit = False
            # session.autoflush = False

            json_data = request.get_json(force=True)
            entity = session.query(MODEL).filter(MODEL.id == id).first()
            if not entity:
                abort(404, message=ENTITY_NAME + " {} doesn't exist".format(id))
            db_transformer.transform_update_params(entity,json_data)


            session.add(entity)
            session.commit()
            # api_url = settings.API_URL
            # if hasattr(entity, 'default_image_data'):
            #     if (entity.default_image_data != None and entity.default_image_data.file_path != None):
            #         entity.default_image_data.file_path = urllib.parse.urljoin(api_url,
            #                                                                    entity.default_image_data.file_path)
            # if hasattr(entity, 'default_image_data'):
            #     if (entity.default_image_data != None and entity.default_image_data.thumb_file_path != None):
            #         entity.default_image_data.thumb_file_path = urllib.parse.urljoin(api_url,
            #                                                                          entity.default_image_data.thumb_file_path)
            # if hasattr(entity, 'default_image_data'):
            #     if (entity.default_image_data != None and entity.default_image_data.optimized_size_file_path != None):
            #         entity.default_image_data.optimized_size_file_path = urllib.parse.urljoin(api_url,
            #                                                                                   entity.default_image_data.optimized_size_file_path)

            entity.images_data = []

            if (entity.gallery_images != None and len(entity.gallery_images) > 0):
                for img_id in entity.gallery_images:
                    image = session.query(Attachments).filter(Attachments.id == img_id).first()
                    if not image:
                        continue
                    entity.images_data.append(image)
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update "+ENTITY_NAME)
        finally:
            pass
            #session.rollback()


#API METHODS FOR LIST ENTITIES
class ProductsListResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT+'-list'
        pass

    @marshal_with(output_fields)
    def get(self):
        try:
            # session.autocommit = False
            # session.autoflush = False

            entities = session.query(MODEL).all()
            for entity in entities:
                entity.images_data = []
                api_url = settings.API_URL
                # if hasattr(entity, 'default_image_data'):
                #     if (entity.default_image_data != None and entity.default_image_data.file_path != None):
                #         entity.default_image_data.file_path = urllib.parse.urljoin(api_url,
                #                                                                    entity.default_image_data.file_path)
                # if hasattr(entity, 'default_image_data'):
                #     if (entity.default_image_data != None and entity.default_image_data.thumb_file_path != None):
                #         entity.default_image_data.thumb_file_path = urllib.parse.urljoin(api_url,
                #                                                                          entity.default_image_data.thumb_file_path)
                # if hasattr(entity, 'default_image_data'):
                #     if (entity.default_image_data != None and entity.default_image_data.optimized_size_file_path != None):
                #         entity.default_image_data.optimized_size_file_path = urllib.parse.urljoin(api_url,
                #                                                                                   entity.default_image_data.optimized_size_file_path)

                if (entity.gallery_images!=None and len(entity.gallery_images) > 0):
                    for img_id in entity.gallery_images:
                        image = session.query(Attachments).filter(Attachments.id == img_id).first()
                        if not image:
                            continue
                        entity.images_data.append(image)
            return entities
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update " + ENTITY_NAME)
        finally:
            pass

            #session.rollback()

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

