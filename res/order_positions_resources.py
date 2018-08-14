from models.db_models.models import OrderPositions
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer

#PARAMS
ENTITY_NAME = "Order Positions"
MODEL = OrderPositions
ROUTE ="/orderPositions"
END_POINT = "order-positions"

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
    'order_data': fields.Nested(order_data_fields),
    'order_position_states': fields.Nested(order_position_states_data),
    'bonuses': fields.Float
}


#API METHODS FOR SINGLE ENTITY
class OrderPositionsResource(Resource):
    def __init__(self):
        self.route = ROUTE+'/<int:id>'
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self, id):
        entity = session.query(MODEL).filter(MODEL.id == id).first()
        if not entity:
            abort(404, message=ENTITY_NAME+" {} doesn't exist".format(id))
        return entity

    def delete(self, id):
        try:
            entity = session.query(MODEL).filter(MODEL.id == id).first()
            if not entity:
                abort(404, message=ENTITY_NAME+" {} doesn't exist".format(id))
            session.delete(entity)
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove "+ENTITY_NAME)

    @marshal_with(output_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            entity = session.query(MODEL).filter(MODEL.id == id).first()
            if not entity:
                abort(404, message=ENTITY_NAME + " {} doesn't exist".format(id))
            db_transformer.transform_update_params(entity,json_data)
            session.add(entity)
            session.commit()
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update "+ENTITY_NAME)

#API METHODS FOR LIST ENTITIES
class OrderPositionsListResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT+'-list'
        pass

    @marshal_with(output_fields)
    def get(self):
        entities = session.query(MODEL).all()
        return entities

    @marshal_with(output_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            entity = MODEL(json_data)
            session.add(entity)
            session.commit()
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record "+ENTITY_NAME)

