from models.db_models.models import OrderPositions, PartnersCatalog, Products
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal, abort, reqparse
from sqlalchemy import desc
from flask import Flask, make_response, send_from_directory, send_file
from flask import Response
import urllib.parse as urllib
import modules.documents_exporter.documents_exporter as documents_exporter
import modules.db_help_modules.user_action_logging_module as user_action_logging

# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'product_id': fields.Integer,
    'order_id': fields.Integer,
    'count': fields.Float,
    'alt_count': fields.Float,
    'description': fields.String,
    'need_invoice': fields.Boolean,
    'amount_per_item': fields.Float,
    'alt_amount_per_item': fields.Float,
    'amount_per_item_discount': fields.Float,
    'alt_amount_per_item_discount': fields.Float,
    'total_amount': fields.Float,
    'client_name': fields.String(
        attribute=lambda x: x.order_data.client_address_data.related_clients.name
            if x.order_data else ''),
    'name': fields.String(
        attribute=lambda x: x.product_data.name if x.product_data else ''),
    'partner_id': fields.Integer(
        attribute=lambda x: x.product_data.partner_id if x.product_data else 0),
    'product_code': fields.String(
        attribute=lambda x: x.product_data.product_code if x.product_data else ''),
    'is_stock_product': fields.Boolean(
        attribute=lambda x: x.product_data.is_stock_product if x.product_data else False),
    'unit_display_value': fields.String(
        attribute=lambda x: x.product_data.product_unit_data.display_value
        if x.product_data and x.product_data.product_unit_data else ''),
    'alt_unit_display_value': fields.String(
        attribute=lambda x: x.product_data.product_data.product_alt_unit_data.display_value
        if x.product_data and x.product_data.product_alt_unit_data else ''),
    'currency_display_value': fields.String(
        attribute=lambda x: x.product_data.product_currency_data.display_value
        if x.product_data and x.product_data.product_currency_data else ''),
    'partner_name': fields.String(
        attribute=lambda x: x.product_data.partner_data.name
        if x.product_data and x.product_data.partner_data else '')
}

# PARAMS
ENTITY_NAME = "Export Orders"
ROUTE = "/exportOrders"
END_POINT = "export-orders"


class ExportOrdersResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    def get_row(self, position):
        cols = [
            ['name'],
            ['product_code'],
            ['count', 'unit_display_value'],
            ['amount_per_item', 'currency_display_value'],
            ['amount_per_item_discount', 'currency_display_value'],
            ['alt_count', 'unit_display_value'],
            ['alt_amount_per_item', 'currency_display_value'],
            ['alt_amount_per_item_discount', 'currency_display_value'],
            ['total_amount', 'currency_display_value'],
            ['client_name']
        ]

        return [position.get(col[0], "-") if len(col) == 1
                else '{}{}'.format(position[col[0]] or 0, position[col[1]])
                for col in cols]

    def get(self):
        try:
            action_type = 'GET'
            parser = reqparse.RequestParser()
            parser.add_argument('user_id')
            parser.add_argument('orders_ids')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            orders_ids = args['orders_ids']
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)

            positions = session.query(OrderPositions) \
                .filter(OrderPositions.order_id.in_([17]),
                        OrderPositions.order_position_state_id != 2).all()

            if not positions:
                abort(404, message="Positions {} doesn't exist".format(id))
            positions = marshal(positions, output_fields)
            titles = ["Наименование", "Артикул", "Количество", "Стоимость 1 ед.", "Скидка",
                      "Количество", "Стоимость 1 ед.", "Скидка", "Итого", "Заказчик"]
            docs = {}
            for position in positions:
                if position.get('partner_id', 0) != 0:
                    if position['partner_id'] in docs:
                        docs[position['partner_id']]['total'] += (position['total_amount'] or 0)
                        docs[position['partner_id']]['positions'].append(self.get_row(position))
                    else:
                        docs[position['partner_id']] = {
                            'name': position['partner_name'],
                            'total': position['total_amount'] or 0,
                            'currency':position['currency_display_value'],
                            'positions': [self.get_row(position)]
                        }

            export_folder, export_path = documents_exporter.export_order_positions(docs, titles)
            return send_from_directory(export_folder,export_path, as_attachment=True)


        except Exception as e:
            return {}
