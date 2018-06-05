from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import DateTime

from sqlalchemy import Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, ForeignKey, String, Column, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
import uuid
# import models.app_models.schema_models.schema_model as schema_model
# import models.app_models.object_models.object_model as object_model
# import modules.json_modules.json_encoder as encoder
import datetime
from geoalchemy2 import Geometry

Base = declarative_base()

import modules.db_model_tranformer_modules.db_model_transformer_module as db_tranformer

# admin settings table
class AdminSettings(Base):
    __tablename__ = 'admin_settings'
    id = Column('id', Integer, primary_key=True)
    data_refresh_interval = Column('data_refresh_interval', Integer)
    count_data_take_device = Column('count_data_take_device', Integer)
    count_log_data_records_auto_clean = Column('count_log_data_records_auto_clean', Integer)
    user_agreement = Column('user_agreement', String)

    def __init__(self,*args):
        db_tranformer.transform_constructor_params(self,args)
        # for a in args:
        #     p = a
        #     for key in p:
        #         s_key = key
        #         s_value = p[key]
        #         if hasattr(self, s_key):
        #             #a.property
        #             setattr(self, s_key, s_value)
        # pass
    # def __init__(self, data_refresh_interval, count_data_take_device, count_log_data_records_auto_clean,
    #              user_agreement):
    #     for key, value in kwargs.items():
    #         print("The value of {} is {}".format(key, value))
    #     self.data_refresh_interval = data_refresh_interval
    #     self.count_data_take_device = count_data_take_device
    #     self.count_log_data_records_auto_clean = count_log_data_records_auto_clean
    #     self.user_agreement = user_agreement


# admin settings table
class Attachments(Base):
    __tablename__ = 'attachments'
    id = Column('id', Integer, primary_key=True)
    upload_date = Column('upload_date', DateTime)
    original_file_name = Column('original_file_name', String(256))
    file_size = Column('file_size', Integer)
    file_path = Column('file_path', String(256))
    user_creator_id = Column('user_creator_id', ForeignKey('users.id'))
    thumb_file_path = Column('thumb_file_path', String(256))
    optimized_size_file_path = Column('optimized_size_file_path', String(256))

    def __init__(self, original_file_name, file_size, file_path, user_creator_id):
        self.upload_date = datetime.datetime.now()
        self.uid = str(uuid.uuid4())
        self.original_file_name = original_file_name
        self.file_size = file_size
        self.file_path = file_path
        self.user_creator_id = user_creator_id
        self.thumb_file_path = None
        self.optimized_size_file_path = None


# brands catalog
class BrandsCatalog(Base):
    __tablename__ = 'brands_catalog'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(100))
    images = Column('images', postgresql.ARRAY(Integer))
    description = Column('description', String(1000))
    short_description = Column('short_description', String(600))
    default_image_id = Column('default_image_id', ForeignKey('attachments.id'))

    def __init__(self, name):
        self.name = name


# client addresses
class ClientAddresses(Base):
    __tablename__ = 'client_addresses'
    id = Column('id', Integer, primary_key=True)
    client_id = Column('client_id', ForeignKey('clients.id'))
    address = Column('address', String(500))
    is_default = Column('is_default', Boolean)

    def __init__(self, client_id, address):
        self.client_id = client_id
        self.address = address


# client info
class ClientInfo(Base):
    __tablename__ = 'cilent_info'
    id = Column('id', Integer, primary_key=True)
    client_id = Column('client_id', ForeignKey('clients.id'))
    logo_attachment_id = Column('logo_attachment_id', ForeignKey('attachments.id'))
    email = Column('email', String(32))
    main_info = Column('main_info', String(5500))
    additional_info = Column('additional_info', String(1500))
    phone_number = Column('phone_number', String(32))

    def __init__(self, client_id):
        self.client_id = client_id


# client types
class ClientTypes(Base):
    __tablename__ = 'client_types'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64))
    title = Column('title', String(64))

    def __init__(self, name, title):
        self.name = name
        self.title = title


