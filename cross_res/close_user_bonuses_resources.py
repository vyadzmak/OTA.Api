from models.db_models.models import UserBonuses
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import and_
#PARAMS
ENTITY_NAME = "Close User Bonuses"
MODEL = UserBonuses
ROUTE ="/closeUserBonuses"
END_POINT = "close-user-bonuses"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'status' :fields.Integer
}

#API METHODS FOR SINGLE ENTITY
class CloseUserBonusesResource(Resource):
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

            user_bonuses = session.query(UserBonuses).filter(and_(
                UserBonuses.user_id == user_id,
                UserBonuses.state== True)) \
                .all()

            for bonus in user_bonuses:
                bonus.state = False
                session.add(bonus)
                session.commit()

            response ={
                'status' : 200
            }

            return response
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")



