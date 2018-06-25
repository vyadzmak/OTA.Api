from models.db_models.models import Products, ProductComments
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import desc
import random
def generate_comments():
    try:
        user_id = 1
        comments = [
            'Все ОК',
            'Отлично',
            'Спасибо',
            "Товар понравился",
            "Буду покупать еще",
            "Отвратительно"

        ]

        products = session.query(Products).all()

        product_ids = []

        for product in products:
            product_ids.append(product.id)

        count = 0

        for i in range(0,count):
            p_r =random.randint(0,len(product_ids)-1)
            p_id = product_ids[p_r]
            c_r = random.randint(0,len(comments)-1)
            comment_text = comments[c_r]
            rate = random.randint(0,5)
            com = {'user_id':user_id, 'product_id':p_id, 'comment_text':comment_text,'rate':rate}
            comment = ProductComments(com)
            session.add(comment)
            session.commit()








        pass
    except Exception as e:
        pass