# clients
class Clients(Base):
    __tablename__ = 'clients'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(70))
    registration_date = Column('registration_date', DateTime)
    registration_number = Column('registration_number', String(25))
    lock_state = Column('lock_state', Boolean)
    client_type_id = Column('client_type_id', ForeignKey('client_types.id'))

    def __init__(self, name, client_type_id):
        self.name = name
        self.client_type_id = client_type_id



# currency catalog
class CurrencyCatalog(Base):
    __tablename__ = 'currency_catalog'
    id = Column('id', Integer, primary_key=True)
    system_name = Column('system_name', String(50))
    name = Column('name', String(100))
    display_value = Column('display_value', String(100))
    is_default = Column('is_default', Boolean)

    def __init__(self, system_name, name, display_value, is_default=False):
        self.name = name
        self.system_name = system_name
        self.display_value = display_value
        self.is_default = is_default


# log table
class Log(Base):
    __tablename__ = 'log'
    id = Column('id', Integer, primary_key=True)
    date = Column('date', DateTime)
    message = Column('message', String)

    def __init__(self, message):
        self.date = datetime.datetime.now()
        self.message = message


# order position states
class OrderPositionStates(Base):
    __tablename__ = 'order_position_states'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64))
    title = Column('title', String(64))

    def __init__(self, name, title):
        self.name = name
        self.title = title


# order positions
class OrderPositions(Base):
    __tablename__ = 'order_positions'
    id = Column('id', Integer, primary_key=True)
    product_id = Column('product_id', ForeignKey('products.id'))
    order_id = Column('order_id', ForeignKey('orders.id'))
    count = Column('count', Float)
    description = Column('description', String(300))
    need_invoice = Column('need_invoice', Boolean)
    order_position_state_id = Column('order_position_state_id', ForeignKey('order_position_states.id'))
    amount_per_item = Column('amount_per_item', Float)
    amount_per_item_discount = Column('amount_per_item_discount', Float)
    total_amount = Column('total_amount', Float)

    def __init__(self, product_id, order_id, count, description, need_invoice, order_position_state_id, amount_per_item,
                 total_amount, amount_per_item_discount):
        self.product_id = product_id
        self.order_id = order_id
        self.count = count
        self.description = description
        self.need_invoice = need_invoice
        self.order_position_state_id = order_position_state_id
        self.amount_per_item = amount_per_item
        self.total_amount = total_amount
        self.amount_per_item_discount = amount_per_item_discount


# order states
class OrderStates(Base):
    __tablename__ = 'order_states'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64))
    title = Column('title', String(64))

    def __init__(self, name, title):
        self.name = name
        self.title = title


# orders
class Orders(Base):
    __tablename__ = 'orders'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    creation_date = Column('creation_date', DateTime)
    number = Column('number', String(32))
    executor_id = Column('executor_id', ForeignKey('users.id'))
    processed_date = Column('processed_date', DateTime)
    execute_date = Column('execute_date', DateTime)
    amount = Column('amount', Float)
    amount_discount = Column('amount_discount', Float)
    total_amount = Column('total_amount', Float)

    def __init__(self, user_id, number, amount, amount_discount, total_amount):
        self.user_id = user_id
        self.creation_date = datetime.datetime.now()
        self.number = number
        self.amount = amount
        self.amount_discount = amount_discount
        self.total_amount = total_amount


# partners catalog
class PartnersCatalog(Base):
    __tablename__ = 'partners_catalog'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(100))
    images = Column('images', postgresql.ARRAY(Integer))
    description = Column('description', String(1000))
    short_description = Column('short_description', String(600))
    default_image_id = Column('default_image_id', ForeignKey('attachments.id'))

    def __init__(self, name):
        self.name = name


