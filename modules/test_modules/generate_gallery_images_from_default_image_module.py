from models.db_models.models import Products, ProductComments
from db.db import session
from sqlalchemy import and_
def generate_gallery():
    try:
        # user_login = session.query(UserLogins).filter(and_(
        #     UserLogins.login == login,
        #     UserLogins.password == encrypted_password)) \
        #     .first()
        products = session.query(Products).filter(and_(
            Products.default_image_id!=None,
            Products.gallery_images==None
        )).all()

        for p in products:
            arr = []
            arr.append(p.default_image_id)
            p.gallery_images = arr
            session.add(p)
            session.commit()


            t=p
            pass

        e=0
        pass
    except Exception as e:
        pass