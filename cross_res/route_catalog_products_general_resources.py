from models.db_models.models import Products, Log, Users
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import and_
import base64
import datetime

# PARAMS
ENTITY_NAME = "Route Catalog Products General"
ROUTE = "/routeCatalogProductsGeneral"
END_POINT = "route-catalog-products-general"

# NESTED SCHEMA FIELDS
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
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'name':fields.String,
    'category_id':fields.Integer,
    'user_creator_id':fields.Integer,
    'creation_date':fields.DateTime,
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
    'gallery_images': fields.List(fields.Integer),
    'product_recomendations': fields.List(fields.Integer),
    'default_image_id': fields.Integer,
    'default_image_data':fields.Nested(default_image_data_products),
    'recommended_amount':fields.Float,
    'bonus_percent':fields.Float,
    'alt_amount': fields.Float,
    'alt_unit_value': fields.Float,
    'alt_unit_id': fields.Integer,
    'alt_discount_amount': fields.Float
}


# API METHODS FOR SINGLE ENTITY
class RouteCatalogProductsGeneralResource(Resource):
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

            return product
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