# products catalog
class ProductsCatalog(Base):
    __tablename__ = 'products_catalog'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64))
    short_description = Column('short_description', String(500))
    full_description = Column('full_description', String(1000))
    images = Column('images', postgresql.ARRAY(Integer))
    user_creator_id = Column('user_creator_id', ForeignKey('users.id'))
    creation_date = Column('creation_date', DateTime)
    is_lock_state = Column('is_lock', Boolean)
    parent_category_id = Column('parent_category_id', Integer)

    default_image_id = Column('default_image_id', ForeignKey('attachments.id'))

    def __init__(self, name, user_creator_id, parent_category_id=-1):
        self.name = name
        self.user_creator_id = user_creator_id
        self.parent_category_id = parent_category_id
        self.creation_date = datetime.datetime.now()


# product comments
class ProductComments(Base):
    __tablename__ = 'product_comments'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    creation_date = Column('creation_date', DateTime)
    comment_text = Column('comment_text', String(600))
    rate = Column('rate', Float)
    is_delete = Column('is_delete', Boolean)
    product_id = Column('product_id', ForeignKey('products.id'))

    def __init__(self, user_id, comment_text, rate, product_id):
        self.user_id = user_id
        self.comment_text = comment_text
        self.rate = rate
        self.product_id = product_id
        self.creation_date = datetime.datetime.now()


# products catalog
class Products(Base):
    __tablename__ = 'products'
    id = Column('id', Integer, primary_key=True)
    category_id = Column('category_id', Integer)
    user_creator_id = Column('user_creator_id', ForeignKey('users.id'))
    creation_date = Column('creation_date', DateTime)
    name = Column('name', String(250))
    product_code = Column('product_code', String(32))
    short_description = Column('short_description', String(250))
    full_description = Column('full_description', String(1500))
    brand_id = Column('brand_id', ForeignKey('brands.id'))
    partner_id = Column('partner_id', ForeignKey('partners.id'))
    amount = Column('amount', Float)
    currency_id = Column('currency_id', ForeignKey('currency_catalog.id'))
    unit_value = Column('unit_value', Float)
    unit_id = Column('unit_id', ForeignKey('unit_catalog.id'))
    is_stock_product = Column('is_stock_product', Boolean)
    stock_text = Column('stock_text', String(150))
    is_discount_product = Column('is_discount_product', Boolean)
    discount_amount = Column('discount', Float)
    not_available = Column('not_available', Boolean)
    not_show_in_catalog = Column('not_show_in_catalog', Boolean)
    gallery_images = Column('gallery_images', postgresql.ARRAY(Integer))
    product_recomendations = Column('product_recomendations', postgresql.ARRAY(Integer))
    default_image_id = Column('default_image_id', ForeignKey('attachments.id'))

    def __init__(self, category_id, user_creator_id, name, amount, currency_id):
        self.category_id = category_id
        self.user_creator_id = user_creator_id
        self.name = name
        self.amount = amount
        self.currency_id = currency_id
        self.creation_date = datetime.datetime.now()


# settings
class Settings(Base):
    __tablename__ = 'settings'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250))
    value = Column('value', String(1500))

    def __init__(self, name, value):
        self.name = name
        self.value = value


# unit catalog
class UnitCatalog(Base):
    __tablename__ = 'unit_catalog'
    id = Column('id', Integer, primary_key=True)
    system_name = Column('system_name', String(50))
    name = Column('name', String(100))
    display_value = Column('display_value', String(100))
    is_default = Column('is_default', Boolean)

    def __init__(self, system_name, name, display_value, is_default=False):
        self.name = name
        self.system_name = system_name
        self.display_value = display_value
        self.is_default = is_default


# user cart positions
class UserCartPositions(Base):
    __tablename__ = 'user_cart_positions'
    id = Column('id', Integer, primary_key=True)
    product_id = Column('product_id', ForeignKey('products.id'))
    user_cart_id = Column('user_cart_id', ForeignKey('user_carts.id'))
    count = Column('count', Float)
    description = Column('description', String(300))
    need_invoice = Column('need_invoice', Boolean)
    temp_cart_uid = Column('temp_cart_uid', String(300))

    def __init__(self, product_id, count, temp_cart_uid):
        self.product_id = product_id
        self.count = count
        self.temp_cart_uid = temp_cart_uid


