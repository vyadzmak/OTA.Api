from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer, ForeignKey, String, Column, JSON, select, func, and_
from sqlalchemy.orm import column_property, object_session, remote, foreign, aliased
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime
import random

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


# area catalog
class AreaCatalog(Base):
    __tablename__ = 'area_catalog'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(1000))

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# admin settings table
class Attachments(Base):
    __tablename__ = 'attachments'
    id = Column('id', Integer, primary_key=True)
    upload_date = Column('upload_date', DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    original_file_name = Column('original_file_name', String(256))
    file_size = Column('file_size', Integer)
    file_path = Column('file_path', String(256))
    user_creator_id = Column('user_creator_id', ForeignKey('users.id'))
    thumb_file_path = Column('thumb_file_path', String(256))
    uid = Column('uid', String(64), default=str(uuid.uuid4()))
    optimized_size_file_path = Column('optimized_size_file_path', String(256))

    attachment_user_data = relationship('Users', backref="attachment_user_data")

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.upload_date = datetime.datetime.now(datetime.timezone.utc)
        self.uid = str(uuid.uuid4())
        # self.thumb_file_path = None
        # self.optimized_size_file_path = None


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

        # area catalog


class CityCatalog(Base):
    __tablename__ = 'city_catalog'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(1000))
    area_id = Column('area_id', ForeignKey('area_catalog.id'))
    area_data = relationship("AreaCatalog", backref="area_data")

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# client addresses
class ClientAddresses(Base):
    __tablename__ = 'client_addresses'
    id = Column('id', Integer, primary_key=True)
    client_id = Column('client_id', ForeignKey('clients.id'))
    address = Column('address', String(500))
    is_default = Column('is_default', Boolean, default=False)
    confirmed = Column('confirmed', Boolean, default=False)
    tobacco_alcohol_license = Column('tobacco_alcohol_license', Boolean, default=False)
    name = Column('name', String(250))
    code = Column('code', String(250))
    phone_number = Column('phone_number', String(50))

    city_id = Column('city_id', ForeignKey('city_catalog.id'))

    city_data = relationship('CityCatalog', backref="city_data")
    related_clients = relationship('Clients', backref="client_addresses_data")

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.confirmed = False


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
    registration_date = Column('registration_date', DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    registration_number = Column('registration_number', String(25))
    lock_state = Column('lock_state', Boolean, default=False)
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
    is_default = Column('is_default', Boolean, default=False)

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# log table
class Log(Base):
    __tablename__ = 'log'
    id = Column('id', Integer, primary_key=True)
    date = Column('date', DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    message = Column('message', String)

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


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
    need_invoice = Column('need_invoice', Boolean, default=False)
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
    creation_date = Column('creation_date', DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    number = Column('number', String(32))
    executor_id = Column('executor_id', ForeignKey('users.id'))
    processed_date = Column('processed_date', DateTime)
    execute_date = Column('execute_date', DateTime)
    amount = Column('amount', Float)
    amount_discount = Column('amount_discount', Float)
    total_amount = Column('total_amount', Float)
    order_state_id = Column('order_state_id', ForeignKey('order_states.id'))
    client_address_id = Column('client_address_id', ForeignKey('client_addresses.id'))
    currency_id = Column('currency_id', ForeignKey('currency_catalog.id'))

    currency_data = relationship('CurrencyCatalog', backref="currency_data")
    client_address_data = relationship('ClientAddresses', backref="client_address_data")
    order_state_data = relationship('OrderStates', backref="order_state_data")

    # order_user_data = relationship('Users',backref = "order_user_data")

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.creation_date = datetime.datetime.now(datetime.timezone.utc)
        # self.start_counter =
        self.number = ''
        self.order_state_id = 1


# product comments
class ProductComments(Base):
    __tablename__ = 'product_comments'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    creation_date = Column('creation_date', DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    comment_text = Column('comment_text', String(600))
    rate = Column('rate', Float)
    is_delete = Column('is_delete', Boolean, default=False)
    product_id = Column('product_id', ForeignKey('products.id'))

    comment_user_data = relationship('Users', backref="comment_user_data")
    comment_product_data = relationship('Products', backref="comment_product_data")

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.creation_date = datetime.datetime.now(datetime.timezone.utc)


# products catalog
class Products(Base):
    __tablename__ = 'products'
    id = Column('id', Integer, primary_key=True)
    category_id = Column('category_id', Integer)
    user_creator_id = Column('user_creator_id', ForeignKey('users.id'))
    creation_date = Column('creation_date', DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    name = Column('name', String(250), default="")
    product_code = Column('product_code', String(32), default="")
    short_description = Column('short_description', String(250), default="")
    full_description = Column('full_description', String(1500), default="")
    brand_id = Column('brand_id', ForeignKey('brands_catalog.id'))
    partner_id = Column('partner_id', ForeignKey('partners_catalog.id'))
    amount = Column('amount', Float, default=0)
    currency_id = Column('currency_id', ForeignKey('currency_catalog.id'))
    unit_value = Column('unit_value', Float, default=0)
    unit_id = Column('unit_id', ForeignKey('unit_catalog.id'))
    is_stock_product = Column('is_stock_product', Boolean, default=False)
    stock_text = Column('stock_text', String(150), default="")
    is_discount_product = Column('is_discount_product', Boolean, default=False)
    discount_amount = Column('discount_amount', Float, default=0)
    not_available = Column('not_available', Boolean, default=False)
    not_show_in_catalog = Column('not_show_in_catalog', Boolean, default=False)
    gallery_images = Column('gallery_images', postgresql.ARRAY(Integer), default=[])
    product_recomendations = Column('product_recomendations', postgresql.ARRAY(Integer), default=[])
    default_image_id = Column('default_image_id', ForeignKey('attachments.id'))
    bonus_percent = Column('bonus_percent', Float, default=0)
    recommended_amount = Column('recommended_amount', Float, default=0)
    alt_amount = Column('alt_amount', Float, default=0)
    alt_unit_value = Column('alt_unit_value', Float, default=0)
    alt_unit_id = Column('alt_unit_id', ForeignKey('unit_catalog.id'))
    alt_discount_amount = Column('alt_discount_amount', Float, default=0)
    is_delete = Column('is_delete', Boolean, default=False)

    default_image_data = relationship('Attachments', backref="default_image_data_product_products")
    product_unit_data = relationship("UnitCatalog", backref="product_unit_data", foreign_keys=[unit_id])
    product_alt_unit_data = relationship("UnitCatalog", backref="product_alt_unit_data", foreign_keys=[alt_unit_id])
    product_currency_data = relationship("CurrencyCatalog", backref="product_currency_data")
    partner_data = relationship("PartnersCatalog", backref="product_partner_data")

    rate = column_property(
        select([func.avg(ProductComments.rate)]). \
            where(and_(ProductComments.product_id == id, ProductComments.is_delete == False)). \
            correlate_except(ProductComments)
    )

    comments_count = column_property(
        select([func.count(ProductComments.id)]). \
            where(and_(ProductComments.product_id == id, ProductComments.is_delete == False)). \
            correlate_except(ProductComments)
    )

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.creation_date = datetime.datetime.now(datetime.timezone.utc)
        self.is_stock_product = False
        self.is_discount_product = False
        self.not_available = False
        self.not_show_in_catalog = False
        self.unit_value = 0
        self.discount_amount = 0
        self.alt_unit_value = 0
        self.alt_discount_amount = 0
        self.alt_amount = 0
        self.product_code = ''
        self.product_recomendations = []
        self.stock_text = ''
        self.bonus_percent = 0
        self.recommended_amount = 0


# product categories
class ProductCategories(Base):
    __tablename__ = 'product_categories'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(64))
    short_description = Column('short_description', String(500))
    full_description = Column('full_description', String(1000))
    images = Column('images', postgresql.ARRAY(Integer))
    user_creator_id = Column('user_creator_id', ForeignKey('users.id'))
    creation_date = Column('creation_date', DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    is_lock = Column('is_lock', Boolean, default=False)
    parent_category_id = Column('parent_category_id', Integer)
    default_image_id = Column('default_image_id', ForeignKey('attachments.id'))
    is_delete = Column('is_delete', Boolean, default=False)

    default_image_data = relationship('Attachments', backref="default_image_data_product_categories")
    child_categories = relationship("ProductCategories",
                               primaryjoin = and_(remote(parent_category_id) == foreign(id),
                                                  foreign(is_delete) == False),
                               uselist=True)

    internal_products_count = column_property(
        select([func.count(Products.id)]). \
            where(and_(Products.category_id == id, Products.is_delete == False)). \
            correlate_except(Products)
    )

    @property
    def internal_categories_count(self):
        return object_session(self). \
            scalar(
            select([func.count(ProductCategories.id)]). \
                where(and_(ProductCategories.parent_category_id == self.id, ProductCategories.is_delete == False))
        )

    @property
    def child_products_count(self):
        child_ids = [x.id for x in self.child_categories]
        return object_session(self). \
            scalar(
            select([func.count(Products.id)]) \
            .where(and_(Products.category_id.in_(child_ids), Products.is_delete == False))
        )

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.creation_date = datetime.datetime.now(datetime.timezone.utc)
        self.is_lock = False


# partners catalog
class PartnersCatalog(Base):
    __tablename__ = 'partners_catalog'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(100))
    images = Column('images', postgresql.ARRAY(Integer))
    description = Column('description', String(1000))
    short_description = Column('short_description', String(600))
    default_image_id = Column('default_image_id', ForeignKey('attachments.id'))
    minimum_order_amount = Column('minimum_order_amount', Float, default=0)

    default_image_data_partners = relationship('Attachments', backref="default_image_data_partners")

    products_count = column_property(
        select([func.count(Products.id)]). \
            where(and_(Products.partner_id == id, Products.is_delete == False)). \
            correlate_except(Products)
    )

    @property
    def images_data(self):
        return object_session(self).query(Attachments) \
            .filter(Attachments.id.in_(self.images) if self.images is not None else False).all()


    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.minimum_order_amount = 0


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
    is_default = Column('is_default', Boolean, default=False)

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)

        # user carts


class UserBonuses(Base):
    __tablename__ = 'user_bonuses'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    order_id = Column('order_id', ForeignKey('orders.id'))
    creation_date = Column('creation_date', DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    state = Column('state', Boolean, default=True)
    amount = Column('amount', Float)

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.creation_date = datetime.datetime.now(datetime.timezone.utc)
        self.state = True


# user cart positions
class UserCartPositions(Base):
    __tablename__ = 'user_cart_positions'
    id = Column('id', Integer, primary_key=True)
    product_id = Column('product_id', ForeignKey('products.id'))
    user_cart_id = Column('user_cart_id', ForeignKey('user_carts.id'))
    count = Column('count', Float, default=0)
    description = Column('description', String(300))
    need_invoice = Column('need_invoice', Boolean, default=False)
    temp_cart_uid = Column('temp_cart_uid', String(300), default=str(uuid.uuid4()))
    alt_count = Column('alt_count', Float, default=0)
    user_cart_position_product_data = relationship('Products', backref="user_cart_position_product_data")

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.temp_cart_uid = str(uuid.uuid4())
        self.need_invoice = False


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
    creation_date = Column('creation_date', DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    cart_state_id = Column('cart_state_id', ForeignKey('user_cart_states.id'))
    close_date = Column('close_date', DateTime)

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.creation_date = datetime.datetime.now(datetime.timezone.utc)
        self.cart_state_id = 1

        # user info


class UserConfirmationCodes(Base):
    __tablename__ = 'user_confirmation_codes'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    code = Column('code', String(8))
    creation_date = Column('creation_date', DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.creation_date = datetime.datetime.now(datetime.timezone.utc)
        code = random.randint(1000, 9999)
        self.code = str(code)


# user favorite products
class UserFavoriteProducts(Base):
    __tablename__ = 'user_favorite_products'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    products_ids = Column('products_ids', postgresql.ARRAY(Integer))

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# user info
class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', ForeignKey('users.id'))
    phone_number = Column('phone_number', String(32))
    email = Column('email', String(32))
    birthday = Column('birthday', Date)
    avatar_id = Column('avatar_id', ForeignKey('attachments.id'))

    avatar_data = relationship('Attachments', backref="avatar_data")

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
    registration_date = Column('registration_date', DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    last_login_date = Column('last_login_date', DateTime)

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.registration_date = datetime.datetime.now(datetime.timezone.utc)


# user role routes
class UserRoleRoutes(Base):
    __tablename__ = 'user_role_routes'
    id = Column('id', Integer, primary_key=True)
    user_role_id = Column('user_role_id', ForeignKey('user_roles.id'))
    admin_route_access = Column('admin_route_access', Boolean, default=False)
    data_settings_route_access = Column('data_settings_route_access', Boolean, default=False)
    catalog_route_access = Column('catalog_route_access', Boolean, default=False)
    requests_route_access = Column('requests_route_access', Boolean, default=False)
    messages_route_access = Column('messages_route_access', Boolean, default=False)
    events_route_access = Column('events_route_access', Boolean, default=False)
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
    lock_state = Column('lock_state', Boolean, default=False)

    related_user_login = relationship('UserLogins', backref="user_data")

    # client_data = relationship('Clients', backref="client_data")

    # order_user_data = relationship('Orders', backref = "order_user_data")
    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# user role routes
class ViewSettings(Base):
    __tablename__ = 'view_settings'
    id = Column('id', Integer, primary_key=True)

    show_slider = Column('show_slider', Boolean, default=False)
    show_badges = Column('show_badges', Boolean, default=False)
    show_recommendations = Column('show_recommendations', Boolean, default=False)
    show_badge_popular = Column('show_badge_popular', Boolean, default=False)
    show_badge_discount = Column('show_badge_discount', Boolean, default=False)
    show_badge_stock = Column('show_badge_stock', Boolean, default=False)
    show_badge_partners = Column('show_badge_partners', Boolean, default=False)
    default_slider_image = Column('default_slider_image', Integer)
    slider_images = Column('slider_images', postgresql.ARRAY(Integer))
    recomendation_elements = Column('recomendation_elements', postgresql.ARRAY(Integer))
    brand_elements = Column('brand_elements', postgresql.ARRAY(Integer))
    partner_elements = Column('partner_elements', postgresql.ARRAY(Integer))
    show_brands = Column('show_brands', Boolean, default=False)

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# product category positions
class ProductCategoryPositions(Base):
    __tablename__ = 'product_category_positions'
    id = Column('id', Integer, primary_key=True)
    parent_category_id = Column('parent_category_id', ForeignKey('product_categories.id'))
    child_category_positions = Column('child_category_positions', postgresql.ARRAY(Integer))

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# products positions
class ProductsPositions(Base):
    __tablename__ = 'products_positions'
    id = Column('id', Integer, primary_key=True)
    category_id = Column('category_id', ForeignKey('product_categories.id'))
    products_positions = Column('products_positions', postgresql.ARRAY(Integer))

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# message contents
class MessageContents(Base):
    __tablename__ = 'message_contents'
    id = Column('id', Integer, primary_key=True)
    user_sender_id = Column('user_sender_id', ForeignKey('users.id'))
    creation_date = Column('creation_date', DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    title = Column('title', String(500))
    message = Column('message', String(5000))
    is_popup = Column('is_popup', Boolean, default=False)

    receivers = relationship('Messages', backref="message_content")
    user_data = relationship('Users', backref="message_contents_user_data")

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
        self.creation_date = datetime.datetime.now(datetime.timezone.utc)


# messages
class Messages(Base):
    __tablename__ = 'messages'
    id = Column('id', Integer, primary_key=True)
    receiver_user_id = Column('receiver_user_id', ForeignKey('users.id'))
    is_read = Column('is_read', Boolean, default=False)
    message_content_id = Column('message_content_id', ForeignKey('message_contents.id'))

    user_data = relationship('Users', backref="messages_user_data")

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)


# events
class Events(Base):
    __tablename__ = 'events'
    id = Column('id', Integer, primary_key=True)
    user_creator_id = Column('user_creator_id', ForeignKey('users.id'))
    product_id = Column('product_id', ForeignKey('products.id'))
    end_date = Column('end_date', DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    count_days_notifications = Column('count_days_notifications', Integer)
    state = Column('state', Boolean, default=False)
    message = Column('message', String(5000))

    user_data = relationship('Users', backref="events_user_data")
    product_data = relationship('Products', backref="events_product_data")

    def __init__(self, *args):
        db_tranformer.transform_constructor_params(self, args)
