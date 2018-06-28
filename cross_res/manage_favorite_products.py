from models.db_models.models import UserFavoriteProducts
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer

from sqlalchemy import and_
import base64
import datetime
from sqlalchemy import desc
# PARAMS
ENTITY_NAME = "Manage Favorite Products"
ROUTE = "/manageFavoriteProducts"
END_POINT = "manage-favorite-products"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'status_code': fields.Integer,

}


# API METHODS FOR SINGLE ENTITY
class ManageFavoriteProductsResource(Resource):
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
            parser.add_argument('value')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            product_id = int(args['product_id'])
            value = (args['value'])
            if (value=='False' or value=='false'):
                value =False
            else:
                value = True
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)

            favorite_products = session.query(UserFavoriteProducts).filter(UserFavoriteProducts.user_id==user_id).first()

            response = {
                'status_code': 200
            }

            if (not favorite_products):
                favorite_products_args = {}
                favorite_products_args["user_id"] =user_id
                favorite_products_args["products_ids"] =[product_id]
                favorite_products_entity = UserFavoriteProducts(favorite_products_args)
                session.add(favorite_products_entity)
                session.commit()
                return response

            favorite_products_ids = favorite_products.products_ids
            if (value==True):
                if ((product_id in favorite_products_ids)==False):
                    favorite_products_ids.append(product_id)
            else:
                arr =[]
                for p_id in favorite_products_ids:
                    if (p_id!=product_id):
                        arr.append(p_id)

                favorite_products_ids = arr


            # f_args ={}
            # f_args["products_ids"] = [favorite_products_ids]

            # favorite_products = session.query(UserFavoriteProducts).filter(UserFavoriteProducts.user_id==user_id).first()

            # db_transformer.transform_update_params(favorite_products, f_args)
            # favorite_products.products_ids=[]
            # session.add(favorite_products)
            # session.commit()

            output = map(int, favorite_products_ids)
            favorite_products.products_ids = output

            # setattr(favorite_products,'products_ids',favorite_products_ids)
            session.add(favorite_products)
            session.commit()




            return response
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

