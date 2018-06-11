from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import os
import werkzeug
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from models.db_models.models import Attachments
import uuid
import re
import subprocess
from pathlib import Path
from models.app_models.setting_models.setting_model import ROOT_DIR,UPLOADS_FOLDER_ORIGINAL, UPLOADS_FOLDER_OPTIMIZED, \
    UPLOADS_FOLDER_THUMBS, ALLOWED_EXTENSIONS, THUMB_SIZE, OPTIMIZED_SIZE

import modules.img_resizer_modules.img_resizer_module as image_resizer

ENTITY_NAME = "Upload Files"
#MODEL = Log
ROUTE ="/uploadFiles"
END_POINT = "upload-files"


# UPLOAD_FOLDER = 'd:\\uploads'
# ALLOWED_EXTENSIONS = set(['xls','xlsx'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_file_name():
    pass


class UploadFileResource(Resource):
    def __init__(self):
        self.route = ROUTE
        self.end_point = END_POINT
        pass

    def post(self):
        try:
            f = request.form
            user_creator_id = f.get('user_id')

            f_list = []
            files = []
            for t in request.files:
                f_list = request.files.getlist(str(t))
                for j_file in f_list:
                    files.append(j_file)

            # dir_id = str(uuid.uuid4().hex)
            # project_folder = os.path.join(UPLOADS_FOLDER_ORIGINAL, dir_id)
            result_ids =[]
            for file in files:

                # if not os.path.exists(ROOT_DIR+project_folder):
                #     os.makedirs(ROOT_DIR+project_folder)
                if file and allowed_file(file.filename):
                    # From flask uploading tutorial
                    filename = file.filename  # str(secure_filename(file.filename)).lower()
                    v = Path(filename)
                    short_name = Path(filename).stem

                    short_name = re.sub(r'[\\/*?:"<>|]', "", short_name)
                    short_name = short_name.replace(" ","_")
                    extension = Path(filename).suffix
                    file_id = str(uuid.uuid4().hex)
                    result_file_name = file_id + extension
                    print("Save to " + result_file_name)
                    file_path = os.path.join(UPLOADS_FOLDER_ORIGINAL, result_file_name)
                    file_path = file_path.replace('\\','/')
                    save_path =ROOT_DIR+file_path
                    file.save(save_path)
                    file_size = os.path.getsize(save_path)


                    thumbs_file_path = UPLOADS_FOLDER_THUMBS
                    thumbs_name = file_id+".jpg"
                    thumbs_file_path_db = os.path.join(thumbs_file_path,thumbs_name)
                    thumbs_save_path =ROOT_DIR+os.path.join(thumbs_file_path,thumbs_name).replace('\\','/')
                    image_resizer.resize_image(save_path,thumbs_save_path,THUMB_SIZE)

                    optimized_file_path = UPLOADS_FOLDER_OPTIMIZED
                    optimized_name = file_id + ".jpg"
                    optimized_file_path_db = os.path.join(optimized_file_path,optimized_name)
                    optimized_save_path =  ROOT_DIR +os.path.join(optimized_file_path, optimized_name).replace('\\', '/')
                    image_resizer.resize_image(save_path, optimized_save_path, OPTIMIZED_SIZE)

                    attributes = {'original_file_name':filename,'file_size':file_size,'file_path':file_path,'user_creator_id':user_creator_id,'thumb_file_path':thumbs_file_path_db,'optimized_size_file_path':optimized_file_path_db}

                    attachment = Attachments(attributes)
                    session.add(attachment)
                    session.commit()
                    result_ids.append(attachment.id)

                    #ЗДЕСЬ НАДО ВХЕРАЧИТЬ СЖАТИЕ ЕСЛИ НАДО, А ОНО НАДО
                    # return {}
                else:
                    # return error
                    return {}

            return result_ids
        except Exception as e:
            return {"State": "Error"}
