from models.db_models.models import Messages, MessageContents, Users
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import models.app_models.setting_models.setting_model as settings

# PARAMS
ENTITY_NAME = "MessageContents"
MODEL = MessageContents
ROUTE = "/messageContents"
END_POINT = "messageContents"

# NESTED SCHEMA FIELDS
# user_fields = {
#     'name': fields.String(attribute=lambda x: x.last_name + ' ' + x.first_name)
# }
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'user_sender_id': fields.Integer,
    'creation_date': fields.DateTime,
    'title': fields.String,
    'message': fields.String,
    'is_popup': fields.Boolean,
    # 'user_data': fields.Nested(user_fields)
    'name': fields.String(attribute=lambda x: x.user_data.name if x.user_data is not None else '')
}


# API METHODS FOR SINGLE ENTITY
class MessageContentsResource(Resource):
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
            session.delete(entity)
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
class MessageContentsListResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT + '-list'
        pass

    @marshal_with(output_fields)
    def get(self):
        entities = session.query(MODEL).all()
        return entities

    @marshal_with(output_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            send_all = json_data.get('send_all', False)
            receivers = json_data.get('receivers', [])
            json_data['receivers'] = None
            json_data['send_all'] = None
            entity_data = {'user_sender_id': json_data['user_sender_id'],
                           'title': json_data['title'],
                           'message': json_data['message'],
                           'is_popup': json_data['is_popup']}
            entity = MODEL(entity_data)

            session.add(entity)
            session.commit()

            if send_all:
                users = session.query(Users.id).filter(Users.client_id != settings.OWNER_CLIENT_ID).all()
                session.bulk_insert_mappings(Messages, [
                    {'receiver_user_id': user[0],
                     'message_content_id': entity.id,
                     'is_read': False}
                    for user in users
                ])
                session.commit()
            else:
                session.bulk_insert_mappings(Messages, [
                    {'receiver_user_id': user_id,
                     'message_content_id': entity.id,
                     'is_read': False}
                    for user_id in receivers
                ])
                session.commit()
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while adding record " + ENTITY_NAME)
