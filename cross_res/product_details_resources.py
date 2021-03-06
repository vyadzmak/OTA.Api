from models.db_models.models import Products, ProductComments, Attachments, Orders, OrderPositions, BrandsCatalog, \
    PartnersCatalog
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import and_

# PARAMS
ENTITY_NAME = "Product Details"
MODEL = Products
ROUTE = "/productDetails"
END_POINT = "product-details"

# NESTED SCHEMA FIELDS
brand_data_fields = {
    'id': fields.Integer,
    'name': fields.String
}

partner_data_fields = {
    'id': fields.Integer,
    'name': fields.String
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
gallery_image_data_fields = {
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

recommendations_data_fields = {
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
    'rate': fields.Float(attribute=lambda x: round(x.rate or 0, 2)),
    'product_unit_data': fields.Nested(unit_data_fields),
    'product_currency_data': fields.Nested(currency_data_fields),
    'product_alt_unit_data': fields.Nested(unit_data_fields),
    'alt_amount': fields.Float,
    'alt_unit_value': fields.Float,
    'alt_unit_id': fields.Integer,
    'alt_discount_amount': fields.Float
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
    'brand_data': fields.Nested(brand_data_fields),
    'partner_id': fields.Integer,
    'partner_data': fields.Nested(partner_data_fields),
    'currency_id': fields.Integer,
    'unit_id': fields.Integer,
    'default_image_id': fields.Integer,
    'default_image_data': fields.Nested(default_image_data_products),
    'comments_count': fields.Integer,
    'rate': fields.Float(attribute=lambda x: round(x.rate or 0, 2)),
    'product_unit_data': fields.Nested(unit_data_fields),
    'product_currency_data': fields.Nested(currency_data_fields),

    'gallery_images': fields.List(fields.Integer),
    'product_recomendations': fields.List(fields.Integer),

    'gallery_images_data': fields.Nested(gallery_image_data_fields),
    'product_recomendations_data': fields.Nested(recommendations_data_fields),
    'recommended_amount': fields.Float,
    'bonus_percent': fields.Float,
    'can_comments': fields.Boolean,
    'product_alt_unit_data': fields.Nested(unit_data_fields),
    'alt_amount': fields.Float,
    'alt_unit_value': fields.Float,
    'alt_unit_id': fields.Integer,
    'alt_discount_amount': fields.Float
}


# API METHODS FOR SINGLE ENTITY
class ProductDetailsResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def get(self):
        try:

            action_type = 'GET'
            parser = reqparse.RequestParser()
            parser.add_argument('user_id')
            parser.add_argument('product_id')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = int(args['user_id'])
            product_id = int(args['product_id'])
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)
            product = session.query(Products).filter(Products.id == product_id).first()
            # products = products.
            if not product:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            if (product.brand_id != None):
                product.brand_data = session.query(BrandsCatalog).filter(BrandsCatalog.id == product.brand_id).first()

            if (product.partner_id != None):
                product.partner_data = session.query(PartnersCatalog).filter(
                    PartnersCatalog.id == product.partner_id).first()

            product.can_comments = False

            orders = session.query(Orders).filter(Orders.user_id == user_id).all()

            for order in orders:
                order_positions = session.query(OrderPositions).filter(
                    and_(
                        OrderPositions.order_id == order.id,
                        OrderPositions.product_id == product.id
                    )
                ).first()

                if (order_positions != None):
                    product.can_comments = True
                    break

            # comments = session.query(ProductComments).filter(
            #     ProductComments.product_id == product.id and ProductComments.is_delete == False).all()
            #
            # product.comments_count = 0
            # product.rate = 0
            #
            # if (comments != None):
            #     total_rate = 0
            #     comments_count = 0
            #     for comment in comments:
            #         total_rate += comment.rate
            #         comments_count += 1
            #
            #     if (comments_count > 0):
            #         product.comments_count = comments_count
            #         product.rate = round((total_rate / comments_count), 2)

                    # products.internal_products_count = len(products)
            attachments = []
            if (product.gallery_images != None):
                for a_id in product.gallery_images:
                    attachment = session.query(Attachments).filter(Attachments.id == a_id).first()
                    if (attachment != None):
                        attachments.append(attachment)

                product.gallery_images_data = attachments

            recommendations = []

            if product.product_recomendations is not None:
                for p_id in product.product_recomendations:
                    recommended_product = session.query(Products).filter(Products.id == p_id,
                                                                         Products.is_delete == False).first()
                    if recommended_product is not None:
                        # rec_comments = session.query(ProductComments) \
                        #     .filter(ProductComments.product_id == recommended_product.id,
                        #             ProductComments.is_delete == False).all()
                        # recommended_product.comments_count = 0
                        # recommended_product.rate = 0
                        # if rec_comments is not None:
                        #     rec_total_rate = 0
                        #     rec_comments_count = 0
                        #     for rec_comment in rec_comments:
                        #         rec_total_rate += rec_comment.rate
                        #         rec_comments_count += 1
                        #
                        #     if rec_comments_count > 0:
                        #         recommended_product.comments_count = rec_comments_count
                        #         recommended_product.rate = round((rec_total_rate / rec_comments_count), 2)
                        recommendations.append(recommended_product)

            product.product_recomendations_data = recommendations

            return product

        except Exception as e:
            abort(400, message="Product details Error")
            if (hasattr(e, 'data')):
                if (e.data != None and "message" in e.data):
                    abort(400, message=e.data["message"])
