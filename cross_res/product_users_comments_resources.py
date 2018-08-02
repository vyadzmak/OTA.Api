from models.db_models.models import Products, ProductComments, Attachments,Orders,OrderPositions,UserInfo
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import desc
from sqlalchemy import and_
# PARAMS
ENTITY_NAME = "Product User Comments"
MODEL = ProductComments
ROUTE = "/productUsersComments"
END_POINT = "product-users-comments"

# NESTED SCHEMA FIELDS
avatar_image_data_fields = {
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

user_data_fields = {
    'id': fields.Integer(attribute="id"),
    'name': fields.String(attribute="name"),
    'avatar':fields.Nested(avatar_image_data_fields)
}

comment_fields = {
    'id': fields.Integer,
    'user_id':fields.Integer,
    'creation_date': fields.String(
        attribute=lambda x: x.creation_date.strftime("%Y-%m-%d %H:%M") if x.creation_date is not None else ''),
    'comment_text':fields.String,
    'rate':fields.Float,
    'is_delete':fields.Boolean,
    'product_id':fields.Integer,
    'comment_user_data':fields.Nested(user_data_fields),
}
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'can_comments':fields.Boolean,
    'comments': fields.Nested(comment_fields),
    'rate':fields.Float,
    'comments_count':fields.Integer
}


# API METHODS FOR SINGLE ENTITY
class ProductUsersCommentsResource(Resource):
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

            product.can_comments =False

            orders = session.query(Orders).filter(Orders.user_id==user_id).all()

            for order in orders:
                order_positions = session.query(OrderPositions).filter(
                    and_(
                        OrderPositions.order_id == order.id,
                        OrderPositions.product_id == product.id
                    )
                ).first()

                if (order_positions!=None):
                    product.can_comments =True
                    break


            comments = session.query(ProductComments).filter(
                ProductComments.product_id == product.id).order_by(desc(ProductComments.creation_date)).all()

            product.comments = comments
            product.comments_count = 0
            product.rate = 0




            if (not comments):
                product.comments=[]


            if (product.comments != None):
                total_rate = 0
                comments_count = 0
                for comment in product.comments:
                    total_rate += comment.rate
                    comments_count += 1

                    user_id = comment.user_id
                    user_info = session.query(UserInfo).filter(UserInfo.user_id==user_id).first()

                    if (not user_info):
                        continue

                    avatar_id = user_info.avatar_id

                    if (avatar_id!=None):
                        avatar = session.query(Attachments).filter(Attachments.id==avatar_id).first()
                        if (not avatar):
                            continue

                        comment.comment_user_data.avatar = avatar


                if (comments_count > 0):
                    product.comments_count = comments_count
                    product.rate = round((total_rate / comments_count), 2)




            return product

        except Exception as e:
            abort(400, message="Product details Error")
            if (hasattr(e, 'data')):
                if (e.data != None and "message" in e.data):
                    abort(400, message=e.data["message"])
