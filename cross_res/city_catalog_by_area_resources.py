from models.db_models.models import CityCatalog
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.image_path_converter_modules.image_path_converter as image_path_converter
#PARAMS
ENTITY_NAME = "City Catalog by Area"
MODEL = CityCatalog
ROUTE ="/cityCatalogByArea"
END_POINT = "city-catalog-by-area"

#NESTED SCHEMA FIELDS
area_data_fields ={
    'id': fields.Integer,
    'name': fields.String,

}
#OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'name':fields.String,
    'area_id':fields.Integer,
    'area_data':fields.Nested(area_data_fields)
}


#API METHODS FOR SINGLE ENTITY
class CityCatalogByAreaResource(Resource):
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
            parser.add_argument('area_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            area_id = args['area_id']
            user_action_logging.log_user_actions(ROUTE,user_id, action_type)
            city_catalogs = session.query(CityCatalog).filter(CityCatalog.area_id==area_id).all()
            if not city_catalogs:
                abort(400, message='Ошибка получения данных. Данные не найдены')


            return city_catalogs
        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")



