from models.db_models.models import ProductCategories,Products
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.image_path_converter_modules.image_path_converter as image_path_converter
import copy
#PARAMS
ENTITY_NAME = "Category List Without Products"
MODEL = ProductCategories
ROUTE ="/categoryListWithoutProducts"
END_POINT = "category-list-without-products"

#NESTED SCHEMA FIELDS

#OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'name':fields.String,
}



#API METHODS FOR SINGLE ENTITY
class CategoryListWithoutProductsResource(Resource):

    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        self.x_res =[]
        pass


    @marshal_with(output_fields)
    def get(self):
        try:


            action_type='GET'
            parser = reqparse.RequestParser()
            parser.add_argument('user_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']

            user_action_logging.log_user_actions(ROUTE,user_id, action_type)
            product_categories = session.query(ProductCategories).filter(ProductCategories.is_delete == False).all()
            if not product_categories:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            categories_without_products =[]

            for product_category in product_categories:
                product = session.query(Products).filter(Products.category_id==product_category.id).first()

                if (product==None):
                    categories_without_products.append(product_category)



            return categories_without_products
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")
        # finally:
        #     pass
        #     #session.rollback()


