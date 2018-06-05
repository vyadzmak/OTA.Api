from res.clients_resources import *
from res.admin_settings_resources import *

#[resource_class]
api_resources_crud =[
    AdminSettingsResource,
    AdminSettingsListResource

]

def init_single_resource(api, resource, route, endpoint):
    api.add_resource(resource, route, endpoint=endpoint)
    pass

def init_api_resources(api):
    for r in api_resources_crud:
        ex = r()
        init_single_resource(api, r, ex.route, ex.end_point)
        pass
