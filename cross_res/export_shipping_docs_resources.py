from models.db_models.models import OrderPositions
from db.db import session
from flask_restful import Resource, fields, marshal, abort, reqparse
from flask import send_from_directory
import datetime
import modules.documents_exporter.documents_exporter as documents_exporter
import modules.db_help_modules.user_action_logging_module as user_action_logging

output_fields = {
    'id': fields.Integer,
    'product_id': fields.Integer,
    'count': fields.Float(default=0),
    'alt_count': fields.Float(default=0),
    'amount_per_item': fields.Float(default=0),
    'alt_amount_per_item': fields.Float(default=0),
    'amount_per_item_discount': fields.Float(default=0),
    'alt_amount_per_item_discount': fields.Float(default=0),
    'total_amount': fields.Float(default=0),
    'name': fields.String(
        attribute=lambda x: x.product_data.name if x.product_data else '-'),
    'partner_id': fields.Integer(
        attribute=lambda x: x.product_data.partner_id if x.product_data else 0),
    'product_code': fields.String(
        attribute=lambda x: x.product_data.product_code if x.product_data else '-'),
    'is_stock_product': fields.String(
        attribute=lambda x: 'Да' if x.product_data and x.product_data.is_stock_product else 'Нет'),
    'unit_display_value': fields.String(
        attribute=lambda x: x.product_data.product_unit_data.display_value
        if x.product_data and x.product_data.product_unit_data
           and x.product_data.product_unit_data.display_value else '-'),
    'alt_unit_display_value': fields.String(
        attribute=lambda x: x.product_data.product_alt_unit_data.display_value
        if x.product_data and x.product_data.product_alt_unit_data else '-'),
    'currency_display_value': fields.String(
        attribute=lambda x: x.product_data.product_currency_data.display_value
        if x.product_data and x.product_data.product_currency_data
           and x.product_data.product_currency_data.display_value else '-'),
    'partner_name': fields.String(
        attribute=lambda x: x.product_data.partner_data.name
        if x.product_data and x.product_data.partner_data
           and x.product_data.partner_data.name else '-')
}

# PARAMS
ENTITY_NAME = "Export Shipping Docs"
ROUTE = "/exportShippingDocs"
END_POINT = "export-shipping-docs"


