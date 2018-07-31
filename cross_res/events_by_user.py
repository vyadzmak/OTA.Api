from models.db_models.models import Events
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
from datetime import datetime

# PARAMS
ENTITY_NAME = "Events By User"
ROUTE = "/eventsByUser"
END_POINT = "events-by-user"


# API METHODS FOR SINGLE ENTITY
class EventsByUserResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

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
            events = session.query(Events).filter(Events.state == True).all()
            counter = 0
            for x in events:
                if (x.end_date.replace(tzinfo=None) - datetime.utcnow()).days <= x.count_days_notifications:
                    counter += 1
            return counter
        except Exception as e:
            if (hasattr(e, 'data')):
                if (e.data != None and "message" in e.data):
                    abort(400, message=e.data["message"])
            abort(400, message="Неопознанная ошибка")
