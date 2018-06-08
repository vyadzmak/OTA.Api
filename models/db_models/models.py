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
import datetime

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

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


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
    uid = Column('uid', String(64))
    optimized_size_file_path = Column('optimized_size_file_path', String(256))

    attachment_user_data = relationship('Users', backref="attachment_user_data")
    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.upload_date = datetime.datetime.now(datetime.timezone.utc)
        self.uid = str(uuid.uuid4())
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

    default_image_data_brands = relationship('Attachments', backref="default_image_data_brands")
    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# client addresses
class ClientAddresses(Base):
    __tablename__ = 'client_addresses'
    id = Column('id', Integer, primary_key=True)
    client_id = Column('client_id', ForeignKey('clients.id'))
    address = Column('address', String(500))
    is_default = Column('is_default', Boolean)

    related_clients = relationship('Clients', backref="client_addresses_data")

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# client info
class ClientInfo(Base):
    __tablename__ = 'client_info'
    id = Column('id', Integer, primary_key=True)
    client_id = Column('client_id', ForeignKey('clients.id'))
    logo_attachment_id = Column('logo_attachment_id', ForeignKey('attachments.id'))
    email = Column('email', String(32))
    main_info = Column('main_info', String(5500))
    additional_info = Column('additional_info', String(1500))
    phone_number = Column('phone_number', String(32))

    attachment_data = relationship('Attachments', backref="attachment_data")
    related_clients = relationship('Clients', backref="client_info_data")
    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# client types
class ClientTypes(Base):
    __tablename__ = 'client_types'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64))
    title = Column('title', String(64))

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# clients
class Clients(Base):
    __tablename__ = 'clients'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(70))
    registration_date = Column('registration_date', DateTime)
    registration_number = Column('registration_number', String(25))
    lock_state = Column('lock_state', Boolean)
    client_type_id = Column('client_type_id', ForeignKey('client_types.id'))

    client_type_data = relationship('ClientTypes', backref="client_type_data")
    related_users = relationship('Users', backref="client_data")
    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.registration_date = datetime.datetime.now(datetime.timezone.utc)
        self.lock_state = False

# currency catalog
class CurrencyCatalog(Base):
    __tablename__ = 'currency_catalog'
    id = Column('id', Integer, primary_key=True)
    system_name = Column('system_name', String(50))
    name = Column('name', String(100))
    display_value = Column('display_value', String(100))
    is_default = Column('is_default', Boolean)

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# log table
class Log(Base):
    __tablename__ = 'log'
    id = Column('id', Integer, primary_key=True)
    date = Column('date', DateTime)
    message = Column('message', String)

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.date = datetime.datetime.now(datetime.timezone.utc)


# order position states
class OrderPositionStates(Base):
    __tablename__ = 'order_position_states'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64))
    title = Column('title', String(64))

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


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

    product_data = relationship('Products', backref="product_data")
    order_data = relationship('Orders', backref="order_data")
    order_position_states = relationship('OrderPositionStates', backref="order_position_states")

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# order states
class OrderStates(Base):
    __tablename__ = 'order_states'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64))
    title = Column('title', String(64))

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


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
    order_state_id = Column('order_state_id', ForeignKey('order_states.id'))
    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.creation_date = datetime.datetime.now(datetime.timezone.utc)
        self.number = ''
        self.order_state_id = 1



