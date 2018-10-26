import requests
from modules.http.smsc_api import *
def send_sms(phone, message):
    try:
        smsc = SMSC()
        #
        # r = smsc.send_sms(phone, "Код подтверждения: "+message, sender="sms")
        login = "sundet_ota"
        password = "ota12345"
        message="Код подтверждения: "+message
        url = "http://cabinet.brandsms.kz/sys/send.php?login="+login+"&psw="+password+"&phones="+phone+"&mes="+message+"&charset=utf-8"
        r = requests.get(url)

        sundet_phone_number ='+77077750095'
        balance = float(smsc.get_balance())

        if (balance<100):
            message = "На балансе рассылки СМС ОТА осталось "+str(balance)+" тенге, скоро отключится рассылка. Пополните баланс"
            need_money_url = "http://cabinet.brandsms.kz/sys/send.php?login=" + login + "&psw=" + password + "&phones=" + sundet_phone_number + "&mes=" + message
            requests.get(need_money_url)
        pass
    except Exception as e:
        pass
