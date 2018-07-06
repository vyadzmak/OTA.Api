from models.db_models.models import Products, ProductComments
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import desc
#PARAMS
ENTITY_NAME = "Products by Product Category"
MODEL = Products
ROUTE ="/productsByProductCategory"
END_POINT = "products-by-product-category"

#NESTED SCHEMA FIELDS
currency_data_fields = {
    'id': fields.Integer,
    'system_name':fields.String,
    'display_value':fields.String,
    'name':fields.String,
    'is_default': fields.Boolean
}

unit_data_fields = {
    'id': fields.Integer,
    'system_name':fields.String,
    'display_value':fields.String,
    'name':fields.String,
    'is_default': fields.Boolean
}

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

#OUTPUT SCHEMA
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
    'default_image_id': fields.Integer,
    'default_image_data':fields.Nested(default_image_data_products),
    'comments_count':fields.Integer,
    'rate':fields.Float,
    'product_unit_data':fields.Nested(unit_data_fields),
    'product_currency_data':fields.Nested(currency_data_fields),
    'recommended_amount':fields.Float,
    'bonus_percent':fields.Float

}



#API METHODS FOR SINGLE ENTITY
class ProductsByProductCategoryResource(Resource):
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
            products = session.query(Products).filter(Products.category_id==category_id).order_by(desc(Products.id)).all()
            #products = products.
            if not products:
                abort(400, message='Ошибка получения данных. Данные не найдены')
            for product in products:
                comments = session.query(ProductComments).filter(ProductComments.product_id==product.id and ProductComments.is_delete==False).all()
                product.comments_count = 0
                product.rate = 0
                if (not comments):

                    continue
                total_rate =0
                comments_count=0
                for comment in comments:
                    total_rate+=comment.rate
                    comments_count+=1

                if (comments_count>0):
                    product.comments_count =comments_count
                    product.rate =round((total_rate/comments_count),2)

            #products.internal_products_count = len(products)

            return products
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")
        finally:
            pass
            #session.rollback()


