from models.db_models.models import AdminSettings
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
#PARAMS
ENTITY_NAME = "Admin Settings"
MODEL = AdminSettings
ROUTE ="/adminSettings"
END_POINT = "admin-settings"


#OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'data_refresh_interval': fields.Integer,
    'count_data_take_device': fields.Integer,
    'count_log_data_records_auto_clean': fields.Integer,
    'user_agreement': fields.String,
}


#API METHODS FOR SINGLE ENTITY
class AdminSettingsResource(Resource):
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
            # model.name = json_data['name']
            # model.registration_number = json_data["registration_number"]
            # model.lock_state = json_data["lock_state"]
            # model.client_type_id = json_data["client_type_id"]
            db_transformer.transform_update_params(entity,json_data)
            session.add(entity)
            session.commit()
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while update "+ENTITY_NAME)

#API METHODS FOR LIST ENTITIES
class AdminSettingsListResource(Resource):
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

            #tt = **json_data
            #** {var: "!!"}

            entity = MODEL(json_data)
            # entity = MODEL(
            #     data_refresh_interval=json_data["data_refresh_interval"],
            #     count_data_take_device=json_data["count_data_take_device"],
            #     count_log_data_records_auto_clean=json_data["count_log_data_records_auto_clean"],
            #     user_agreement=json_data["user_agreement"]
            # )
            session.add(entity)
            session.commit()
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record "+ENTITY_NAME)

