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
from res.orders_resources import *

from res.partners_catalog_resources import *
from res.product_categories_resources import *
from res.products_resources import *
from res.settings_resources import *
from res.unit_catalog_resources import *
from res.user_cart_states_resources import *
from res.user_carts_resources import *
from res.user_cart_positions_resources import  *

from res.user_info_resources import *
from res.user_logins_resources import *
from res.user_route_roles_resources import *
from res.user_roles_resources import *
from res.users_resources import *
from res.view_settings_resources import *

#cross resourcse

from cross_res.user_auth_resources import *

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
    OrdersResource,
    OrdersListResource,
    PartnersResource,
    PartnersListResource,
    ProductCategoriesResource,
    ProductCategoriesListResource,
    ProductsResource,
    ProductsListResource,

    SettingsResource,
    SettingsListResource,

    UnitCatalogResource,
    UnitCatalogListResource,

    UserCartStatesResource,
    UserCartStatesListResource,
    UserCartsResource,
    UserCartsListResource,
    UserCartPositionsResource,
    UserCartPositionsListResource,
    UserInfoResource,
    UserInfoListResource,
    UserLoginsResource,
    UserLoginsListResource,
    UserRoleRoutesResource,
    UserRoleRoutesListResource,
    UserRolesResource,
    UserRolesListResource,
    UsersResource,
    UsersListResource,
    ViewSettingsResource,
    ViewSettingsListResource
]


#[resource_class]
api_resources_cross =[
    UserAuthResource
]
def init_single_resource(api, resource, route, endpoint):
    api.add_resource(resource, route, endpoint=endpoint)
    pass

def init_api_resources(api):
    for crud_resource in api_resources_crud:
        ex = crud_resource()
        init_single_resource(api, crud_resource, ex.route, ex.end_point)

        pass

    for cross_resource in api_resources_cross:
        ex = cross_resource()
        init_single_resource(api, cross_resource, ex.route, ex.end_point)
        pass
