from models.db_models.models import ProductCategories, Products, ProductCategoryPositions
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.image_path_converter_modules.image_path_converter as image_path_converter
import copy

# PARAMS
ENTITY_NAME = "Products Categories by Product Category"
MODEL = ProductCategories
ROUTE = "/productsCategoriesByProductCategory"
END_POINT = "products-categories-by-product-category"

# NESTED SCHEMA FIELDS
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

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'default_image_id': fields.Integer,
    'default_image_data': fields.Nested(default_image_data_product_categories),

    'internal_categories_count': fields.Integer,
    'internal_products_count': fields.Integer
}


# API METHODS FOR SINGLE ENTITY
class ProductsCategoriesByProductCategoryResource(Resource):
    def get_to_all_categories(self, ids):

        result_ids = []

        for category_id in ids:
            product_categories = session.query(ProductCategories).filter(
                ProductCategories.parent_category_id == category_id).all()

            if (not product_categories):
                continue
            for p_cat in product_categories:
                result_ids.append(p_cat.id)

        if (len(result_ids) != 0):
            self.get_to_all_categories(result_ids)
        else:
            self.x_res = ids

    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        self.x_res = []
        pass

    @marshal_with(output_fields)
    def get(self):
        try:

            action_type = 'GET'
            parser = reqparse.RequestParser()
            parser.add_argument('user_id')
            parser.add_argument('category_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            category_id = args['category_id']
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)
            product_categories = session.query(ProductCategories).filter(
                ProductCategories.parent_category_id == category_id,
                ProductCategories.is_delete == False).all()
            if not product_categories:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            # product_categories = copy.deepcopy(product_categories)

            for category in product_categories:
                res_ids = []
                res_ids.append(category.id)
                category.internal_products_count = 0
                self.get_to_all_categories(res_ids)
                for x_cat in self.x_res:
                    products = session.query(Products).filter(Products.category_id == x_cat,
                                                              Products.is_delete == False).all()

                    if (not products):
                        continue
                    category.internal_products_count += len(products)
                    pass

                # if (category.default_image_data!=None):
                #     image_path_converter.convert_path(category.default_image_data)
                sub_cats = session.query(ProductCategories).filter(ProductCategories.parent_category_id == category.id,
                                                                   ProductCategories.is_delete == False).all()
                if (not sub_cats):
                    continue
                category.internal_categories_count = len(sub_cats)

            product_category_position = session.query(ProductCategoryPositions) \
                .filter(ProductCategoryPositions.parent_category_id == category_id).first()
            if product_category_position is not None:
                positioned_categories = {x: x for x in product_category_position.child_category_positions}
                other_categories = []
                for cat in product_categories:
                    if cat.id in product_category_position.child_category_positions:
                        positioned_categories[cat.id] = cat
                    else:
                        other_categories.append(cat)
                product_categories = list(positioned_categories.values()) + other_categories

            return product_categories
        except Exception as e:
            if (hasattr(e, 'data')):
                if (e.data != None and "message" in e.data):
                    abort(400, message=e.data["message"])
            abort(400, message="Неопознанная ошибка")
            # finally:
            #     pass
            #     #session.rollback()
