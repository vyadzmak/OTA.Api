from models.db_models.models import Users, UserLogins,UserInfo,UserCarts,UserCartPositions,Products,CurrencyCatalog
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.image_path_converter_modules.image_path_converter as image_path_converter
from sqlalchemy import and_
#PARAMS
ENTITY_NAME = "User Cart Product Count"
MODEL = Users
ROUTE ="/userCartProductCount"
END_POINT = "user-cart-product-details"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'product_count': fields.Integer,
}

#API METHODS FOR SINGLE ENTITY
class UserCartProductCountResource(Resource):
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
            parser.add_argument('user_cart_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            product_id = args['product_id']
            user_cart_id = args['user_cart_id']
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)

            products = session.query(UserCartPositions).filter(and_(
                UserCartPositions.product_id==product_id,
                UserCartPositions.user_cart_id==user_cart_id)).first()
            if (not products):
                response = {'product_count':1}
                return  response

            response = {'product_count':int(products.count)}


            return response
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")