class ExportShippingDocsResource(Resource):
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
            ['total_amount', 'currency_display_value'],
            ['is_stock_product']
        ]
        rr = [position.get(col[0], "-") if len(col) == 1
              else '{} {}'.format(position[col[0]] or 0, position[col[1]])
              for col in cols]
        return rr

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
            orders_ids = [int(x) for x in args['orders_ids'].split(',')]
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)

            positions = session.query(OrderPositions) \
                .filter(OrderPositions.order_id.in_(orders_ids),
                        OrderPositions.order_position_state_id != 2).all()

            if not positions:
                abort(404, message="Positions {} doesn't exist".format(id))
            marshlled_positions = marshal(positions, output_fields)

            curr_keys = ['count', 'amount_per_item', 'unit_display_value', 'amount_per_item_discount']
            alt_keys = ['alt_count', 'alt_amount_per_item', 'alt_unit_display_value', 'alt_amount_per_item_discount']

            positions = []
            for pos in marshlled_positions:
                if pos['count'] > 0:
                    curr_pos = pos.copy()
                    for alt_key in alt_keys:
                        curr_pos.pop(alt_key)
                    if curr_pos['amount_per_item_discount'] > 0:
                        curr_pos['amount_per_item_discount'] = curr_pos['amount_per_item'] - curr_pos[
                            'amount_per_item_discount']
                    curr_pos['total_amount'] = curr_pos['count'] * (
                        curr_pos['amount_per_item'] - curr_pos['amount_per_item_discount'])
                    positions.append(curr_pos)
                if pos['alt_count'] > 0:
                    curr_pos = pos.copy()
                    change_dict = dict(zip(curr_keys, alt_keys))
                    for curr_key, alt_key in change_dict.items():
                        curr_pos[curr_key] = curr_pos[alt_key]
                    for alt_key in alt_keys:
                        curr_pos.pop(alt_key)
                    if curr_pos['amount_per_item_discount'] > 0:
                        curr_pos['amount_per_item_discount'] = curr_pos['amount_per_item'] - curr_pos[
                            'amount_per_item_discount']
                    curr_pos['total_amount'] = curr_pos['count'] * (
                        curr_pos['amount_per_item'] - curr_pos['amount_per_item_discount'])
                    positions.append(curr_pos)
            if len(positions) == 0:
                return "All products have 0 count. Nothing to download."

            titles = ["Наименование", "Артикул", "Количество", "Стоимость 1 ед.", "Скидка", "Итого", "Акция"]
            docs = {}
            for position in positions:
                if position.get('partner_id', 0) != 0:
                    if position['partner_id'] in docs:
                        docs[position['partner_id']]['total'] += position['total_amount']
                        if '{}-{}-{}-{}'.format(position['product_id'],
                                                '1' if position['is_stock_product'] else '0',
                                                position['amount_per_item'],
                                                position['amount_per_item_discount'],
                                                position['unit_display_value']) in docs[position['partner_id']][
                            'positions']:
                            docs[position['partner_id']]['positions']['{}-{}-{}-{}'.format(position['product_id'],
                                                  '1' if position['is_stock_product'] else '0',
                                                  position['amount_per_item'],
                                                  position['amount_per_item_discount'],
                                                  position['unit_display_value'])]['total_amount'] += position['total_amount']
                            docs[position['partner_id']]['positions']['{}-{}-{}-{}'.format(position['product_id'],
                                              '1' if position['is_stock_product'] else '0',
                                              position['amount_per_item'],
                                              position['amount_per_item_discount'],
                                              position['unit_display_value'])]['count'] += position['count']
                        else:
                            docs[position['partner_id']]['positions']['{}-{}-{}-{}'.format(position['product_id'],
                                                                                       '1' if position[
                                                                                           'is_stock_product'] else '0',
                                                                                       position['amount_per_item'],
                                                                                       position[
                                                                                           'amount_per_item_discount'],
                                                                                       position[
                                                                                           'unit_display_value'])] = position

                    else:
                        docs[position['partner_id']] = {
                            'name': position['partner_name'],
                            'total': position['total_amount'] or 0,
                            'currency': position['currency_display_value'],
                            'positions': {
                                '{}-{}-{}-{}'.format(position['product_id'],
                                                          '1' if position['is_stock_product'] else '0',
                                                          position['amount_per_item'],
                                                          position['amount_per_item_discount'],
                                                          position['unit_display_value']): position
                            }
                        }


            styles_dict = {
                'title': ['ota_title', 'ota_text'],
                'subtitle': ['ota_subtitle', 'ota_subtitle', 'ota_subtitle'],
                'subtitle_text': ['ota_text', 'ota_text', 'ota_text'],
                'shop_subtitle': ['shop_ota_subtitle', 'shop_ota_subtitle', 'shop_ota_subtitle', 'shop_ota_subtitle',
                                  'shop_ota_subtitle'],
                'shop_subtitle_text': ['ota_text', 'ota_text', 'ota_text', 'ota_text', 'ota_text'],
                'header': ['ota_header', 'ota_header', 'ota_header', 'ota_header', 'ota_header',
                           'ota_header', 'ota_header'],
                'data_row': ['ota_text', 'ota_num', 'ota_num', 'ota_num', 'ota_num',
                             'ota_num', 'ota_text', 'ota_text'],
                'total_row': ['ota_text', 'ota_text', 'ota_text', 'ota_text',
                              'ota_header', 'ota_header']
            }

            documents = {}
            dtnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            for key, document in docs.items():
                converted_data_rows = [[['Погрузочный лист для {}'.format(document['name']), dtnow]]]
                names = [styles_dict['title']]
                names.append(styles_dict['header'])
                converted_data_rows.append([titles])
                for position in document['positions'].values():
                    names.append(styles_dict['data_row'])
                    converted_data_rows.append([self.get_row(position)])

                names.append(styles_dict['total_row'])
                converted_data_rows.append(
                    [['', '', '', '', 'Сум. Итого', '{} {}'.format(document['total'], document['currency'])]])
                documents[key] = {
                    'name': document['name'],
                    'rows': converted_data_rows,
                    'styles': names
                }

            export_folder, export_path = documents_exporter.export_order_positions(documents, 3)
            return send_from_directory(export_folder, export_path, as_attachment=True)

        except Exception as e:
            return {}
