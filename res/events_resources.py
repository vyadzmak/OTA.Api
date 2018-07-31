from models.db_models.models import Events
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from datetime import datetime
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer

# PARAMS
ENTITY_NAME = "Events"
MODEL = Events
ROUTE = "/events"
END_POINT = "events"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'user_creator_id': fields.Integer,
    'product_id': fields.Integer,
    'count_days_notifications': fields.Integer,
    'end_date': fields.DateTime,
    'message': fields.String,
    'type': fields.String(attribute=lambda x: 'success'
    if (x.end_date.replace(tzinfo=None) - datetime.utcnow()).days > x.count_days_notifications else
    'error' if (x.end_date.replace(tzinfo=None) - datetime.utcnow()).days < 1 else 'warning'),
    'name': fields.String(attribute=lambda x: x.user_data.name if x.user_data is not None else ''),
    'product': fields.String(attribute=lambda x: x.product_data.name if x.product_data is not None else ''),
    'product_code': fields.String(attribute=lambda x: x.product_data.product_code if x.product_data is not None else '')
}


# API METHODS FOR SINGLE ENTITY
class EventsResource(Resource):
    def __init__(self):
        self.route = ROUTE + '/<int:id>'
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self, id):
        entity = session.query(MODEL).filter(MODEL.id == id).first()
        if not entity:
            abort(404, message=ENTITY_NAME + " {} doesn't exist".format(id))
        return entity

    def delete(self, id):
        try:
            entity = session.query(MODEL).filter(MODEL.id == id).first()
            if not entity:
                abort(404, message=ENTITY_NAME + " {} doesn't exist".format(id))
            entity.state = False
            session.commit()
            return {}, 204
        except Exception as e:
            session.rollback()
            abort(400, message="Error while remove " + ENTITY_NAME)

    @marshal_with(output_fields)
    def put(self, id):
        try:
            json_data = request.get_json(force=True)
            entity = session.query(MODEL).filter(MODEL.id == id).first()
            if not entity:
                abort(404, message=ENTITY_NAME + " {} doesn't exist".format(id))
            db_transformer.transform_update_params(entity, json_data)
            session.add(entity)
            session.commit()
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update " + ENTITY_NAME)


# API METHODS FOR LIST ENTITIES
class EventsListResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT + '-list'
        pass

    @marshal_with(output_fields)
    def get(self):
        entities = session.query(MODEL).filter(MODEL.state == True).all()
        return entities

    @marshal_with(output_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            json_data['state'] = True
            entity = MODEL(json_data)
            session.add(entity)
            session.commit()
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record " + ENTITY_NAME)
