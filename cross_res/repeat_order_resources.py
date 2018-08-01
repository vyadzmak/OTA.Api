from models.db_models.models import Orders,OrderPositions,UserCarts,UserCartPositions
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.image_path_converter_modules.image_path_converter as image_path_converter
from sqlalchemy import and_
import uuid
#PARAMS
ENTITY_NAME = "Repeat Order"
MODEL = Orders
ROUTE ="/repeatOrder"
END_POINT = "repeat-order"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'cart_id': fields.Integer,
}

#API METHODS FOR SINGLE ENTITY
class RepeatOrderResource(Resource):
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
            parser.add_argument('order_id')
            parser.add_argument('user_cart_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = int(args['user_id'])
            order_id = int(args['order_id'])
            user_cart_id = int(args['user_cart_id'])
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)

            old_order = session.query(Orders).filter(Orders.id==order_id).first()

            if (not old_order):
                abort(400, message="Order not found")

            old_order_positions = session.query(OrderPositions).filter(OrderPositions.order_id==old_order.id).all()

            if (not old_order_positions):
                abort(400, message="Order positions not found")

            user_cart = {}
            if (user_cart_id == -1):
                user_cart_args = {}
                user_cart_args["user_id"] = user_id
                user_cart_entity = UserCarts(user_cart_args)
                session.add(user_cart_entity)
                session.commit()
                user_cart = user_cart_entity
            else:
                user_cart = session.query(UserCarts).filter(UserCarts.id == user_cart_id).first()

            for old_position in old_order_positions:
                user_cart_position_args = {}
                user_cart_position_args['product_id'] = old_position.product_id
                user_cart_position_args['user_cart_id'] = user_cart.id
                user_cart_position_args['count'] = old_position.count
                user_cart_position_args['temp_cart_uid'] = str(uuid.uuid4().hex)
                user_cart_position_args['need_invoice'] =old_position.need_invoice
                user_cart_position_args['alt_count'] =old_position.alt_count
                user_cart_position_entity = UserCartPositions(user_cart_position_args)
                session.add(user_cart_position_entity)
                session.commit()

                pass



            response = {'cart_id':user_cart.id}


            return response
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")



