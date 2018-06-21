from models.db_models.models import Orders,Users
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer

#PARAMS
ENTITY_NAME = "Orders"
MODEL = Orders
ROUTE ="/orders"
END_POINT = "orders"

#NESTED SCHEMA FIELDS
currency_data_fields ={
    'id': fields.Integer,
    'system_name':fields.String,
    'display_value':fields.String,
    'name':fields.String,
    'is_default': fields.Boolean
}

area_data_fields ={
    'id': fields.Integer,
    'name': fields.String,

}
city_data_fields = {
    'id':fields.Integer,
    'name':fields.String,
    'area_id':fields.Integer,
    'area_data':fields.Nested(area_data_fields)
}
client_address_data_fields ={
    'id': fields.Integer,
    'client_id':fields.Integer,
    'address': fields.String,
    'is_default': fields.Boolean,
    'name': fields.String,
    'confirmed':fields.Boolean,
    'tobacco_alcohol_license': fields.Boolean,
    'code':fields.String,
    'city_id': fields.Integer,
    'city_data':fields.Nested(city_data_fields)
}

order_state_data_fields = {
    'id': fields.Integer,
    'name':fields.String,
    'title': fields.String
}

client_data_fields = {
    'id':fields.Integer,
    'name':fields.String,
    'registration_date': fields.DateTime,
    'registration_number':fields.String,
}
order_user_data_fields = {
    'id': fields.Integer,
    'name':fields.String,
    'client_id':fields.Integer,
    'client_data': fields.Nested(client_data_fields)
}
#OUTPUT SCHEMA
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
    'currency_id': fields.Integer,
    'client_address_id': fields.Integer,
    'currency_data': fields.Nested(currency_data_fields),
    'client_address_data':fields.Nested(client_address_data_fields),
    'order_state_data':fields.Nested(order_state_data_fields),
    'order_user_data': fields.Nested(order_user_data_fields),
    'order_executor_data': fields.Nested(order_user_data_fields)
}


#API METHODS FOR SINGLE ENTITY
class OrdersResource(Resource):
    def __init__(self):
        self.route = ROUTE+'/<int:id>'
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self, id):
        entity = session.query(MODEL).filter(MODEL.id == id).first()
        if not entity:
            abort(404, message=ENTITY_NAME+" {} doesn't exist".format(id))

        entity.order_user_data =session.query(Users).filter(Users.id==entity.user_id).first()
        if (entity.executor_id!=None):
            entity.order_executor_data =session.query(Users).filter(Users.id==entity.executor_id).first()

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
class OrdersListResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT+'-list'
        pass

    @marshal_with(output_fields)
    def get(self):
        entities = session.query(MODEL).all()

        for entity in entities:
            entity.order_user_data = session.query(Users).filter(Users.id == entity.user_id).first()
            if (entity.executor_id != None):
                entity.order_executor_data = session.query(Users).filter(Users.id == entity.executor_id).first()

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

