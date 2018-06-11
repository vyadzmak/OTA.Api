from models.db_models.models import Orders
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
user_data_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name")
}
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'user_id':fields.Integer,
    'creation_date':fields.DateTime,
    'number':fields.String,
    'executor_id': fields.Integer,
    'processed_date': fields.DateTime,
    'execute_date': fields.DateTime,
    'amount': fields.Float,
    'amount_discount': fields.Float,
    'total_amount': fields.Float,
    'order_state_id':fields.Integer,
    #'order_user_data':fields.Nested(user_data_fields)
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
            action_type='GET'
            parser = reqparse.RequestParser()
            parser.add_argument('user_id')
            parser.add_argument('state_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            state_id = int(args['state_id'])
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)
            orders =[]
            # check login

            if (state_id==1 or state_id==3):
                orders = session.query(Orders).filter(Orders.order_state_id==state_id).all()
                t=0
                pass
            elif (state_id==2):
                orders = session.query(Orders).filter(and_(Orders.order_state_id==2,Orders.executor_id==user_id)).all()



            if not orders:
                return []



            return orders
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

