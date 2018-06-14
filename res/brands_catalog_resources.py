from models.db_models.models import BrandsCatalog,Attachments
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import models.app_models.setting_models.setting_model as settings
import urllib.parse
#PARAMS
ENTITY_NAME = "Brands Catalog"
MODEL = BrandsCatalog
ROUTE ="/brandsCatalog"
END_POINT = "brands-catalog"

#NESTED SCHEMA FIELDS
default_image_data_brands = {
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
#OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'name':fields.String,
    'images': fields.List(fields.Integer),
    'description': fields.String,
    'short_description': fields.String,
    'default_image_id': fields.Integer,
    'default_image_data_brands':fields.Nested(default_image_data_brands),
    'images_data':fields.Nested(default_image_data_brands)
}


#API METHODS FOR SINGLE ENTITY
class BrandsResource(Resource):
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

            if (entity.images!=None and len(entity.images)>0):
                    for img_id in entity.images:
                        image =session.query(Attachments).filter(Attachments.id== img_id).first()
                        if not image:
                            continue
                        entity.images_data.append(image)
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

            #api_url = settings.API_URL
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
            #
            entity.images_data = []

            if (entity.images != None and len(entity.images) > 0):
                for img_id in entity.images:
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
class BrandsListResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT+'-list'
        pass

    @marshal_with(output_fields)
    def get(self):
        try:
            entities = session.query(MODEL).all()
            # session.autocommit = False
            # session.autoflush = False

            for entity in entities:
                entity.images_data = []

                if (entity.images!=None and len(entity.images) > 0):
                    for img_id in entity.images:
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

