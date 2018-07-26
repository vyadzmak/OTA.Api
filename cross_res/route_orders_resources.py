from models.db_models.models import Orders, Users
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import and_
import base64
import datetime

# PARAMS
ENTITY_NAME = "Route Orders"
ROUTE = "/routeOrders"
END_POINT = "route-orders"

# NESTED SCHEMA FIELDS
currency_data_fields = {
    'id': fields.Integer,
    'system_name': fields.String,
    'display_value': fields.String,
    'name': fields.String,
    'is_default': fields.Boolean
}

area_data_fields = {
    'id': fields.Integer,
    'name': fields.String,

}
city_data_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'area_id': fields.Integer,
    'area_data': fields.Nested(area_data_fields)
}
client_address_data_fields = {
    'id': fields.Integer,
    'client_id': fields.Integer,
    'address': fields.String,
    'is_default': fields.Boolean,
    'name': fields.String,
    'confirmed': fields.Boolean,
    'tobacco_alcohol_license': fields.Boolean,
    'code': fields.String,
    'city_id': fields.Integer,
    'city_data': fields.Nested(city_data_fields),
    'phone_number': fields.String
}

order_state_data_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'title': fields.String
}

client_data_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'registration_date': fields.DateTime,
    'registration_number': fields.String,
}
order_user_data_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'client_id': fields.Integer,
    'client_data': fields.Nested(client_data_fields)
}
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'creation_date': fields.DateTime,
    'number': fields.String,
    'executor_id': fields.Integer,
    'processed_date': fields.DateTime,
    'execute_date': fields.DateTime,
    'amount': fields.Float,
    'amount_discount': fields.Float,
    'total_amount': fields.Float,
    'order_state_id': fields.Integer,
    'currency_id': fields.Integer,
    'client_address_id': fields.Integer,
    'currency_data': fields.Nested(currency_data_fields),
    'client_address_data': fields.Nested(client_address_data_fields),
    'order_state_data': fields.Nested(order_state_data_fields),
    'order_user_data': fields.Nested(order_user_data_fields),
    'order_executor_data': fields.Nested(order_user_data_fields)
}


# API METHODS FOR SINGLE ENTITY
class RouteOrdersResource(Resource):
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
            parser.add_argument('state_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            state_id = int(args['state_id'])
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)
            orders = []
            # check login

            if (state_id == 1 or state_id == 3):
                orders = session.query(Orders).filter(Orders.order_state_id == state_id).all()
                t = 0
                pass
            elif (state_id == 2):
                orders = session.query(Orders).filter(
                    and_(Orders.order_state_id == 2, Orders.executor_id == user_id)).all()

            for entity in orders:
                entity.order_user_data = session.query(Users).filter(Users.id == entity.user_id).first()
                if (entity.executor_id != None):
                    entity.order_executor_data = session.query(Users).filter(Users.id == entity.executor_id).first()

            if not orders:
                return []

            return orders
        except Exception as e:
            if (hasattr(e, 'data')):
                if (e.data != None and "message" in e.data):
                    abort(400, message=e.data["message"])
            abort(400, message="Неопознанная ошибка")
