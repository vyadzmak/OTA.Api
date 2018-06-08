import json
class UserData():
    id = -1
    name =""
    def __init__(self):
        pass
class AuthModel():
    login =""
    password =""
    def __init__(self):
        self.user_data =UserData()
        pass

