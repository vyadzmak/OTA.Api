from models.db_models.models import UserCarts,UserCartPositions,Products,CurrencyCatalog, Orders
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.image_path_converter_modules.image_path_converter as image_path_converter
#PARAMS
ENTITY_NAME = "Make Users Order"
MODEL = Orders
ROUTE ="/makeUserOrder"
END_POINT = "make-user-order"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'status_code': fields.Integer,

}
#API METHODS FOR SINGLE ENTITY
class MakeUserOrderResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def post(self):
        try:

            action_type='POST'
            json_data = request.get_json(force=True)

            user_cart_id = json_data['user_cart_id']
            address_id = json_data['user_address_id']

            user_cart = session.query(UserCarts).filter(UserCarts.id==user_cart_id).first()



            if (not user_cart):
                abort(400, message = "Корзина не найдена")

            user_cart_positions = session.query(UserCartPositions).filter(
                UserCartPositions.user_cart_id == user_cart.id).all()

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




            order_args ={}
            order_args["user_id"] = user_cart.user_id
            order_args["amount"] = total_sum_without_discount
            order_args["amount_discount"] = amount_sum
            order_args["total_amount"] = total_sum
            order_args["client_address_id"] = address_id
            order_args["currency_id"] = currency_id

            order_entity = Orders(order_args)
            session.add(order_entity)
            session.commit()

            start_position = 1000000000

            order_number = start_position+order_entity











            response = {
                'status_code': 200
            }
            return response

        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")



