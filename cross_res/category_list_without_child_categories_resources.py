from models.db_models.models import ProductCategories,Products
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.image_path_converter_modules.image_path_converter as image_path_converter
import copy
#PARAMS
ENTITY_NAME = "Category List Without Child Categories"
MODEL = ProductCategories
ROUTE ="/categoryListWithoutChildCategories"
END_POINT = "category-list-without-child-categories"

#NESTED SCHEMA FIELDS

#OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'name':fields.String,
}



#API METHODS FOR SINGLE ENTITY
class CategoryListWithoutChildCategoriesResource(Resource):

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
            product_categories = session.query(ProductCategories).all()
            if not product_categories:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            categories_without_childs =[]

            for product_category in product_categories:
                category = session.query(ProductCategories).filter(ProductCategories.parent_category_id==product_category.id).first()

                if (category==None):
                    categories_without_childs.append(product_category)



            return categories_without_childs
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")
        # finally:
        #     pass
        #     #session.rollback()


