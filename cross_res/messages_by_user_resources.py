from models.db_models.models import Messages
from db.db import session
from flask import request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging

# PARAMS
ENTITY_NAME = "Messages By User"
ROUTE = "/messagesByUser"
END_POINT = "messages-by-user"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'receiver_user_id': fields.Integer,
    'is_read': fields.Boolean,
    'title': fields.String(attribute=lambda x: x.message_content.title if x.message_content is not None else ''),
    'date': fields.String(
        attribute=lambda x: x.message_content.creation_date if x.message_content is not None else None),
    'as_date': fields.String(
        attribute=lambda x: x.message_content.creation_date.strftime("%Y-%m-%d %H:%M") if x.message_content is not None else ''),
    'is_popup': fields.String(
        attribute=lambda x: x.message_content.is_popup if x.message_content is not None else False)
}


# API METHODS FOR SINGLE ENTITY
class MessagesByUserResource(Resource):
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
            args = parser.parse_args()
            if len(args) == 0:
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)
            messages = session.query(Messages).filter(Messages.receiver_user_id == user_id).all()
            return messages
        except Exception as e:
            if (hasattr(e, 'data')):
                if (e.data != None and "message" in e.data):
                    abort(400, message=e.data["message"])
            abort(400, message="Неопознанная ошибка")

    @marshal_with(output_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            entity = session.query(Messages).filter(Messages.id == json_data['id']).first()
            if not entity:
                abort(404, message="Record doesn't exist".format(id))
            entity.is_read = True
            session.add(entity)
            session.commit()
            return entity, 201
        except Exception as e:
            session.rollback()
            abort(400, message="Error while updating record")