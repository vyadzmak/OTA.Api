
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from models.app_models.setting_models.setting_model import DB_URI

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=create_engine(DB_URI))
session = scoped_session(Session)

def init_session():
    Session = sessionmaker(autocommit=False,
                           autoflush=False,
                           bind=create_engine(DB_URI))
    session = scoped_session(Session)