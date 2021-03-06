from models.db_models.models import Users, UserBonuses, UserLogins,UserInfo,UserCarts,UserCartPositions,Products,CurrencyCatalog
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.image_path_converter_modules.image_path_converter as image_path_converter
from sqlalchemy import desc
#PARAMS
ENTITY_NAME = "Manage Users Cart Details"
MODEL = Users
ROUTE ="/manageUserCartDetails"
END_POINT = "manage-user-cart-details"

# NESTED SCHEMA FIELDS
currency_data_fields = {
    'id': fields.Integer,
    'system_name': fields.String,
    'display_value': fields.String,
    'name': fields.String,
    'is_default': fields.Boolean
}

partner_data_fields = {
    'id': fields.Integer,
    'name': fields.String
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

product_data_fields ={
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
    'product_unit_data': fields.Nested(unit_data_fields),
    'product_currency_data': fields.Nested(currency_data_fields),
    'product_alt_unit_data': fields.Nested(unit_data_fields),
    'alt_amount': fields.Float,
    'alt_unit_value': fields.Float,
    'alt_unit_id': fields.Integer,
    'alt_discount_amount': fields.Float,
    'partner_data': fields.Nested(partner_data_fields)

}

user_cart_positions_fields ={
    'id': fields.Integer,
    'product_id': fields.Integer,
    'count': fields.Float,
    'alt_count':fields.Float,
    'need_invoice': fields.Boolean,
    'description': fields.String,
    'user_cart_id':fields.Integer,
    'user_cart_position_product_data':fields.Nested(product_data_fields),
    'bonuses': fields.Float
}

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,

    'cart_state_id':fields.Integer,
    'products_count': fields.Integer,
    'total_amount': fields.Float,
    'total_amount_without_discount': fields.Float,
    'discount_amount':fields.Float,
    'currency_data': fields.Nested(currency_data_fields),
    'economy_delta': fields.Float,
    'economy_percent': fields.Float,
    'cart_positions': fields.Nested(user_cart_positions_fields),
    'bonuses_amount':fields.Float
}

#API METHODS FOR SINGLE ENTITY
class ManageUserCartDetailsResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    @marshal_with(output_fields)
    def post(self):
        try:

            action_type='POST'
            json_data = request.get_json(force=True)

            user_cart_id = json_data['id']
            cart_positions = json_data['cart_positions']
            # user_action_logging.log_user_actions(ROUTE, user_id, action_type)

            db_cart_positions = session.query(UserCartPositions).filter(UserCartPositions.user_cart_id==user_cart_id).order_by(desc(UserCartPositions.id)).all()

            remove_cart_position_indexes =[]
            #проверяем все ли элементы корзины из реальной БД есть в той, что пришла
            for db_cart_position in db_cart_positions:
                founded =False
                for cart_position in cart_positions:
                    m_cart_position_id =cart_position['id']
                    if (m_cart_position_id==db_cart_position.id):
                        founded=True
                        break

                if (founded==False):
                    remove_cart_position_indexes.append(db_cart_position.id)

            #удаляем все позиции которые были удалены на стороне клиента
            for remove_cart_position_index in remove_cart_position_indexes:
                entity = session.query(UserCartPositions).filter(UserCartPositions.id == remove_cart_position_index).first()
                if not entity:
                    continue
                session.delete(entity)
                session.commit()

            total_bonuses = 0
            for position in cart_positions:
                position_args ={}
                position_args['id'] = position['id']
                position_args['count'] = position['count']
                position_args['alt_count'] = position['alt_count']
                position_args['description'] = position['description']
                position_args['need_invoice'] = position['need_invoice']

                db_position = session.query(UserCartPositions).filter(UserCartPositions.id==position_args['id']).first()

                if (not db_position):
                    continue

                db_transformer.transform_update_params(db_position, position_args)
                session.add(db_position)
                session.commit()

            user_cart = session.query(UserCarts).filter(UserCarts.id==user_cart_id).first()
            if not user_cart:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            user_cart_positions = session.query(UserCartPositions).filter(UserCartPositions.user_cart_id==user_cart.id).all()
            # for cart_position in cart_positions:
            #     cart_position

            user_cart.cart_positions = user_cart_positions
            total_sum = 0
            total_sum_without_discount = 0

            amount_sum = 0
            currency_id = -1

            for cart_position in user_cart_positions:
                count = cart_position.count
                alt_count = cart_position.alt_count

                cart_position.bonus =0
                product = session.query(Products).filter(Products.id == cart_position.product_id).first()
                if (currency_id == -1):
                    currency_id = product.currency_id

                if (not product):
                    continue

                if (product.alt_discount_amount == None):
                    product.alt_discount_amount = 0

                if (product.alt_amount == None):
                    product.alt_amount = 0

                cart_position.bonuses =0
                if (cart_position.count!=0):
                    bonus =product.amount* (product.bonus_percent/100)*cart_position.count
                    bonus+=product.alt_amount*(product.bonus_percent/100)*cart_position.alt_count
                    bonus = round(bonus,2)
                    if (bonus != None):
                        cart_position.bonuses = bonus
                        total_bonuses+=bonus

                single_amount = 0
                if (product.is_discount_product == True):
                    discount_amount = product.discount_amount
                    alt_discount_amount = product.alt_discount_amount

                    if (discount_amount == 0):
                        discount_amount = product.amount

                    if (alt_discount_amount == None or alt_discount_amount == 0):
                        alt_discount_amount = product.alt_amount

                    if (discount_amount == 0):
                        discount_amount = product.amount

                    single_amount = round(discount_amount * count, 2)
                    alt_single_amount = round(alt_discount_amount * alt_count, 2)

                    total_sum += single_amount
                    total_sum += alt_single_amount

                    total_sum_without_discount += round(product.amount * count, 2)
                    total_sum_without_discount += round(product.alt_amount * alt_count, 2)

                    delta = product.amount - discount_amount
                    alt_delta = product.alt_amount - alt_discount_amount

                    amount_sum += round(delta * count, 2)
                    amount_sum += round(alt_delta * alt_count, 2)

                else:
                    total_sum += round(product.amount * count, 2)
                    total_sum += round(product.alt_amount * alt_count, 2)
                    total_sum_without_discount += round(product.amount * count, 2)
                    total_sum_without_discount += round(product.alt_amount * alt_count, 2)

            economy_delta = total_sum_without_discount - amount_sum
            economy_percent = round(100 * (economy_delta / total_sum_without_discount), 2)

            user_cart.total_amount = total_sum
            user_cart.total_amount_without_discount = total_sum_without_discount
            user_cart.discount_amount = amount_sum
            user_cart.economy_delta = economy_delta
            user_cart.economy_percent = economy_percent
            user_cart.products_count = len(user_cart_positions)
            user_cart.currency_data = session.query(CurrencyCatalog).filter(CurrencyCatalog.id == currency_id).first()
            user_cart.bonuses_amount=round(total_bonuses,2)
            return user_cart

        except Exception as e:
            if (hasattr(e,'data')):
                if (e.data!=None and "message" in e.data):
                    abort(400,message =e.data["message"])
            abort(400, message = "Неопознанная ошибка")



