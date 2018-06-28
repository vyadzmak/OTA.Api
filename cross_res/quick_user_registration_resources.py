from models.db_models.models import Users, UserLogins, UserInfo,Clients,ClientInfo,UserConfirmationCodes,UserFavoriteProducts
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import datetime
import base64
# PARAMS
ENTITY_NAME = "Quick User Registration"
# MODEL = Users
ROUTE = "/quickUserRegistration"
END_POINT = "quick-user-registration"

# NESTED SCHEMA FIELDS
avatar_data_fields = {
    'id': fields.Integer,
    'original_file_name': fields.String,
    'file_path': fields.String,
    'file_size': fields.Integer,
    'uid': fields.String,
    'user_creator_id': fields.Integer,
    'upload_date': fields.DateTime,
    'thumb_file_path': fields.String,
    'optimized_size_file_path': fields.String
}
user_info_data = {
    "id":fields.Integer,
    "user_id":fields.Integer,
    "email":fields.String,
    "phone_number":fields.String,
    "birthday":fields.String,
    'avatar_id':fields.Integer,
    'avatar_data':fields.Nested(avatar_data_fields)
}

user_role_data = {
    'id': fields.Integer,
    'name': fields.String,
    'title': fields.String,

}

user_client_data = {
    'id': fields.Integer,
    'name': fields.String,
    'registration_number': fields.String
}

user_login_data = {
    'id': fields.Integer,
    'login': fields.String,
    'last_login_date': fields.DateTime
}

user_confirmation_code_fields ={
    'id':fields.Integer,
    'code':fields.String
}

user_favorites_products_fields ={
    'id':fields.Integer,
    'products_ids':fields.List(fields.Integer)
}


# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'lock_state': fields.Boolean,
    'client_data': fields.Nested(user_client_data),
    'user_role_data': fields.Nested(user_role_data),
    'user_login': fields.Nested(user_login_data),
    'user_info_data':fields.Nested(user_info_data),
    'user_confirmation_code_data': fields.Nested(user_confirmation_code_fields),
    'user_favorites_products': fields.Nested(user_favorites_products_fields)
}
# API METHODS FOR LIST ENTITIES
class QuickUserRegistrationResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def post(self):
        error_message = ""
        try:
            json_data = request.get_json(force=True)

            phone_number = json_data['phone_number']

            user_login = session.query(UserLogins).filter(UserLogins.login==phone_number).first()

            if (user_login!=None):
                error_message = "Пользователь с таким номером уже существует системе!"
                abort(400, message="")


            clients_args ={}
            clients_args["name"] = json_data["client_name"]
            clients_args["client_type_id"] = 3
            client_entity = Clients(clients_args)
            session.add(client_entity)
            session.commit()

            client_id = client_entity.id



            users_args ={}
            users_args['name']=json_data["user_name"]
            users_args['client_id']=client_id
            users_args['user_role_id']=4
            users_args['lock_state']=True
            user_entity = Users(users_args)
            session.add(user_entity)
            session.commit()

            user_login_args = {}
            user_login_args['user_id'] = user_entity.id
            user_login_args['login'] = phone_number
            user_login_args['password'] = str(base64.b64encode(bytes(json_data["password"],"utf-8")))
            user_login_entity = UserLogins(user_login_args)
            session.add(user_login_entity)
            session.commit()

            user_info_args = {}
            user_info_args['user_id'] = user_entity.id
            user_info_args['phone_number'] ='+'+phone_number
            user_info_entity = UserInfo(user_info_args)
            session.add(user_info_entity)
            session.commit()

            user_confirmation_code_args = {}
            user_confirmation_code_args['user_id'] = user_entity.id
            user_confirmation_entity = UserConfirmationCodes(user_confirmation_code_args)
            session.add(user_confirmation_entity)
            session.commit()

            user_favorites_args = {}
            user_favorites_args['user_id'] = user_entity.id
            user_favorites_args['products_ids'] =[]
            user_favorites_entity = UserFavoriteProducts(user_favorites_args)
            session.add(user_favorites_entity)
            session.commit()


            user = session.query(Users).filter(Users.id==user_entity.id).first()
            user.user_confirmation_code_data = user_confirmation_entity
            user.user_favorites_products = user_favorites_entity
            if (not user):
                abort(400, message ="Данные не найдены")

            login = session.query(UserLogins).filter(UserLogins.user_id == user_entity.id).first()
            user_info = session.query(UserInfo).filter(UserInfo.user_id == user.id).first()
            user.user_login = login
            user.user_info_data = user_info
            return user, 201


        except Exception as e:
            session.rollback()
            abort(400, message=error_message, code=400)
