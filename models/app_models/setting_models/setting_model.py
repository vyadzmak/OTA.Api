import os, sys

# MODULE WITH "CONSTANTS" DO NOT CHANGE ANYTHING
ROOT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

print("ROOT =" + ROOT_DIR)

# application run mode
DEBUG_MODE = True

# data folder
DATA_FOLDER = ROOT_DIR + "/data/"

# exports folder
EXPORTS_FOLDER = ROOT_DIR + "/exports/"

# temp folder
TEMP_FOLDER = ROOT_DIR + "/temp/"

# upload folder
UPLOADS_FOLDER = '/uploads'

# upload folder original files
UPLOADS_FOLDER_ORIGINAL = UPLOADS_FOLDER + "/original/"

# upload folder thumbs files
UPLOADS_FOLDER_THUMBS = UPLOADS_FOLDER + "/thumbs/"

# upload folder optimized files
UPLOADS_FOLDER_OPTIMIZED = UPLOADS_FOLDER + "/optimized/"

# thumbs size
THUMB_SIZE = [256, 256]

# optimized size
OPTIMIZED_SIZE = [1024, 768]

# allowed extensions
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'bmp']

# API URL
API_URL = "http://127.0.0.1:5000/"
# API_URL ="http://10.0.2.2:5000/"

# use proxy
USE_PROXY = False

# proxy settings
PROXY_SETTINGS = {'http': None, 'https': None}

# DB URI
DB_URI = 'postgresql://postgres:12345678@localhost/ota'

# OWNER CLIENT ID
OWNER_CLIENT_ID = 3
