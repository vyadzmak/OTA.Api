from models.db_models.models import UserConfirmationCodes, Users
from db.db import session
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import and_
import base64
import datetime
from sqlalchemy import desc
# PARAMS
ENTITY_NAME = "User Confirmation Code Check"
ROUTE = "/userConfirmationCodeCheck"
END_POINT = "user-confirmation-code-check"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {

}


# API METHODS FOR SINGLE ENTITY
class UserConfirmationCodeCheckResource(Resource):
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
            parser.add_argument('code')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            code = args['code']
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)
            #products = session.query(Products).filter(Products.category_id==category_id).order_by(desc(Products.id)).all()

            user_confirmation_code = session.query(UserConfirmationCodes).filter(UserConfirmationCodes==user_id).order_by(desc(UserConfirmationCodes.id)).first()
            if (not user_confirmation_code):
                abort(400,message='Error')


            if (user_confirmation_code!=code):
                abort(400,message='Error')

            user = session.query(Users).filter(Users.id==user_id).first()

            if (not user):
                abort(400,message='Error')


            user.lock_state = False
            session.add(user)
            session.commit()

            return 200, 'OK'
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")

