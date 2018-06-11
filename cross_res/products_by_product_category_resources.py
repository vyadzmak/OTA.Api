from models.db_models.models import ProductCategories
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging

#PARAMS
ENTITY_NAME = "Products by Product Category"
MODEL = ProductCategories
ROUTE ="/productsCategoriesByProductCategory"
END_POINT = "products-categories-by-product-category"

#NESTED SCHEMA FIELDS
default_image_data_product_categories = {
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
    'default_image_id': fields.Integer,
    'default_image_data':fields.Nested(default_image_data_product_categories),

    'internal_categories_count':fields.Integer
}



#API METHODS FOR SINGLE ENTITY
class ProductsCategoriesByProductCategoryResource(Resource):
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
            parser.add_argument('category_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            category_id = args['category_id']
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)
            product_categories = session.query(ProductCategories).filter(ProductCategories.parent_category_id==category_id).all()
            if not product_categories:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            for category in product_categories:
                sub_cats = session.query(ProductCategories).filter(ProductCategories.parent_category_id==category_id).all()
                if (not sub_cats):
                    continue
                category.internal_categories_count = len(sub_cats)

            return product_categories
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")



