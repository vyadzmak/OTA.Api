from models.db_models.models import Products, ProductComments, ViewSettings,UserFavoriteProducts,OrderPositions,UserCartPositions,UserCarts
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
from operator import itemgetter
from sqlalchemy import desc
from sqlalchemy import and_
# PARAMS
ENTITY_NAME = "Filter Products"
MODEL = Products
ROUTE = "/filterProducts"
END_POINT = "filter-products"

# NESTED SCHEMA FIELDS
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

# OUTPUT SCHEMA
output_fields = {
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
    'product_currency_data': fields.Nested(currency_data_fields),
    'count':fields.Integer
}


# API METHODS FOR SINGLE ENTITY
class FilterProductResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    def get_user_cart_argument(self,args):
        try:
            user_cart_id = args['user_cart_id']
            return int(user_cart_id)
        except:
            return -1

    # filter by brand
    def filter_by_brand(self, brand_id):
        try:
            products = session.query(Products).filter(Products.brand_id==brand_id).all()
            return products
        except Exception as e:
            return None

    # filter by partner
    def filter_by_partner(self, partner_id):
        try:
            products = session.query(Products).filter(Products.partner_id == partner_id).all()
            return products
            pass
        except Exception as e:
            return None

            # filter by partner
    def filter_by_all_partners(self):
                try:
                    products = session.query(Products).filter(Products.partner_id !=None).all()
                    return products
                    pass
                except Exception as e:
                    return None

            # filter by discount
    def filter_by_discount(self):
                try:
                    products = session.query(Products).filter(Products.is_discount_product==True).all()
                    return products
                    pass
                except Exception as e:
                    return None

                    # filter by discount
    def filter_by_stock(self):
                        try:
                            products = session.query(Products).filter(Products.is_stock_product == True).all()
                            return products
                            pass
                        except Exception as e:
                            return None

    # filter by favorites
    def filter_by_favorites(self, user_id):
            try:
                user_favorite_products = session.query(UserFavoriteProducts).filter(
                    UserFavoriteProducts.user_id == user_id).first()

                if (not user_favorite_products):
                    abort(400, message="Not found favorite products")

                if (not user_favorite_products):
                    abort(400, message="Not found favorite products")

                products = []

                for favorite_product_id in user_favorite_products.products_ids:
                    product = session.query(Products).filter(Products.id == favorite_product_id).first()

                    if (not product):
                        continue

                    products.append(product)
                return products
            except Exception as e:
                return None

    # filter by recommendations
    def filter_by_recommendations(self):
        try:
            view_settings = session.query(ViewSettings).first()

            if (not view_settings):
                return None
            products = []
            rec_elements =view_settings.recomendation_elements

            if (not rec_elements):
                return None

            for rec_element in rec_elements:
                product = session.query(Products).filter(Products.id==rec_element).first()

                if (not product):
                    continue

                products.append(product)

            return products
            pass
        except Exception as e:
            return None


    # filter by name
    def filter_by_name(self,name):
            try:
                r_name = '%'+name+'%'
                products = session.query(Products).filter(Products.name.ilike(r_name)).all()
                return products
            except Exception as e:
                return None


                # filter by name

    def filter_by_popular(self):
        try:
            limit =10

            order_positions = session.query(OrderPositions).all()

            p_ids = []
            for order_position in order_positions:
                if (order_position.product_id in p_ids==True):
                    continue
                else:
                    p_ids.append(order_position.product_id)
                pass

            f_products =[]

            for p_id in p_ids:

                ps = session.query(OrderPositions).filter(OrderPositions.product_id==p_id).all()

                count =0

                for p in ps:
                    count+=p.count
                f_products.append([p_id,count])

            sorted(f_products, key=itemgetter(1))
            result_products = []
            counter=0
            for pr in f_products:
                if (counter>=limit):
                    break

                p_id =pr[0]

                product = session.query(Products).filter(Products.id==p_id).first()

                if (not product):
                    continue

                result_products.append(product)



            # products = session.query(Products).filter(Products.name.ilike(r_name)).all()
            # return products
            return result_products
        except Exception as e:
            return None

    @marshal_with(output_fields)
    def get(self):
        try:

            action_type = 'GET'
            parser = reqparse.RequestParser()
            parser.add_argument('user_id')
            parser.add_argument('filter_parameter')
            parser.add_argument('filter_value')
            parser.add_argument('user_cart_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            filter_parameter = args['filter_parameter']
            filter_value = args['filter_value']
            user_cart_id = self.get_user_cart_argument(args)
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)
            products = []
            # filter paramenters 1 - brands, 2 -partners, 3 - favorites, 4 - recommends , 5 - filter by name, 6 - discount, 7 -stock
            # session.query(Products).filter(Products.category_id==category_id).order_by(desc(Products.id)).all()
            # products = products.

            if (str(filter_parameter)=='1'):
                products = self.filter_by_brand(filter_value)
            elif (str(filter_parameter)=='2'):
                products = self.filter_by_partner(filter_value)
            elif (str(filter_parameter) == '3'):
                products = self.filter_by_favorites(user_id)
            elif (str(filter_parameter) == '4'):
                products = self.filter_by_recommendations()
            elif (str(filter_parameter)=='5'):
                products = self.filter_by_name(filter_value)
            elif (str(filter_parameter)=='6'):
                products = self.filter_by_discount()
            elif (str(filter_parameter) == '7'):
                products = self.filter_by_stock()
            elif (str(filter_parameter) == '8'):
                products = self.filter_by_all_partners()
            elif (str(filter_parameter) == '9'):
                products = self.filter_by_popular()

            if not products:
                abort(400, message='Ошибка получения данных. Данные не найдены')
            for product in products:
                if (user_cart_id==-1):
                    product.count =1
                else:
                    user_cart = session.query(UserCarts).filter(UserCarts.id == user_cart_id).first()
                    check_user_cart_positions = session.query(UserCartPositions).filter(and_(
                        UserCartPositions.user_cart_id == user_cart.id,
                        UserCartPositions.product_id == product.id
                    )).first()

                    if (not check_user_cart_positions):
                        product.count = 1
                    else:
                        product.count=check_user_cart_positions.count
                    pass

                comments = session.query(ProductComments).filter(
                    ProductComments.product_id == product.id and ProductComments.is_delete == False).all()
                product.comments_count = 0
                product.rate = 0
                if (not comments):
                    continue
                total_rate = 0
                comments_count = 0
                for comment in comments:
                    total_rate += comment.rate
                    comments_count += 1

                if (comments_count > 0):
                    product.comments_count = comments_count
                    product.rate = round((total_rate / comments_count), 2)

            # products.internal_products_count = len(products)

            return products
        except Exception as e:
            if (hasattr(e, 'data')):
                if (e.data != None and "message" in e.data):
                    abort(400, message=e.data["message"])
            abort(400, message="Неопознанная ошибка")
        finally:
            pass
            # session.rollback()
