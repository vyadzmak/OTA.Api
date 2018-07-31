from models.db_models.models import Messages
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging

# PARAMS
ENTITY_NAME = "Messages By Message Content"
ROUTE = "/messagesByMessageContent"
END_POINT = "messages-by-message-content"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'receiver_user_id':fields.Integer,
    'is_read': fields.Boolean,
    'name': fields.String(attribute=lambda x: x.user_data.name if x.user_data is not None else '')
}

# API METHODS FOR SINGLE ENTITY
class MessagesByMessageContentResource(Resource):
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
            parser.add_argument('message_content_id')
            args = parser.parse_args()
            if len(args) == 0:
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            message_content_id = args['message_content_id']
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)
            messages = session.query(Messages).filter(Messages.message_content_id == message_content_id).all()
            return messages
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

