from models.db_models.models import Attachments
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging

# PARAMS
ENTITY_NAME = "Attachments Info"
ROUTE = "/attachmentsInfo"
END_POINT = "attachments-info"

# NESTED SCHEMA FIELDS
user_data = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name")
}
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'upload_date': fields.DateTime,
    'original_file_name': fields.String,
    'file_size': fields.Integer,
    'file_path': fields.String,
    'user_creator_id': fields.Integer,
    'thumb_file_path': fields.String,
    'optimized_size_file_path': fields.String,
    'uid': fields.String,
    'attachment_user_data': fields.Nested(user_data),
}


# API METHODS FOR SINGLE ENTITY
class AttachmentsInfoResource(Resource):
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
            parser.add_argument('attachments_ids')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            attachments_ids = args['attachments_ids']
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)

            attachments_ids = [int(s) for s in attachments_ids.split(',')]
            attachments = session.query(Attachments).filter(Attachments.id.in_(attachments_ids)).all()
            if not attachments:
                return []
                # abort(400, message='Ошибка получения данных. Данные не найдены')

            # result = copy.deepcopy(attachments)
            return attachments
        except Exception as e:
            if (hasattr(e, 'data')):
                if (e.data != None and "message" in e.data):
                    abort(400, message=e.data["message"])
            abort(400, message="Неопознанная ошибка")
        finally:
            pass
            # session.rollback()
