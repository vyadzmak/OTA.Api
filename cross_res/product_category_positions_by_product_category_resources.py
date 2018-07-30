from models.db_models.models import ProductCategoryPositions
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging

# PARAMS
ENTITY_NAME = "Product category position by product category"
MODEL = ProductCategoryPositions
ROUTE = "/productCategoryPositionsByCategory"
END_POINT = "product-category-position-by-product-category"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'parent_category_id': fields.Integer,
    'child_category_positions': fields.List(fields.Integer)
}


# API METHODS FOR SINGLE ENTITY
class ProductCategoryPositionsByProductCategoryResource(Resource):
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
            if len(args) == 0:
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            category_id = args['category_id']
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)
            category_position = session.query(ProductCategoryPositions).filter(
                ProductCategoryPositions.parent_category_id == category_id).first()
            if not category_position:
                category_position = {'id': None,
                        'parent_category_id': category_id,
                        'child_category_positions': []}

            return category_position
        except Exception as e:
            if (hasattr(e, 'data')):
                if (e.data != None and "message" in e.data):
                    abort(400, message=e.data["message"])
            abort(400, message="Неопознанная ошибка")
