from models.db_models.models import Log, Users
from db.db import session
import datetime


def clean_log_by_condition():
    try:
        logs = session.query(Log).all()

        if (len(logs) > 2000):
            session.query(Log).delete()
            session.commit()
        pass
    except Exception as e:
        session.rollback()

def log_user_actions(route, user_id, action_type):
    try:
        clean_log_by_condition()
        user = session.query(Users).filter(Users.id == user_id).first()
        user_name = user.name
        client_name = user.client_data.name
        date = datetime.datetime.now(datetime.timezone.utc)
        message =("Пользователь {0}, компания {1}, выполнил действие {2} на роуте {3}").format(user_name,client_name,action_type,route)
        l_message={'date':date,'message':message}
        log = Log(l_message)
        session.add(log)
        session.commit()
        pass
    except:
        pass