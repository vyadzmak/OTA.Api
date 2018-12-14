from models.db_models.models import Orders
from db.db import session
from flask_restful import Resource, fields, marshal, abort, reqparse
from flask import send_from_directory
import datetime
import modules.documents_exporter.documents_exporter as documents_exporter
import modules.db_help_modules.user_action_logging_module as user_action_logging

# NESTED SCHEMA FIELDS
# OUTPUT SCHEMA
output_fields = {
    'id': fields.Integer,
    'creation_date': fields.DateTime,
    'number': fields.String,
    'total_amount': fields.Float,
    'order_state_id': fields.Integer,
    'currency_display_value': fields.String(
        attribute=lambda x: x.currency_data.display_value
        if x.currency_data else '-'),
    'client_name': fields.String(
        attribute=lambda x: x.client_address_data.related_clients.name
        if x.client_address_data
           and x.client_address_data.related_clients
           and x.client_address_data.related_clients.name else '-'),
    'client_address': fields.String(
        attribute=lambda x: x.client_address_data.address
        if x.client_address_data
           and x.client_address_data.address else '-'),
    'client_address_code': fields.String(
        attribute=lambda x: x.client_address_data.code
        if x.client_address_data else '-'),
    'client_city_name': fields.String(
        attribute=lambda x: x.client_address_data.city_data.name
        if x.client_address_data
           and x.client_address_data.city_data else '-'),
    'client_area_name': fields.String(
        attribute=lambda x: x.client_address_data.city_data.area_data.name
        if x.client_address_data
           and x.client_address_data.city_data
           and x.client_address_data.city_data.area_data else '-'),
}
# PARAMS
ENTITY_NAME = "Export Orders By Date"
ROUTE = "/exportOrdersByDate"
END_POINT = "export-orders-by-date"


class ExportOrdersByDateResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    def get_row(self, position):
        cols = [
            ['creation_date'],
            ['number'],
            ['client_name'],
            ['client_area_name'],
            ['client_city_name'],
            ['client_address'],
            ['client_address_code'],
            ['total_amount', 'currency_display_value']
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
            parser.add_argument('order_state_ids')
            parser.add_argument('date_from')
            parser.add_argument('date_to')
            args = parser.parse_args()
            if (len(args) == 0):
                abort(400, message='Arguments not found')
            user_id = args['user_id']
            order_state_ids = [int(x) for x in args['order_state_ids'].split(',')]
            date_from = args['date_from']
            date_to = args['date_to']
            user_action_logging.log_user_actions(ROUTE, user_id, action_type)

            orders = session.query(Orders) \
                .filter(Orders.order_state_id.in_(order_state_ids),
                        Orders.creation_date > date_from, Orders.creation_date < date_to) \
                .order_by(Orders.id).all()

            if not orders:
                abort(404, message="Positions {} doesn't exist".format(id))

            titles = ["Дата", "Номер заявки", "Клиент", "Регион/Область", "Город/а.е.", "Адрес", "Менеджер", "Сумма"]
            marshalled_orders = marshal(orders, output_fields)

            styles_dict = {
                'title': ['ota_title', 'ota_text'],
                'subtitle': ['ota_subtitle', 'ota_subtitle'],
                'header': ['ota_header', 'ota_header', 'ota_header', 'ota_header', 'ota_header',
                           'ota_header', 'ota_header', 'ota_header'],
                'data_row': ['ota_text', 'ota_text', 'ota_text', 'ota_text', 'ota_text',
                             'ota_text', 'ota_text', 'ota_num'],
                'total_row': ['ota_text', 'ota_text', 'ota_text', 'ota_text', 'ota_text',
                              'ota_text', 'ota_header', 'ota_header']
            }

            documents = {}
            dtnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            converted_data_rows = [
                [['Выгрузка заказов', dtnow]],
                [['Период', '{}/{}'.format(date_from, date_to)]]
            ]
            names = [styles_dict['title']]
            names.append(styles_dict['subtitle'])
            names.append(styles_dict['header'])
            converted_data_rows.append([titles])
            total_sum = 0
            for order in marshalled_orders:
                order['creation_date'] = datetime.datetime.strptime(order['creation_date'],
                                                                    '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
                names.append(styles_dict['data_row'])
                converted_data_rows.append([self.get_row(order)])
                total_sum += order['total_amount']
            currency_display_value = marshalled_orders[0]['currency_display_value'] if len(
                marshalled_orders) > 0 else ''
            names.append(styles_dict['total_row'])
            converted_data_rows.append(
                [['', '', '', '', '', '', 'Итого', '{} {}'.format(total_sum, currency_display_value)]])

            documents['1'] = {
                'name': 'Выгрузка данных',
                'rows': converted_data_rows,
                'styles': names
            }

            export_folder, export_path = documents_exporter.export_order_positions(documents, 5)
            return send_from_directory(export_folder, export_path, as_attachment=True)

        except Exception as e:
            return {}
