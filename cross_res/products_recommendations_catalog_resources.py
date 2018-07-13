from models.db_models.models import Products, Log, Users,ViewSettings
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import and_
import base64
import datetime

# PARAMS
ENTITY_NAME = "Products Recommendations Catalog"
ROUTE = "/productsRecommendationsCatalog"
END_POINT = "products-recommendations-catalog"

# NESTED SCHEMA FIELDS
category_fields = {
    'id': fields.Integer,
    'name':fields.String
}
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'name':fields.String,
    'product_code':fields.String,
    'is_recommend':fields.Boolean,
}


# API METHODS FOR SINGLE ENTITY
class ProductsRecommendationsCatalogResource(Resource):
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

            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)
            # product = session.query(Products).filter(Products.id==product_id).first()
            t=0

            products = session.query(Products).all()

            if not products:
                abort(400, message='Ошибка получения данных. Данные не найдены')


            settings = session.query(ViewSettings).first()

            if (not settings):
                return Products

            recommendations =settings.recomendation_elements


            if (len(recommendations)>0):
                for pr in products:
                    p_id = pr.id
                    if ((p_id in recommendations)==True):
                        pr.is_recommend = True
                    else:
                        pr.is_recommend=False

            return products
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

