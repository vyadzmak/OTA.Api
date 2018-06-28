from models.db_models.models import Users, UserLogins,UserInfo,UserCarts,UserCartPositions,Products,CurrencyCatalog
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.image_path_converter_modules.image_path_converter as image_path_converter
#PARAMS
ENTITY_NAME = "Users Cart Details"
MODEL = Users
ROUTE ="/userCartDetails"
END_POINT = "user-cart-details"

# NESTED SCHEMA FIELDS
currency_data_fields = {
    'id': fields.Integer,
    'system_name': fields.String,
    'display_value': fields.String,
    'name': fields.String,
    'is_default': fields.Boolean
}

unit_data_fields = {
    'id': fields.Integer,
    'system_name': fields.String,
    'display_value': fields.String,
    'name': fields.String,
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

product_data_fields ={
    'id': fields.Integer,
    'name': fields.String,
    'category_id': fields.Integer,
    'user_creator_id': fields.Integer,
    'creation_date': fields.DateTime,
    'full_description': fields.String,
    'short_description': fields.String,
    'product_code': fields.String,
    'amount': fields.Float,
    'discount_amount': fields.Float,
    'unit_value': fields.Float,
    'is_stock_product': fields.Boolean,
    'is_discount_product': fields.Boolean,
    'not_available': fields.Boolean,
    'not_show_in_catalog': fields.Boolean,
    'stock_text': fields.String,
    'brand_id': fields.Integer,
    'partner_id': fields.Integer,
    'currency_id': fields.Integer,
    'unit_id': fields.Integer,
    'default_image_id': fields.Integer,
    'default_image_data': fields.Nested(default_image_data_products),
    'comments_count': fields.Integer,
    'rate': fields.Float,
    'product_unit_data': fields.Nested(unit_data_fields),
    'product_currency_data': fields.Nested(currency_data_fields),

}

user_cart_positions_fields ={
    'id': fields.Integer,
    'product_id': fields.Integer,
    'count': fields.Float,
    'need_invoice': fields.Boolean,
    'description': fields.String,
    'user_cart_id':fields.Integer,
    'user_cart_position_product_data':fields.Nested(product_data_fields)
}

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,

    'cart_state_id':fields.Integer,
    'products_count': fields.Integer,
    'total_amount': fields.Float,
    'total_amount_without_discount': fields.Float,
    'discount_amount':fields.Float,
    'currency_data': fields.Nested(currency_data_fields),
    'economy_delta': fields.Float,
    'economy_percent': fields.Float,
    'cart_positions': fields.Nested(user_cart_positions_fields),

}

#API METHODS FOR SINGLE ENTITY
class UserCartDetailsResource(Resource):
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
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            user_cart_id = args['user_cart_id']
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)

            user_cart = session.query(UserCarts).filter(UserCarts.id==user_cart_id).first()
            if not user_cart:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            user_cart_positions = session.query(UserCartPositions).filter(UserCartPositions.user_cart_id==user_cart.id).all()
            # for cart_position in cart_positions:
            #     cart_position

            user_cart.cart_positions = user_cart_positions
            total_sum = 0
            total_sum_without_discount = 0

            amount_sum = 0
            currency_id = -1
            for cart_position in user_cart_positions:
                count = cart_position.count

                product = session.query(Products).filter(Products.id == cart_position.product_id).first()
                if (currency_id == -1):
                    currency_id = product.currency_id

                if (not product):
                    continue
                single_amount = 0
                if (product.is_discount_product == True):
                    discount_amount = product.discount_amount

                    if (discount_amount == 0):
                        discount_amount = product.amount

                    single_amount = round(discount_amount * count, 2)
                    total_sum += single_amount
                    total_sum_without_discount += round(product.amount * count, 2)

                    delta = product.amount - discount_amount

                    amount_sum += round(delta * count, 2)

                else:
                    total_sum += round(product.amount * count, 2)

            economy_delta = total_sum_without_discount - amount_sum
            economy_percent = round(100 * (economy_delta / total_sum_without_discount), 2)

            user_cart.total_amount = total_sum
            user_cart.total_amount_without_discount = total_sum_without_discount
            user_cart.discount_amount = amount_sum
            user_cart.economy_delta = economy_delta
            user_cart.economy_percent = economy_percent
            user_cart.products_count = len(user_cart_positions)
            user_cart.currency_data = session.query(CurrencyCatalog).filter(CurrencyCatalog.id == currency_id).first()

            return user_cart

        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")



