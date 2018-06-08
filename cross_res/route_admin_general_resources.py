from models.db_models.models import AdminSettings, Log, Users
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import and_
import base64
import datetime

# PARAMS
ENTITY_NAME = "Route Admin General"
ROUTE = "/routeAdminGeneral"
END_POINT = "route-admin-general"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'data_refresh_interval': fields.Integer,
    'count_data_take_device': fields.Integer,
    'count_log_data_records_auto_clean': fields.Integer,
    'user_agreement': fields.String
}


# API METHODS FOR SINGLE ENTITY
class RouteAdminGeneralResource(Resource):
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
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']

            user_action_logging.log_user_actions(ROUTE,user_id, action_type)

            # check login
            admin_settings = session.query(AdminSettings).first()

            if not admin_settings:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            return admin_settings
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

