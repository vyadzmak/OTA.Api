from models.db_models.models import Orders
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
from sqlalchemy import desc
from flask import Flask, make_response, send_from_directory, send_file
from flask import Response
import urllib.parse as urllib
from decimal import Decimal
from re import sub
import xlsxwriter
import json
from models.app_models.setting_models.setting_model import EXPORTS_FOLDER
import modules.documents_exporter.export_document_formatter as formatter

import os
import uuid
import unicodedata
import string
from transliterate import translit, get_available_language_codes

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
import datetime
import zlib
import base64
import copy
import json
import zipfile
import shutil


def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r, '_')

    filename = filename.replace('(', '')
    filename = filename.replace(')', '')
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    return ''.join(c for c in cleaned_filename if c in whitelist)


def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode()  # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value  # Instance of bytes


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode()  # uses 'utf-8' for encoding
    else:
        value = bytes_or_str
    return value  # Instance of str


def export_cells(worksheet, data, styles):
    try:
        # row, col, value
        row_index = 0
        cell_index = 0

        for row in data:

            for cell_line in row:
                row_index += 1
                cell_index = 0
                for cell in cell_line:
                    cell_index += 1

                    value = cell
                    _format = styles[row_index - 1][cell_index - 1]
                    if (_format != None):
                        worksheet.write(row_index - 1, cell_index - 1, value, _format)
                    else:
                        worksheet.write(row_index - 1, cell_index - 1, value)
    except Exception as e:
        raise e


def make_archive(source, destination):
    try:
        zip_loc = source
        zip_dest = destination
        shutil.make_archive(zip_loc, 'zip', zip_dest)
        shutil.rmtree(zip_loc, ignore_errors=True)
    except Exception as e:
        pass


# def export_order_positions(documents, sub_titles, titles, styles_dict):
#     try:
#
#         if (not documents):
#             return None
#
#         dir_id = str(uuid.uuid4().hex)
#         exports_folder = os.path.join(EXPORTS_FOLDER, dir_id)
#         if not os.path.exists(exports_folder):
#             os.makedirs(exports_folder)
#         dtnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
#
#         for document in documents.values():
#
#             partner_name = str(document['name']).replace('"', ' ')
#             partner_name = translit(partner_name, 'ru', reversed=True)
#
#             dtnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
#             dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             dt = str(dt).replace('-', '')
#             partner_name = partner_name + "_" + str(dt)
#
#             file_name = clean_filename(partner_name)
#             file_name = file_name.replace('__', "_")
#             file_path = os.path.join(exports_folder, file_name + ".xlsx")
#
#             if (len(file_path) > 255):
#                 file_path = os.path.join(exports_folder, dir_id + ".xlsx")
#             converted_data_rows = [[['ТН для {}'.format(document['name']), dtnow]]]
#             names = [styles_dict['title']]
#             for client_name, positions in document['positions'].items():
#                 names.append(styles_dict['subtitle'])
#                 names.append(styles_dict['subtitle_text'])
#                 names.append(styles_dict['header'])
#                 for i in range(len(positions)):
#                     names.append(styles_dict['data_row'])
#                 converted_data_rows.append([sub_titles])
#                 converted_data_rows.append([[client_name, document.get('client_emails', None).get(client_name, ''),
#                                              document.get('client_registrations', None).get(client_name, '')]])
#                 converted_data_rows.append([titles])
#                 converted_data_rows.append(positions)
#
#             names.append(styles_dict['total_row'])
#             converted_data_rows.append(
#                 [['', '', '', '', '', '', '', 'Итого', '{} {}'.format(document['total'], document['currency'])]])
#
#             workbook = xlsxwriter.Workbook(file_path)
#             sheet_name = document['name'][:28]
#             worksheet = workbook.add_worksheet(sheet_name)
#             widths = formatter.get_column_widths(converted_data_rows)
#             styles = formatter.generate_worksheet_styles(workbook, names)
#             index = 0
#             for width in widths:
#                 worksheet.set_column(index, index, width)
#                 index += 1
#
#             export_cells(worksheet, converted_data_rows, styles)
#             workbook.close()
#
#         zip_name = exports_folder
#         make_archive(exports_folder, zip_name)
#
#         return EXPORTS_FOLDER, str(dir_id) + ".zip"
#         pass
#     except Exception as e:
#         pass

def export_order_positions(documents):
    try:

        if (not documents):
            return None

        dir_id = str(uuid.uuid4().hex)
        exports_folder = os.path.join(EXPORTS_FOLDER, dir_id)
        if not os.path.exists(exports_folder):
            os.makedirs(exports_folder)

        for document in documents.values():

            partner_name = str(document['name']).replace('"', ' ')
            partner_name = translit(partner_name, 'ru', reversed=True)

            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dt = str(dt).replace('-', '')
            partner_name = partner_name + "_" + str(dt)

            file_name = clean_filename(partner_name)
            file_name = file_name.replace('__', "_")
            file_path = os.path.join(exports_folder, file_name + ".xlsx")

            if (len(file_path) > 255):
                file_path = os.path.join(exports_folder, dir_id + ".xlsx")

            workbook = xlsxwriter.Workbook(file_path)
            sheet_name = document['name'][:28]
            worksheet = workbook.add_worksheet(sheet_name)
            widths = formatter.get_column_widths(document['rows'])
            styles = formatter.generate_worksheet_styles(workbook, document['styles'])
            index = 0
            for width in widths:
                worksheet.set_column(index, index, width)
                index += 1

            export_cells(worksheet, document['rows'], styles)
            workbook.close()

        zip_name = exports_folder
        make_archive(exports_folder, zip_name)

        return EXPORTS_FOLDER, str(dir_id) + ".zip"
        pass
    except Exception as e:
        pass
