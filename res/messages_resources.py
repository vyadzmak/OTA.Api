from models.db_models.models import Messages, MessageContents
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer

#PARAMS
ENTITY_NAME = "Messages"
MODEL = Messages
ROUTE ="/messages"
END_POINT = "messages"

#NESTED SCHEMA FIELDS

#OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'date':fields.DateTime,
    'message': fields.String
}


#API METHODS FOR SINGLE ENTITY
class LogResource(Resource):
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
class LogListResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT+'-list'
        pass

    def clean_log_by_condition(self):
        try:
            logs = session.query(Log).all()

            if (len(logs)>5000):
                session.query(Log).delete()
                session.commit()
            pass
        except Exception as e:
            session.rollback()

    @marshal_with(output_fields)
    def get(self):
        entities = session.query(MODEL).all()
        return entities

    @marshal_with(output_fields)
    def post(self):
        try:
            self.clean_log_by_condition()
            json_data = request.get_json(force=True)
            entity = MODEL(json_data)
            session.add(entity)
            session.commit()
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record "+ENTITY_NAME)

