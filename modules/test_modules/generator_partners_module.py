from models.db_models.models import PartnersCatalog
from db.db import session
from flask import Flask, jsonify, request
from flask_restful import Resource, fields, marshal_with, abort, reqparse
import modules.db_model_tranformer_modules.db_model_transformer_module as db_transformer
import modules.db_help_modules.user_action_logging_module as user_action_logging
from sqlalchemy import desc
import random


def generate_partners():
    try:
        partner_names = ['EURASIAN FOODS',
                         'Келешек - STAR',
                         'Dala-Kent',
                         'Южный Престиж',
                         'Madina',
                         'ИП "Кофейные напитки"',
                         'Бөрте Милка',
                         'Доставка лепешек',
                         'ИП Хасанова',
                         'ASDECOR',
                         'ИП НҰРМҰХАММЕД',
                         'Южная Корона',
                         'ИП Париж',
                         'Красивая Меча',
                         'ТОО АРСЕНОВ',
                         'ИП Ерганов'
                         'PANDORA GROUP',
                         'ТОО Омар(Yunus, Comili,Elvan,Today)',
                         'ИП Санжар',
                         'ИП Шым-Бизнес (Bionix, Voka)',
                         'VOKA',
                         'BIONIX',
                         'Нирвана',
                         'ИП Ахмедов',
                         'ТОО "Dena Distribution"',
                         'ТОО "Hydrolife Bottlers Kazakhstan"',
                         'Anadolu Marketing',
                         'ИП Юдаков',
                         'BASTAU',
                         'ТОО "РАУАН"',
                         'ТОО "NIK 1"',
                         'BRIS -Company',
                         'ТОО "Чайный центр"',
                         'Разновидный курт',
                         'TURKUAZ Group of Companies',
                         'ТОО "Салем"',
                         'ТОО "ЖанИС"',
                         'ТОО "Московские Деликатесы"',
                         'ИП Хадиметов',
                         'ТОО "Line Logistic"',
                         'ТОО "Аврора Брендс"',
                         'Арахис Ташкентский',
                         'ИП Леспеков',
                         'ТОО "АсКом-Азия"',
                         'ТОО OASIS GROUP',
                         'ТОО "Гәкку Әулие ата құс"',
                         'Адам',
                         'ИП "Дарина"',
                         'ТОО "Sea Bass" (Русалочка)',
                         'ИП Болатбек Т',
                         'ТОО "TASS GROUP"',
                         'ИП Пак',
                         'aДәм']

        for name in partner_names:
            data = {'name': name}
            partner = PartnersCatalog(data)
            session.add(partner)
            session.commit()

        pass
    except Exception as e:
        pass
