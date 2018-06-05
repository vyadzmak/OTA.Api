def transform_constructor_params(model, args):
    for a in args:
        p = a
        for key in p:
            s_key = key
            s_value = p[key]
            if hasattr(model, s_key):
                setattr(model, s_key, s_value)



def transform_update_params(model, args):
        for key in args:
            s_key = key
            s_value = args[key]
            if hasattr(model, s_key):
                setattr(model, s_key, s_value)