# user cart states
class UserCartStates(Base):
    __tablename__ = 'user_cart_states'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64))
    title = Column('title', String(64))

    def __init__(self, name, title):
        self.name = name
        self.title = title


# user carts
class UserCarts(Base):
    __tablename__ = 'user_carts'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    creation_date = Column('creation_date', DateTime)
    cart_state_id = Column('cart_state_id', ForeignKey('user_cart_states.id'))
    close_date = Column('close_date', DateTime)

    def __init__(self, user_id):
        self.user_id = user_id
        self.creation_date = datetime.datetime.now()
        self.cart_state_id = 1


# user info
class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    phone_number = Column('phone_number', String(32))
    email = Column('email', String(32))
    birthday = Column('birthday', Date)

    def __init__(self, user_id):
        self.user_id = user_id


# user logins
class UserLogins(Base):
    __tablename__ = 'user_logins'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    login = Column('login', String(32))
    password = Column('password', String(250))
    token = Column('token', String)
    registration_date = Column('registration_date', DateTime)
    last_login_date = Column('last_login_date', DateTime)

    def __init__(self, user_id, login, password):
        self.user_id = user_id
        self.login = login
        self.password = password
        self.registration_date = datetime.datetime.now()


# user role routes
class UserRoleRoutes(Base):
    __tablename__ = 'user_role_routes'
    id = Column('id', Integer, primary_key=True)
    user_role_id = Column('user_role_id', ForeignKey('user_roles.id'))
    admin_route_access = Column('admin_route_access', Boolean)
    data_settings_route_access = Column('data_settings_route_access', Boolean)
    catalog_route_access = Column('catalog_route_access', Boolean)
    requests_route_access = Column('requests_route_access', Boolean)

    def __init__(self, user_role_id, admin_route_access, data_settings_route_access, catalog_route_access,
                 requests_route_access):
        self.user_role_id = user_role_id
        self.admin_route_access = admin_route_access
        self.data_settings_route_access = data_settings_route_access
        self.catalog_route_access = catalog_route_access
        self.requests_route_access = requests_route_access


# user roles
class UserRoles(Base):
    __tablename__ = 'user_roles'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64))
    title = Column('title', String(64))

    def __init__(self, name, title):
        self.name = name
        self.title = title


# users
class Users(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(128))
    user_role_id = Column('user_role_id', ForeignKey('user_roles.id'))
    client_id = Column('client_id', ForeignKey('clients.id'))
    lock_state = Column('lock_state', Boolean)

    def __init__(self, name, client_id, user_role_id):
        self.name = name
        self.client_id = client_id
        self.user_role_id = user_role_id

# user role routes
class ViewSettings(Base):
    __tablename__ = 'view_settings'
    id = Column('id', Integer, primary_key=True)

    show_slider = Column('show_slider', Boolean)
    show_badges = Column('show_badges', Boolean)
    show_recommendations = Column('show_recommendations', Boolean)
    show_badge_popular = Column('show_badge_popular', Boolean)
    show_badge_discount = Column('show_badge_discount', Boolean)
    show_badge_stock = Column('show_badge_stock', Boolean)
    show_badge_partners = Column('show_badge_partners', Boolean)

    slider_images = Column('slider_images', postgresql.ARRAY(Integer))
    recomendation_elements = Column('recomendation_elements', postgresql.ARRAY(Integer))
    brand_elements = Column('brand_elements', postgresql.ARRAY(Integer))


    def __init__(self, show_slider,show_badges, show_recommendations):
        self.show_slider = show_slider
        self.show_badges = show_badges
        self.show_recommendations = show_recommendations

