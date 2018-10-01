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
    'order_id': fields.Integer,
    'count': fields.Float,
    'alt_count': fields.Float,
    'description': fields.String,
    'need_invoice': fields.String(
        attribute=lambda x: 'Да' if x.need_invoice else 'Нет'),
    'amount_per_item': fields.Float,
    'alt_amount_per_item': fields.Float,
    'amount_per_item_discount': fields.Float,
    'alt_amount_per_item_discount': fields.Float,
    'total_amount': fields.Float,
    'client_name': fields.String(
        attribute=lambda x: x.order_data.client_address_data.related_clients.name
        if x.order_data and x.order_data.client_address_data
           and x.order_data.client_address_data.related_clients
           and x.order_data.client_address_data.related_clients.name else '-'),
    'client_address': fields.String(
        attribute=lambda x: x.order_data.client_address_data.address
        if x.order_data and x.order_data.client_address_data
           and x.order_data.client_address_data.address else '-'),
    'client_address_name': fields.String(
        attribute=lambda x: x.order_data.client_address_data.name
        if x.order_data and x.order_data.client_address_data else '-'),
    'client_phone': fields.String(
        attribute=lambda x: x.order_data.client_address_data.phone_number
        if x.order_data and x.order_data.client_address_data
           and x.order_data.client_address_data.phone_number else '-'),
    'client_email': fields.String(
        attribute=lambda x: x.order_data.client_address_data.related_clients.client_info_data[0].email
        if x.order_data and x.order_data.client_address_data
           and x.order_data.client_address_data.related_clients
           and x.order_data.client_address_data.related_clients.client_info_data
           and len(x.order_data.client_address_data.related_clients.client_info_data) > 0
           and x.order_data.client_address_data.related_clients.client_info_data[0].email else '-'),
    'registration_number': fields.String(
        attribute=lambda x: x.order_data.client_address_data.related_clients.registration_number
        if x.order_data and x.order_data.client_address_data
           and x.order_data.client_address_data.related_clients else '-'),
    'client_id': fields.String(
        attribute=lambda x: x.order_data.client_address_data.client_id
        if x.order_data and x.order_data.client_address_data else 0),
    'client_address_id': fields.String(
        attribute=lambda x: x.order_data.client_address_id
        if x.order_data and x.order_data.client_address_id else 0),
    'name': fields.String(
        attribute=lambda x: x.product_data.name if x.product_data else '-'),
    'partner_id': fields.Integer(
        attribute=lambda x: x.product_data.partner_id if x.product_data else 0),
    'product_code': fields.String(
        attribute=lambda x: x.product_data.product_code if x.product_data else '-'),
    'is_stock_product': fields.Boolean(
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
            ['total_amount', 'currency_display_value'],
            ['need_invoice']
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

            titles = ["Наименование", "Артикул", "Количество", "Стоимость 1 ед.", "Скидка", "Итого", "Накладная"]
            sub_titles = ["Клиент", "Регистрация", "БИН/ИИН"]
            shop_sub_titles = ["Магазин", "Адрес", "Телефон"]
            docs = {}
            for position in positions:
                if position.get('partner_id', 0) != 0:
                    if position['partner_id'] in docs:
                        docs[position['partner_id']]['total'] += position['total_amount']
                        if position['client_id'] in docs[position['partner_id']]['clients']:
                            if position['client_address_id'] in \
                                    docs[position['partner_id']]['clients'][position['client_id']]['shops']:
                                docs[position['partner_id']]['clients'][position['client_id']]['shops'][
                                    position['client_address_id']]['positions'].append(position)
                                docs[position['partner_id']]['clients'][position['client_id']]['shops'][
                                    position['client_address_id']]['total'] += position['total_amount']
                            else:
                                docs[position['partner_id']]['clients'][position['client_id']]['shops'][
                                    position['client_address_id']] = {
                                    'name': position['client_address_name'],
                                    'address': position['client_address'],
                                    'phone': position['client_phone'],
                                    'total': position['total_amount'] or 0,
                                    'positions': [position]
                                }
                        else:
                            docs[position['partner_id']]['clients'][position['client_id']] = {
                                'name': position['client_name'],
                                'registration': position['registration_number'] or "",
                                'email': position['client_email'],
                                'shops': {position['client_address_id']: {
                                    'name': position['client_address_name'],
                                    'address': position['client_address'],
                                    'total': position['total_amount'] or 0,
                                    'phone': position['client_phone'],
                                    'positions': [position]
                                }}
                            }
                    else:
                        docs[position['partner_id']] = {
                            'name': position['partner_name'],
                            'total': position['total_amount'] or 0,
                            'currency': position['currency_display_value'],
                            'clients': {position['client_id']: {
                                'name': position['client_name'],
                                'registration': position['registration_number'] or "",
                                'email': position['client_email'],
                                'shops': {position['client_address_id']: {
                                    'name': position['client_address_name'],
                                    'address': position['client_address'],
                                    'total': position['total_amount'] or 0,
                                    'phone': position['client_phone'],
                                    'positions': [position]
                                }}
                            }}
                        }
            styles_dict = {
                'title': ['ota_title', 'ota_text'],
                'subtitle': ['ota_subtitle', 'ota_subtitle', 'ota_subtitle'],
                'subtitle_text': ['ota_text', 'ota_text', 'ota_text'],
                'shop_subtitle': ['shop_ota_subtitle', 'shop_ota_subtitle', 'shop_ota_subtitle'],
                'shop_subtitle_text': ['ota_text', 'ota_text', 'ota_text'],
                'header': ['ota_header', 'ota_header', 'ota_header', 'ota_header', 'ota_header',
                           'ota_header', 'ota_header'],
                'data_row': ['ota_text', 'ota_num', 'ota_num', 'ota_num', 'ota_num',
                             'ota_num', 'ota_text'],
                'total_row': ['ota_text', 'ota_text', 'ota_text', 'ota_text',
                              'ota_header', 'ota_header']
            }

            documents = {}
            dtnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            for key, document in docs.items():
                converted_data_rows = [[['ТН для {}'.format(document['name']), dtnow]]]
                names = [styles_dict['title']]
                for client in document['clients'].values():
                    names.append(styles_dict['subtitle'])
                    names.append(styles_dict['subtitle_text'])
                    converted_data_rows.append([sub_titles])
                    converted_data_rows.append([[client['name'], client.get('email', ""),
                                                 client.get('registration', "")]])
                    for shop in client['shops'].values():
                        names.append(styles_dict['shop_subtitle'])
                        names.append(styles_dict['shop_subtitle_text'])
                        converted_data_rows.append([shop_sub_titles])
                        converted_data_rows.append([[shop.get('name', ""),
                                                     shop.get('address', ""),
                                                     shop.get('phone', "")]])
                        names.append(styles_dict['header'])
                        converted_data_rows.append([titles])
                        for position in shop['positions']:
                            names.append(styles_dict['data_row'])
                            converted_data_rows.append([self.get_row(position)])

                        names.append(styles_dict['total_row'])
                        converted_data_rows.append(
                            [['', '', '', '', 'Итого', '{} {}'.format(shop['total'], document['currency'])]])

                names.append(styles_dict['total_row'])
                converted_data_rows.append(
                    [['', '', '', '', 'Сум. Итого', '{} {}'.format(document['total'], document['currency'])]])
                documents[key] = {
                    'name': document['name'],
                    'rows': converted_data_rows,
                    'styles': names
                }

            export_folder, export_path = documents_exporter.export_order_positions(documents)
            return send_from_directory(export_folder, export_path, as_attachment=True)


        except Exception as e:
            return {}
