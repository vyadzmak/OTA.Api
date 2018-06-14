from models.db_models.models import ProductComments, Log, Users
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import and_
import base64
import datetime

# PARAMS
ENTITY_NAME = "Route Catalog Products Comments"
ROUTE = "/routeCatalogProductsComments"
END_POINT = "route-catalog-products-comments"

# NESTED SCHEMA FIELDS
user_data_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name")
}
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'user_id':fields.Integer,
    'creation_date': fields.DateTime,
    'comment_text':fields.String,
    'rate':fields.Float,
    'is_delete':fields.Boolean,
    'product_id':fields.Integer,
    'comment_user_data':fields.Nested(user_data_fields),

}


# API METHODS FOR SINGLE ENTITY
class RouteCatalogProductsCommentsResource(Resource):
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
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            product_id = args['product_id']
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)

            # check login
            comments = session.query(ProductComments).filter(ProductComments.product_id==product_id).all()

            if not comments:
                return []
                #abort(400, message='Ошибка получения данных. Данные не найдены')

            return comments
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

