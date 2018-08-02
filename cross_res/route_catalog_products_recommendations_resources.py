from models.db_models.models import Products, Log, Users
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import and_
import base64
import datetime

# PARAMS
ENTITY_NAME = "Route Catalog Products Recommendations"
ROUTE = "/routeCatalogProductsRecommendations"
END_POINT = "route-catalog-products-recommendations"

# NESTED SCHEMA FIELDS
category_fields = {
    'id': fields.Integer,
    'name': fields.String
}
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'category_id': fields.Integer,
    'user_creator_id': fields.Integer,
    'product_code': fields.String,
    'is_recommend': fields.Boolean,
    # 'product_category_data':fields.Nested(category_fields)
}


# API METHODS FOR SINGLE ENTITY
class RouteCatalogProductsRecommendationsResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self):
        try:
            action_type = 'GET'
            parser = reqparse.RequestParser()
            parser.add_argument('user_id')
            parser.add_argument('product_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            product_id = args['product_id']
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)
            product = session.query(Products).filter(Products.id == product_id).first()
            t = 0

            products = session.query(Products).filter(Products.id != product_id, Products.is_delete == False).all()

            if not products:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            if (not product):
                return products

            recommendations = product.product_recomendations

            if (not recommendations):
                # если у продукта нет рекомендаций то выводим весь список товаров
                rec_products = session.query(Products).filter(Products.id != product_id, Products.is_delete == False).all()
                for r_product in rec_products:
                    r_product.is_recommend = False

                return rec_products

            if (len(recommendations) > 0):
                for pr in products:
                    p_id = pr.id
                    if ((p_id in recommendations) == True):
                        pr.is_recommend = True
                    else:
                        pr.is_recommend = False

            return products
        except Exception as e:
            if (hasattr(e, 'data')):
                if (e.data != None and "message" in e.data):
                    abort(400, message=e.data["message"])
            abort(400, message="Неопознанная ошибка")
