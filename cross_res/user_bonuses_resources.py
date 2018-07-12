from models.db_models.models import UserBonuses
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import and_
#PARAMS
ENTITY_NAME = "User Bonuses Details"
MODEL = UserBonuses
ROUTE ="/userBonusesDetails"
END_POINT = "user-bonuses-details"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'order_id': fields.Integer,
    'user_id': fields.Integer,
    'creation_date': fields.DateTime,
    'state':fields.Boolean,
    'amount': fields.Float
}

#API METHODS FOR SINGLE ENTITY
class UserBonusesDetailsResource(Resource):
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
            if (not user_bonuses):
                return []
                # abort(400, message= "Bonuses not found")


            return user_bonuses
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")



