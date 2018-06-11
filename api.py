from flask import Flask
from flask_restful import Resource, Api
from models.app_models.json_encoder_models.json_encoder import AlchemyEncoder
from flask_cors import CORS
import modules.resources_init_modules.resources_initializer as resources_initializer
from flask_basicauth import BasicAuth
#init application
app = Flask(__name__)
# app.config['BASIC_AUTH_USERNAME'] = 'ota_user'
# app.config['BASIC_AUTH_PASSWORD'] = 'vPe0N9zb7bGK1Ng5'
# app.config['BASIC_AUTH_FORCE'] = True
# basic_auth = BasicAuth(app)

#cors = CORS(app, resources={r"/login/*": {"origins": "*"}})

CORS(app, expose_headers = ["Access-Token","Uid","Content-Disposition"])



app.config['BUNDLE_ERRORS'] = True
json_encoder = AlchemyEncoder
app.json_encoder =json_encoder
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.errorhandler(500)
def internal_error(error):
    return "500 error"

api = Api(app)

#generate routes
resources_initializer.init_api_resources(api)
#start application
if __name__ == '__main__':
    #u_s.get_user_roles()
    app.run(debug=True)