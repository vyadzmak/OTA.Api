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


def convert_document(data):
    try:
        rows = data["rows"][0]["cells"][0]["tableData"]["items"]
        headers = data["rows"][0]["cells"][0]["tableData"]["headers"]
        tt = 0
        titles = []
        names = []

        for header in headers:
            titles.append(header["text"])
            if (header["value"] != 'indicators'):
                names.append(header["value"])

        index = 0
        r_index = -1
        for title in titles:
            if (title == '*' and index == 0):
                titles[index] = 'Наименование'

            if (title == '*' and index > 0):
                r_index = index
                break

            index += 1
        if (r_index != -1):
            titles.remove(titles[r_index])

        export_rows = []

        for row in rows:
            _row = []
            for name in names:
                if (name in row):
                    value = row[name]

                    if (name == 'valueDebet' or name == 'valueCredit'):
                        # pass
                        value = value.replace(',', '')
                        # value = value.replace('.',',')

                    _row.append(value)

            export_rows.append(_row)
        result_rows = []

        result_rows.append([titles])
        result_rows.append(export_rows)
        t = 0
        return names, result_rows
    except Exception as e:
        return None


def get_widths(index, cells):
    # widths =[]
    # for cell in cells:
    #     row = int(cell["row"])
    #     sheet = int(cell["sheet"])
    #     col = int(cell["col"])
    #     if (row==0 and sheet==index):
    #         s_width = 6
    #         if (col==1):
    #             s_width = 8
    #         width =round(int(cell["json"]["width"])/s_width,1)
    #         widths.append(width)
    #
    # return widths
    pass


def export_cells(worksheet, data):
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
                    _format = None
                    if (_format != None):
                        worksheet.write(row - 1, cell_index - 1, value, _format)
                    else:
                        worksheet.write(row_index - 1, cell_index - 1, value)
    except Exception as e:
        pass


def export_single_document(document):
    try:

        if (not document):
            return None

        dir_id = str(uuid.uuid4().hex)
        partner_folder = os.path.join(EXPORTS_FOLDER, dir_id)
        if not os.path.exists(partner_folder):
            os.makedirs(partner_folder)

        s_cmpstr = copy.deepcopy(document.data)
        bc = s_cmpstr.count("b'")

        s_cmpstr = s_cmpstr.replace("b'", "", 1)
        qc = s_cmpstr.count("'")

        s_cmpstr = s_cmpstr.replace("'", "")
        b_cmpstr = to_bytes(s_cmpstr)
        b_cmpstr = base64.b64decode(b_cmpstr)
        rr = to_str(zlib.decompress(b_cmpstr))
        f_cmpstr = rr
        # f_cmpstr = f_cmpstr.replace("'", "")
        data = json.loads(f_cmpstr)

        names, converted_data_rows = convert_document(data)

        project_name = str(document.file_name).replace('"', ' ')
        project_name = translit(project_name, 'ru', reversed=True)

        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dt = str(dt).replace('-', '')
        project_name = project_name + "_" + str(dt)

        file_name = clean_filename(project_name)
        file_name = file_name.replace('__', "_")
        file_path = os.path.join(partner_folder, file_name + ".xlsx")

        if (len(file_path) > 255):
            file_path = os.path.join(partner_folder, dir_id + ".xlsx")

        workbook = xlsxwriter.Workbook(file_path)
        sheet_name = 'Data'
        worksheet = workbook.add_worksheet(sheet_name)
        widths = formatter.get_column_widths(converted_data_rows)
        formatter.generate_worksheet_styles(workbook, worksheet, names)
        index = 0
        for width in widths:
            worksheet.set_column(index, index, width)
            index += 1

        export_cells(worksheet, converted_data_rows)
        workbook.close()
        return partner_folder, file_name + ".xlsx"

        # return partner_folder, file_name + ".xlsx"
        pass
    except Exception as e:
        pass


def make_archive(source, destination):
    try:
        zip_loc = source
        zip_dest = destination
        shutil.make_archive(base_dir=zip_loc, root_dir=zip_loc, format='zip', base_name=zip_dest)
    except Exception as e:
        pass


def export_order_positions(documents, titles):
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

            dtnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dt = str(dt).replace('-', '')
            partner_name = partner_name + "_" + str(dt)

            file_name = clean_filename(partner_name)
            file_name = file_name.replace('__', "_")
            file_path = os.path.join(exports_folder, file_name + ".xlsx")

            if (len(file_path) > 255):
                file_path = os.path.join(exports_folder, dir_id + ".xlsx")
            converted_data_rows = [
                [['Платежка для {} от {}'.format(document['name'], dtnow)]],
                [titles],
                document['positions'],
                [['','','','','','','','Итого','{}{}'.format(document['total'], document['currency'])]]
            ]
            workbook = xlsxwriter.Workbook(file_path)
            sheet_name = document['name']
            worksheet = workbook.add_worksheet(sheet_name)
            widths = formatter.get_column_widths(converted_data_rows)
            # formatter.generate_worksheet_styles(workbook, worksheet, names)
            index = 0
            for width in widths:
                worksheet.set_column(index, index, width)
                index += 1

            export_cells(worksheet, converted_data_rows)
            workbook.close()

        zip_name = exports_folder
        make_archive(exports_folder, zip_name)

        return EXPORTS_FOLDER, str(dir_id) + ".zip"
        pass
    except Exception as e:
        pass
