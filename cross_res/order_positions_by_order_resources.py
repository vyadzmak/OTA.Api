from models.db_models.models import OrderPositions
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import and_
import base64
import datetime
from sqlalchemy import desc

# PARAMS
ENTITY_NAME = "Order Positions By Order"
ROUTE = "/orderPositionsByOrders"
END_POINT = "order-positions-by-order"

# NESTED SCHEMA FIELDS
product_data_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'category_id': fields.Integer,
    'product_code': fields.String,
    'is_stock_product': fields.Boolean,
    'amount': fields.Float,
    'alt_amount': fields.Float,
    'discount_amount': fields.Float,
    'alt_discount_amount': fields.Float,
    'unit_display_value': fields.String(
        attribute=lambda x: x.product_unit_data.display_value if x.product_unit_data else ''),
    'alt_unit_display_value': fields.String(
        attribute=lambda x: x.product_alt_unit_data.display_value if x.product_alt_unit_data else ''),
    'currency_display_value': fields.String(
        attribute=lambda x: x.product_currency_data.display_value if x.product_currency_data else ''),
    'partner_name': fields.String(
        attribute=lambda x: x.partner_data.name if x.partner_data else '')
}

order_data_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'creation_date': fields.DateTime,
    'number': fields.String,
    'executor_id': fields.Integer,
    'processed_date': fields.DateTime,
    'execute_date': fields.DateTime,
    'amount': fields.Float,
    'amount_discount': fields.Float,
    'total_amount': fields.Float
}

order_position_states_data = {
    'id': fields.Integer,
    'name': fields.String,
    'title': fields.String
}
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'product_id': fields.Integer,
    'order_id': fields.Integer,
    'count': fields.Float,
    'alt_count': fields.Float,
    'description': fields.String,
    'need_invoice': fields.Boolean,
    'order_position_state_id': fields.Integer,
    'amount_per_item': fields.Float,
    'alt_amount_per_item': fields.Float,
    'amount_per_item_discount': fields.Float,
    'alt_amount_per_item_discount': fields.Float,
    'total_amount': fields.Float,

    'product_data': fields.Nested(product_data_fields),
    # 'order_data':fields.Nested(order_data_fields),
    'order_position_states': fields.Nested(order_position_states_data),
    'bonuses': fields.Float

}


# API METHODS FOR SINGLE ENTITY
class OrderPositionsByOrderResource(Resource):
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
            parser.add_argument('order_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            order_id = int(args['order_id'])
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)
            orderPositions = session.query(OrderPositions).filter(OrderPositions.order_id == order_id).order_by(
                desc(OrderPositions.id)).all()

            if not orderPositions:
                return []

            return orderPositions
        except Exception as e:
            if (hasattr(e, 'data')):
                if (e.data != None and "message" in e.data):
                    abort(400, message=e.data["message"])
            abort(400, message="Неопознанная ошибка")
