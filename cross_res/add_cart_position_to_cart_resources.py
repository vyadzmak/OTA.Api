from models.db_models.models import UserCarts, UserCartPositions, Products,CurrencyCatalog
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.image_path_converter_modules.image_path_converter as image_path_converter
import uuid
from sqlalchemy import and_
#PARAMS
ENTITY_NAME = "Add Cart Position To Cart"
MODEL = UserCarts
ROUTE ="/addCartPositionToCart"
END_POINT = "add-cart-position-to-cart"

# NESTED SCHEMA FIELDS
currency_data_fields = {
    'id': fields.Integer,
    'system_name':fields.String,
    'display_value':fields.String,
    'name':fields.String,
    'is_default': fields.Boolean
}
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'user_id': fields.String,
    'cart_state_id':fields.Integer,
    'products_count': fields.Integer,
    'total_amount': fields.Float,
    'total_amount_without_discount': fields.Float,
    'discount_amount':fields.Float,
    'currency_data': fields.Nested(currency_data_fields),
    'economy_delta': fields.Float,
    'economy_percent': fields.Float

}

#API METHODS FOR SINGLE ENTITY
class AddCartPositionToCartResource(Resource):
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
            parser.add_argument('user_cart_id')
            parser.add_argument('product_id')
            parser.add_argument('count')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = int(args['user_id'])
            user_cart_id =int(args['user_cart_id'])
            product_id = int(args['product_id'])
            count = float(args['count'])


            user_action_logging.log_user_actions(ROUTE,user_id, action_type)
            user_cart ={}
            if (user_cart_id==-1):
                user_cart_args = {}
                user_cart_args["user_id"] = user_id
                user_cart_entity= UserCarts(user_cart_args)
                session.add(user_cart_entity)
                session.commit()
                user_cart = user_cart_entity
            else:
                user_cart =session.query(UserCarts).filter(UserCarts.id==user_cart_id).first()

                if (not user_cart):
                    user_cart_args = {}
                    user_cart_args["user_id"] = user_id
                    user_cart_entity = UserCarts(user_cart_args)
                    session.add(user_cart_entity)
                    session.commit()
                    user_cart = user_cart_entity


            #check if cart positions contains current product



            check_user_cart_positions =session.query(UserCartPositions).filter(and_(
                UserCartPositions.user_cart_id==user_cart.id,
                UserCartPositions.product_id==product_id
            )) .first()


            if (not check_user_cart_positions):
                user_cart_position_args = {}
                user_cart_position_args['product_id'] = product_id
                user_cart_position_args['user_cart_id'] = user_cart.id
                user_cart_position_args['count'] = count
                user_cart_position_args['temp_cart_uid'] = str(uuid.uuid4().hex)
                user_cart_position_args['need_invoice'] = False
                user_cart_position_entity = UserCartPositions(user_cart_position_args)
                session.add(user_cart_position_entity)
                session.commit()
            else:

                check_user_cart_positions.count = count
                session.add(check_user_cart_positions)
                session.commit()




            #calculte total sum
            user_cart_positions = session.query(UserCartPositions).filter(UserCartPositions.user_cart_id==user_cart.id).all()
            total_sum = 0
            total_sum_without_discount = 0

            amount_sum = 0
            currency_id =-1
            for cart_position in user_cart_positions:
                count = cart_position.count

                product = session.query(Products).filter(Products.id==cart_position.product_id).first()
                if (currency_id==-1):
                    currency_id = product.currency_id



                if (not product):
                    continue
                single_amount =0
                if (product.is_discount_product==True):
                    discount_amount = product.discount_amount

                    if (discount_amount==0):
                        discount_amount = product.amount


                    single_amount = round(discount_amount*count,2)
                    total_sum+=single_amount
                    total_sum_without_discount+=round(product.amount*count,2)

                    delta = product.amount-discount_amount

                    amount_sum+=round(delta*count,2)

                else:
                    total_sum+=round(product.amount*count,2)
                    total_sum_without_discount+=round(product.amount*count,2)

            economy_delta = total_sum_without_discount-amount_sum
            economy_percent =round(100*(economy_delta/total_sum_without_discount),2)


            user_cart.total_amount = total_sum
            user_cart.total_amount_without_discount = total_sum_without_discount
            user_cart.discount_amount = amount_sum
            user_cart.economy_delta = economy_delta
            user_cart.economy_percent = economy_percent
            user_cart.products_count = len(user_cart_positions)
            user_cart.currency_data = session.query(CurrencyCatalog).filter(CurrencyCatalog.id==currency_id).first()

            return user_cart

        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")



