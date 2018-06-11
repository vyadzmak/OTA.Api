from models.db_models.models import ViewSettings
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import and_
import base64
import datetime

# PARAMS
ENTITY_NAME = "Route View Settings Badges"
ROUTE = "/routeViewSettingsBadges"
END_POINT = "route-view-settings-Badges"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'show_badge_popular': fields.Boolean,
    'show_badge_discount': fields.Boolean,
    'show_badge_stock': fields.Boolean,
    'show_badge_partners': fields.Boolean,

}


# API METHODS FOR SINGLE ENTITY
class RouteViewSettingsBadgesResource(Resource):
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
            view_settings = session.query(ViewSettings).first()
            return view_settings
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

