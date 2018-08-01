from models.db_models.models import PartnersCatalog, UserCarts,UserCartPositions, Products
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_help_modules.user_action_logging_module as user_action_logging
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
from sqlalchemy import and_
import base64
import datetime
import models.app_models.setting_models.setting_model as settings
import urllib.parse
from sqlalchemy import desc
# PARAMS
ENTITY_NAME = "Check Minimum Sum Cart By Partners"
ROUTE = "/checkMinimumSumCartByPartners"
END_POINT = "check-minimum-sum-cart-by-partners"

# NESTED SCHEMA FIELDS

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,

}


# API METHODS FOR SINGLE ENTITY
class CheckMinimumSumCartByPartnersResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    # @marshal_with(output_fields)
    def get(self):
        error_message = ''
        try:
            action_type = 'GET'
            parser = reqparse.RequestParser()
            parser.add_argument('user_id')
            parser.add_argument('user_cart_id')

            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')

            user_id = args['user_id']
            user_cart_id = args['user_cart_id']
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)

            user_cart = session.query(UserCarts).filter(UserCarts.id == user_cart_id).first()
            if not user_cart:
                abort(400, message='Ошибка получения данных. Данные не найдены')

            user_cart_positions = session.query(UserCartPositions).filter(
                UserCartPositions.user_cart_id == user_cart.id).order_by(desc(UserCartPositions.id)).all()

            partner_ids =[]
            for position in user_cart_positions:
                product = session.query(Products).filter(Products.id==position.product_id).first()

                if (not product):
                    continue

                if (product.partner_id!=None):
                    partner = session.query(PartnersCatalog).filter(PartnersCatalog.id==product.partner_id).first()

                    if (partner!=None):
                        if (partner.minimum_order_amount!=None and partner.minimum_order_amount>0):
                            if (partner.id not in partner_ids):
                                partner_ids.append(partner.id)

            partner_sums =[]
            for id in partner_ids:

                partner = session.query(PartnersCatalog).filter(PartnersCatalog.id==id).first()

                if (not partner):
                    continue

                partner_sum = [partner.id, partner.name, partner.minimum_order_amount,0]
                partner_sums.append(partner_sum)

            for position in user_cart_positions:
                product = session.query(Products).filter(Products.id==position.product_id).first()
                if (product.partner_id!=None):
                    for partner_sum in partner_sums:
                        if (partner_sum[0]==product.partner_id):
                            count = position.count
                            alt_count = position.alt_count
                            if (alt_count==None):
                                alt_count=0
                            single_amount = product.amount
                            alt_single_amount = product.alt_amount
                            if (alt_single_amount==None):
                                alt_single_amount = 0
                            amount = count*single_amount
                            alt_amount = alt_single_amount*alt_count
                            t_amount = amount+alt_amount
                            partner_sum[3]+=t_amount
                            break


            result_arr =[]

            for partner_sum in partner_sums:
                if (partner_sum[2]>partner_sum[3]):
                    result_arr.append(partner_sum)




            return result_arr
        except Exception as e:
            abort(400, message=error_message)
