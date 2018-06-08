from models.db_models.models import Log
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import and_
import base64
import datetime

# PARAMS
ENTITY_NAME = "Route Admin Logs"
ROUTE = "/routeAdminLogs"
END_POINT = "route-admin-logs"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'id':fields.Integer,
    'date': fields.DateTime,
    'message': fields.String
}


# API METHODS FOR SINGLE ENTITY
class RouteAdminLogsResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self):
        try:
            owner_client_id = 3
            action_type='GET'
            parser = reqparse.RequestParser()
            parser.add_argument('user_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']

            user_action_logging.log_user_actions(ROUTE,user_id, action_type)

            # check login
            logs = session.query(Log).order_by(Log.id.desc()).all()


            if not logs:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            return logs
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

