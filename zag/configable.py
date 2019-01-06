import re
import copy

RX = re.compile('\$(\w+)')

class ConfigException(Exception):
    pass

def substitute(m, config):
    keyword = m.groups()[0]
    if keyword not in config:
        raise ConfigException("Variable `{}` not defined!".format(keyword))

    return config[keyword]

def apply_config(o, config):
    if isinstance(o, basestring):
        return RX.sub(lambda m: substitute(m, config), o)
        
    if isinstance(o, list):
        return [apply_config(item, config) for item in o]

    if isinstance(o, tuple):
        return tuple(apply_config(item, config) for item in o)

    if isinstance(o, set):
        return set(apply_config(item, config) for item in o)

    if isinstance(o, dict):
        return {apply_config(k, config): apply_config(v, config) for k,v in o.items()}
    
    if isinstance(o, Configable):
        no = copy.deepcopy(o)
        for attr, value in no.__dict__.items():
            setattr(no, attr, apply_config(value, config))

        return no

    return o

class Configable(object):

    def get_config(self):
        return {}

    def apply_config(self, config):
        return type(self)(**apply_config(self.__dict__, config))


