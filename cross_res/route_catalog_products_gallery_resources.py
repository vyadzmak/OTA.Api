from models.db_models.models import Products, Attachments, Users
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import and_
import base64
import datetime
import models.app_models.setting_models.setting_model as settings
import urllib.parse
# PARAMS
ENTITY_NAME = "Route Catalog Products Gallery"
ROUTE = "/routeCatalogProductsGallery"
END_POINT = "route-catalog-products-gallery"

# NESTED SCHEMA FIELDS
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
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'gallery_images': fields.List(fields.Integer),
    'default_image_id': fields.Integer,
    'default_image_data':fields.Nested(default_image_data_products),
    'images_data': fields.Nested(default_image_data_products),

}


# API METHODS FOR SINGLE ENTITY
class RouteCatalogProductsGalleryResource(Resource):
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
            parser.add_argument('product_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            product_id = args['product_id']
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)

            # check login
            product = session.query(Products).filter(Products.id==product_id).first()

            if not product:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            entity = product
            if not entity:
                abort(404, message=ENTITY_NAME + " {} doesn't exist".format(id))
            api_url = settings.API_URL
            if hasattr(entity, 'default_image_data'):
                if (entity.default_image_data != None and entity.default_image_data.file_path != None):
                    entity.default_image_data.file_path = urllib.parse.urljoin(api_url,
                                                                               entity.default_image_data.file_path)
            if hasattr(entity, 'default_image_data'):
                if (entity.default_image_data != None and entity.default_image_data.thumb_file_path != None):
                    entity.default_image_data.thumb_file_path = urllib.parse.urljoin(api_url,
                                                                                     entity.default_image_data.thumb_file_path)
            if hasattr(entity, 'default_image_data'):
                if (entity.default_image_data != None and entity.default_image_data.optimized_size_file_path != None):
                    entity.default_image_data.optimized_size_file_path = urllib.parse.urljoin(api_url,
                                                                                              entity.default_image_data.optimized_size_file_path)

            entity.images_data = []

            if (entity.gallery_images != None and len(entity.gallery_images) > 0):
                for img_id in entity.gallery_images:
                    image = session.query(Attachments).filter(Attachments.id == img_id).first()
                    if not image:
                        continue
                    entity.images_data.append(image)

            return entity
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

