from res.clients_resources import *
from res.admin_settings_resources import *
from res.attachments_resources import *
from res.brands_catalog_resources import *
#[resource_class]
api_resources_crud =[
    AdminSettingsResource,
    AdminSettingsListResource,
    AttachmentsResource,
    AttachmentsListResource,
    BrandsResource,
    BrandsListResource

]

def init_single_resource(api, resource, route, endpoint):
    api.add_resource(resource, route, endpoint=endpoint)
    pass

def init_api_resources(api):
    for r in api_resources_crud:
        ex = r()
        init_single_resource(api, r, ex.route, ex.end_point)
        pass
