from models.db_models.models import ProductsPositions
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging

# PARAMS
ENTITY_NAME = "Product position by product category"
MODEL = ProductsPositions
ROUTE = "/productsPositionsByCategory"
END_POINT = "product-position-by-product-category"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'category_id': fields.Integer,
    'products_positions': fields.List(fields.Integer)
}


# API METHODS FOR SINGLE ENTITY
class ProductsPositionsByProductCategoryResource(Resource):
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
            parser.add_argument('category_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            category_id = args['category_id']
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)
            product_position = session.query(ProductsPositions).filter(
                ProductsPositions.category_id == category_id).first()
            if not product_position:
                product_position = {'id': None,
                        'category_id': category_id,
                        'products_positions': []}

            return product_position
        except Exception as e:
            if (hasattr(e, 'data')):
                if (e.data != None and "message" in e.data):
                    abort(400, message=e.data["message"])
            abort(400, message="Неопознанная ошибка")
