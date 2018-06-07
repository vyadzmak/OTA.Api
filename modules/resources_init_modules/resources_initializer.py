from res.clients_resources import *
from res.admin_settings_resources import *
from res.attachments_resources import *
from res.brands_catalog_resources import *
from res.client_adresses_resources import *
from res.client_info_resources import *
from res.client_types_resources import *
from res.clients_resources import *
from res.currency_catalog_resources import *
from res.log_resources import *
from res.order_position_states_resources import *
from res.order_positions_resources import *
from res.order_states_resources import *
from res.partners_catalog_resources import *



#[resource_class]
api_resources_crud =[
    AdminSettingsResource,
    AdminSettingsListResource,
    AttachmentsResource,
    AttachmentsListResource,
    BrandsResource,
    BrandsListResource,
    ClientAddressesResource,
    ClientAddressesListResource,
    ClientInfoResource,
    ClientInfoListResource,
    ClientTypesResource,
    ClientTypesListResource,
    ClientsResource,
    ClientsListResource,
    CurrencyCatalogResource,
    CurrencyCatalogListResource,
    LogResource,
    LogListResource,
    OrderPositionStatesResource,
    OrderPositionStatesListResource,
    OrderPositionsResource,
    OrderPositionsListResource,
    OrderStatesResource,
    OrderStatesListResource,

    PartnersResource,
    PartnersListResource

]

def init_single_resource(api, resource, route, endpoint):
    api.add_resource(resource, route, endpoint=endpoint)
    pass

def init_api_resources(api):
    for r in api_resources_crud:
        ex = r()
        init_single_resource(api, r, ex.route, ex.end_point)
        pass
