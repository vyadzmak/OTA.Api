from models.db_models.models import UserLogins, Orders,Settings,UserInfo, Attachments,ViewSettings, Products, BrandsCatalog, PartnersCatalog, UserFavoriteProducts
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
from sqlalchemy import and_
import base64
import datetime
import models.app_models.setting_models.setting_model as settings
import urllib.parse

# PARAMS
ENTITY_NAME = "Mobile User Auth"
ROUTE = "/mobileUserAuth"
END_POINT = "mobile-user-auth"

# NESTED SCHEMA FIELDS
default_image_data_partners = {
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

default_image_data_brands = {
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
currency_data_fields = {
    'id': fields.Integer,
    'system_name': fields.String,
    'display_value': fields.String,
    'name': fields.String,
    'is_default': fields.Boolean
}

unit_data_fields = {
    'id': fields.Integer,
    'system_name': fields.String,
    'display_value': fields.String,
    'name': fields.String,
    'is_default': fields.Boolean
}

default_image_data_products = {
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

slider_images_data_fields={
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
recomendation_elements_data_fields={
    'id': fields.Integer,
    'name': fields.String,
    'category_id': fields.Integer,
    'user_creator_id': fields.Integer,
    'creation_date': fields.DateTime,
    'full_description': fields.String,
    'short_description': fields.String,
    'product_code': fields.String,
    'amount': fields.Float,
    'discount_amount': fields.Float,
    'unit_value': fields.Float,
    'is_stock_product': fields.Boolean,
    'is_discount_product': fields.Boolean,
    'not_available': fields.Boolean,
    'not_show_in_catalog': fields.Boolean,
    'stock_text': fields.String,
    'brand_id': fields.Integer,
    'partner_id': fields.Integer,
    'currency_id': fields.Integer,
    'unit_id': fields.Integer,
    'default_image_id': fields.Integer,
    'default_image_data': fields.Nested(default_image_data_products),
    'comments_count': fields.Integer,
    'rate': fields.Float,
    'product_unit_data': fields.Nested(unit_data_fields),
    'product_currency_data': fields.Nested(currency_data_fields)
}

brand_elements_data_fields ={
'id': fields.Integer,
    'name':fields.String,
    'images': fields.List(fields.Integer),
    'description': fields.String,
    'short_description': fields.String,
    'default_image_id': fields.Integer,
    'default_image_data_brands':fields.Nested(default_image_data_brands),
    'images_data':fields.Nested(default_image_data_brands),
    'products_count': fields.Integer
}

partner_elements_data_fields ={
'id': fields.Integer,
    'name':fields.String,
    'images': fields.List(fields.Integer),
    'description': fields.String,
    'short_description': fields.String,
    'default_image_id': fields.Integer,
    'default_image_data_partners':fields.Nested(default_image_data_partners),
    'images_data':fields.Nested(default_image_data_partners),
    'products_count': fields.Integer
}

view_settings_fields = {
    'id': fields.Integer,
    'show_slider': fields.Boolean,
    'show_badges': fields.Boolean,
    'show_recommendations': fields.Boolean,
    'show_brands':fields.Boolean,
    'show_badge_popular': fields.Boolean,
    'show_badge_discount': fields.Boolean,
    'show_badge_stock': fields.Boolean,
    'show_badge_partners': fields.Boolean,
    'default_slider_image': fields.Integer,

    'slider_images':fields.List(fields.Integer),
    'recomendation_elements': fields.List(fields.Integer),
    'brand_elements': fields.List(fields.Integer),
    'partner_elements':fields.List(fields.Integer),

    'slider_images_data':fields.Nested(slider_images_data_fields),
    'recomendation_elements_data': fields.Nested(recomendation_elements_data_fields),
    'brand_elements_data': fields.Nested(brand_elements_data_fields),
    'partner_elements_data':fields.Nested(partner_elements_data_fields),
}

login_user_client_data = {
    'id': fields.Integer,
    'name': fields.String,
    'registration_number': fields.String
}

login_user_data = {
    'id': fields.Integer,
    'name': fields.String,
    'client_data': fields.Nested(login_user_client_data),
}

user_favorites_products_fields ={
    'id':fields.Integer,
    'products_ids':fields.List(fields.Integer)
}

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'login': fields.String,
    'password': fields.String,
    'user_data': fields.Nested(login_user_data),
    'last_login_date':fields.DateTime,
    'no_image_url': fields.String,
    'no_avatar_url': fields.String,
    'view_settings':fields.Nested(view_settings_fields),
    'user_favorites_products':fields.Nested(user_favorites_products_fields),
    'avatar_url':fields.String
}


# API METHODS FOR SINGLE ENTITY
class MobileUserAuthResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self):
        error_message =''
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('login')
            parser.add_argument('password')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            login = args['login']
            password = args['password']

            encrypted_password = str(base64.b64encode(bytes(password, "utf-8")))


            # check login
            user_login = session.query(UserLogins).filter(and_(
                UserLogins.login == login,
                UserLogins.password == encrypted_password)) \
                .first()

            if not user_login:
                error_message='Ошибка авторизации. Пользователь с такими данными не найден!'
                abort(400, message='Ошибка авторизации. Пользователь с такими данными не найден!')

            if (user_login.user_data.lock_state==True):
                error_message='Ошибка авторизации. Пользователь заблокирован или не активирован!'
                abort(400, message='Ошибка авторизации. Пользователь заблокирован!')

            if (user_login.user_data.client_data.lock_state==True):
                error_message='Ошибка авторизации. Пользователь с такими данными не найден!'
                abort(400, message='Ошибка авторизации. Клиент (компания) заблокирован!')

            user_login.last_login_date =datetime.datetime.now(datetime.timezone.utc)
            session.add(user_login)
            session.commit()
            # get to additional params

            orders = session.query(Orders).filter(Orders.order_state_id==1).all()
            if (orders!=None):
                user_login.orders_count = len(orders)


            #no image url
            setting = session.query(Settings).filter(Settings.name=='no_image_url').first()
            if (not setting):
                return user_login
            # api_url = settings.API_URL
            user_login.no_image_url=setting.value

            setting = session.query(Settings).filter(Settings.name == 'no_avatar_url').first()
            if (not setting):
                return user_login
            # api_url = settings.API_URL
            user_login.no_avatar_url =setting.value

            # getting avatar
            user_info = session.query(UserInfo).filter(UserInfo.user_id == user_login.id).first()
            if user_info!=None:
                attachment = session.query(Attachments).filter(Attachments.id == user_info.avatar_id).first()
                if attachment:
                    user_login.avatar_url = attachment.thumb_file_path

            view_settings = session.query(ViewSettings).first()

            if (not view_settings):
                error_message = 'Критическая ошибка! Данные построения интерфейса не найдены'
                abort(400, message='Критическая ошибка! Данные построения интерфейса не найдены')


            # load additional params with view settings
            # 'slider_images_data': fields.Nested(slider_images_data_fields),
            # 'recomendation_elements_data': fields.Nested(recomendation_elements_data_fields),
            # 'brand_elements_data': fields.Nested(brand_elements_data_fields),
            # 'partner_elements_data': fields.Nested(partner_elements_data_fields),
            slider_images =[]
            if (view_settings.slider_images!=None):
                for id in view_settings.slider_images:
                    attachment = session.query(Attachments).filter(Attachments.id==id).first()

                    if (not attachment):
                        continue

                    slider_images.append(attachment)

                view_settings.slider_images_data =slider_images

            recommendations = []
            if (view_settings.recomendation_elements != None):
                for id in view_settings.recomendation_elements:
                    product = session.query(Products).filter(Products.id == id).first()

                    if (not product):
                        continue

                    recommendations.append(product)

                view_settings.recomendation_elements_data = recommendations

            brands = []
            if (view_settings.brand_elements != None):
                for id in view_settings.brand_elements:
                    brand = session.query(BrandsCatalog).filter(BrandsCatalog.id == id).first()

                    if (not brand):
                        continue

                    brands.append(brand)

                view_settings.brand_elements_data = brands

            partners = []
            if (view_settings.partner_elements != None):
                for id in view_settings.partner_elements:
                    partner = session.query(PartnersCatalog).filter(PartnersCatalog.id == id).first()

                    if (not partner):
                        continue

                    partners.append(partner)

                view_settings.partner_elements_data = partners

            user_login.view_settings =view_settings

            user_login.user_favorites_products = session.query(UserFavoriteProducts).filter(UserFavoriteProducts.user_id==user_login.user_data.id).first()

            return user_login
        except Exception as e:
            abort(400, message = error_message)

