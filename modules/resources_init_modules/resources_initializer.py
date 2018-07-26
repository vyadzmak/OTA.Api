from res.clients_resources import *
from res.admin_settings_resources import *
from res.area_catalog_resources import *
from res.attachments_resources import *
from res.brands_catalog_resources import *
from res.client_adresses_resources import *
from res.city_catalog_resources import *
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
from res.user_confirmation_codes_resources import *
from res.user_info_resources import *
from res.user_logins_resources import *
from res.user_route_roles_resources import *
from res.user_roles_resources import *
from res.users_resources import *
from res.view_settings_resources import *
from res.upload_files_resources import *
from res.attachment_original_view_resources import *
from res.attachment_thumbs_view_resources import *
from res.attachment_optimized_view_resources import *
from res.product_comments_resources import *
from res.user_favorite_products_resources import *
from res.user_bonuses_resources import *
#cross resourcse
from cross_res.user_auth_resources import *
from cross_res.route_admin_general_resources import *
from cross_res.route_admin_users_resources import *
from cross_res.route_admin_clients_resources import *
from cross_res.route_admin_log_resources import *
from cross_res.route_admin_settings_resources import *
from cross_res.attacments_info_resources import *
from cross_res.client_info_by_client_resources import *
from cross_res.client_addresses_by_client_resources import *
from cross_res.products_categories_by_product_category_resources import *
from cross_res.products_by_product_category_resources import *
from cross_res.route_catalog_products_general_resources import *
from cross_res.route_catalog_products_gallery_resources import *
from cross_res.route_catalog_products_recommendations_resources import *
from cross_res.route_catalog_products_comments_resources import *
from cross_res.route_orders_resources import *
from cross_res.route_view_settings_general_resources import *
from cross_res.route_view_settings_slider_resources import *
from cross_res.route_view_settings_badges_resources import *
from cross_res.city_catalog_by_area_resources import *
from cross_res.users_by_client_resources import *
from cross_res.order_positions_by_order_resources import *
from cross_res.manage_users_resources import *
from cross_res.users_details_resources import *
from cross_res.quick_user_registration_resources import *
from cross_res.route_view_settings_resources import *
from cross_res.product_details_resources import *
from cross_res.user_favorite_products_by_user_resources import *
from cross_res.filter_products_resources import *
from cross_res.orders_history_resources import *
from cross_res.mobile_user_auth_resources import *
from cross_res.user_confirmation_code_check_resource import *
from cross_res.user_cart_details_resources import *
from cross_res.add_cart_position_to_cart_resources import *
from cross_res.manage_user_cart_details_resources import *
from  cross_res.make_user_order_resources import *
from cross_res.manage_favorite_products import *
from cross_res.user_profile_resources import *
from cross_res.user_cart_product_count_resources import *
from cross_res.update_user_profile_resources import *
from cross_res.update_client_profile_resources import *
from cross_res.category_list_without_products_resources import *
from cross_res.category_list_without_child_categories_resources import *
from cross_res.user_bonuses_resources import *
from cross_res.close_user_bonuses_resources import *
from cross_res.products_recommendations_catalog_resources import *
from cross_res.repeat_order_resources import *
from cross_res.product_users_comments_resources import *
#[resource_class]
api_resources_crud =[
    AdminSettingsResource,
    AdminSettingsListResource,
    AreaCatalogResource,
    AreaCatalogListResource,
    AttachmentsResource,
    AttachmentsListResource,
    BrandsResource,
    BrandsListResource,

    CityCatalogResource,
    CityCatalogListResource,
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
    ProductCommentsResource,
    ProductCommentsListResource,

    ProductsResource,
    ProductsListResource,

    SettingsResource,
    SettingsListResource,

    UnitCatalogResource,
    UnitCatalogListResource,
    UploadFileResource,
    AttachmentOriginalViewResource,
    AttachmentThumbsViewResource,
    AttachmentOptimizedViewResource,

    UserBonusesResource,
    UserConfirmationCodesResource,
    UserConfirmationCodesListResource,

    UserCartStatesResource,
    UserCartStatesListResource,
    UserCartsResource,
    UserCartsListResource,
    UserCartPositionsResource,
    UserCartPositionsListResource,
    UserFavoriteProductsResource,
    UserFavoriteProductsListResource,
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
    UserAuthResource,
    RouteAdminGeneralResource,
    RouteAdminUsersResource,
    RouteAdminClientsResource,
    RouteAdminLogsResource,
    RouteAdminSettingsResource,
    AttachmentsInfoResource,
    ClientInfoByClientResource,
    ClientAddressesByClientResource,
    ProductsCategoriesByProductCategoryResource,
    ProductsByProductCategoryResource,
    RouteCatalogProductsGeneralResource,
    RouteCatalogProductsGalleryResource,
    RouteCatalogProductsRecommendationsResource,
    RouteCatalogProductsCommentsResource,
    RouteOrdersResource,
    RouteViewSettingsGeneralResource,
    RouteViewSettingsSliderResource,
    RouteViewSettingsBadgesResource,
    CityCatalogByAreaResource,
    UsersByClientResource,
    OrderPositionsByOrderResource,
    ManageUsersResource,
    ManageUsersListResource,
    UsersDetailsResource,
    QuickUserRegistrationResource,
    RouteViewSettingsResource,
    ProductDetailsResource,
    UserFavoriteProductsByUserResource,
    FilterProductResource,
    OrdersHistoryResource,
    MobileUserAuthResource,
    UserConfirmationCodeCheckResource,
    UserCartDetailsResource,
    AddCartPositionToCartResource,
    ManageUserCartDetailsResource,
    MakeUserOrderResource,
    ManageFavoriteProductsResource,
    UserProfileResource,
    UserCartProductCountResource,
    UpdateUserProfileResource,
    UpdateClientProfileResource,
    CategoryListWithoutProductsResource,
    CategoryListWithoutChildCategoriesResource,
    UserBonusesDetailsResource,
    CloseUserBonusesResource,
    ProductsRecommendationsCatalogResource,
    RepeatOrderResource,
    ProductUsersCommentsResource
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
