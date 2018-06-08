import json
import jsonpickle

def encode(ob,unpickable=False):
    try:
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)
        #if (unpickable==False):
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        json_s = jsonpickle.encode(ob, unpicklable=False)
        return json_s
    except Exception as e:
        print(str(e))
        return ""

def decode(js):
    try:
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)
        jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)
        obj = jsonpickle.decode(js)
        return obj
    except Exception as e:
        print(str(e))
        return ""