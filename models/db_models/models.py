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


# admin settings table
class AdminSettings(Base):
    __tablename__ = 'admin_settings'
    id = Column('id', Integer, primary_key=True)
    data_refresh_interval = Column('data_refresh_interval', Integer)
    count_data_take_device = Column('count_data_take_device', Integer)
    count_log_data_records_auto_clean = Column('count_log_data_records_auto_clean', Integer)
    user_agreement = Column('user_agreement', String)

    def __init__(self, data_refresh_interval, count_data_take_device, count_log_data_records_auto_clean,
                 user_agreement):
        self.data_refresh_interval = data_refresh_interval
        self.count_data_take_device = count_data_take_device
        self.count_log_data_records_auto_clean = count_log_data_records_auto_clean
        self.user_agreement = user_agreement


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

# log table
class Log(Base):
    __tablename__ = 'log'
    id = Column('id', Integer, primary_key=True)
    date = Column('date', DateTime)
    message = Column('message', String)

    def __init__(self, message):
        self.date = datetime.datetime.now()
        self.message = message