# partners catalog
class PartnersCatalog(Base):
    __tablename__ = 'partners_catalog'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(100))
    images = Column('images', postgresql.ARRAY(Integer))
    description = Column('description', String(1000))
    short_description = Column('short_description', String(600))
    default_image_id = Column('default_image_id', ForeignKey('attachments.id'))

    default_image_data_partners = relationship('Attachments', backref="default_image_dat_partners")

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# product categories
class ProductCategories(Base):
    __tablename__ = 'product_categories'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64))
    short_description = Column('short_description', String(500))
    full_description = Column('full_description', String(1000))
    images = Column('images', postgresql.ARRAY(Integer))
    user_creator_id = Column('user_creator_id', ForeignKey('users.id'))
    creation_date = Column('creation_date', DateTime)
    is_lock = Column('is_lock', Boolean)
    parent_category_id = Column('parent_category_id', Integer)
    default_image_id = Column('default_image_id', ForeignKey('attachments.id'))

    default_image_data = relationship('Attachments', backref="default_image_data_product_categories")
    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.creation_date = datetime.datetime.now(datetime.timezone.utc)
        self.is_lock = False

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

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.creation_date = datetime.datetime.now(datetime.timezone.utc)


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
    brand_id = Column('brand_id', ForeignKey('brands_catalog.id'))
    partner_id = Column('partner_id', ForeignKey('partners_catalog.id'))
    amount = Column('amount', Float)
    currency_id = Column('currency_id', ForeignKey('currency_catalog.id'))
    unit_value = Column('unit_value', Float)
    unit_id = Column('unit_id', ForeignKey('unit_catalog.id'))
    is_stock_product = Column('is_stock_product', Boolean)
    stock_text = Column('stock_text', String(150))
    is_discount_product = Column('is_discount_product', Boolean)
    discount_amount = Column('discount_amount', Float)
    not_available = Column('not_available', Boolean)
    not_show_in_catalog = Column('not_show_in_catalog', Boolean)
    gallery_images = Column('gallery_images', postgresql.ARRAY(Integer))
    product_recomendations = Column('product_recomendations', postgresql.ARRAY(Integer))
    default_image_id = Column('default_image_id', ForeignKey('attachments.id'))


    default_image_data = relationship('Attachments', backref="default_image_data_product_products")

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.creation_date = datetime.datetime.now(datetime.timezone.utc)
        self.is_stock_product=False
        self.is_discount_product=False
        self.not_available=False
        self.not_show_in_catalog=False
        self.unit_value = 0
        self.discount_amount=0
        self.product_code =''
        self.product_recomendations=[

        ]
        self.stock_text =''

# settings
class Settings(Base):
    __tablename__ = 'settings'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250))
    value = Column('value', String(1500))

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# unit catalog
class UnitCatalog(Base):
    __tablename__ = 'unit_catalog'
    id = Column('id', Integer, primary_key=True)
    system_name = Column('system_name', String(50))
    name = Column('name', String(100))
    display_value = Column('display_value', String(100))
    is_default = Column('is_default', Boolean)

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


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

    user_cart_position_product_data = relationship('Products', backref="user_cart_position_product_data")
    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.temp_cart_uid =  str(uuid.uuid4())
        self.need_invoice=False

# user cart states
class UserCartStates(Base):
    __tablename__ = 'user_cart_states'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64))
    title = Column('title', String(64))

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# user carts
class UserCarts(Base):
    __tablename__ = 'user_carts'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    creation_date = Column('creation_date', DateTime)
    cart_state_id = Column('cart_state_id', ForeignKey('user_cart_states.id'))
    close_date = Column('close_date', DateTime)

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.creation_date = datetime.datetime.now(datetime.timezone.utc)
        self.cart_state_id = 1


# user info
class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    phone_number = Column('phone_number', String(32))
    email = Column('email', String(32))
    birthday = Column('birthday', Date)

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


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

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.registration_date = datetime.datetime.now(datetime.timezone.utc)


# user role routes
class UserRoleRoutes(Base):
    __tablename__ = 'user_role_routes'
    id = Column('id', Integer, primary_key=True)
    user_role_id = Column('user_role_id', ForeignKey('user_roles.id'))
    admin_route_access = Column('admin_route_access', Boolean)
    data_settings_route_access = Column('data_settings_route_access', Boolean)
    catalog_route_access = Column('catalog_route_access', Boolean)
    requests_route_access = Column('requests_route_access', Boolean)

    related_user_roles = relationship('UserRoles', backref="user_role_route_access")
    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# user roles
class UserRoles(Base):
    __tablename__ = 'user_roles'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64))
    title = Column('title', String(64))

    related_users = relationship('Users', backref="user_role_data")
    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# users
class Users(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(128))
    user_role_id = Column('user_role_id', ForeignKey('user_roles.id'))
    client_id = Column('client_id', ForeignKey('clients.id'))
    lock_state = Column('lock_state', Boolean)

    related_user_login = relationship('UserLogins', backref="user_data")
    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


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

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
