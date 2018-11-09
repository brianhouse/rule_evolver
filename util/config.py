import os, shutil, __main__, yaml


class Config(dict):

    def __init__(self):    
        with open(os.path.abspath(os.path.join(os.path.dirname(__main__.__file__), "config.yaml"))) as f:
            data = yaml.load(f)
        data = {} if data is None else data
        dict.__init__(self, data)
        f.close()
        
    def __missing__(self, key):
        raise ConfigError(key)


class ConfigError(Exception):

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return repr("No '%s' in config" % self.key)
                 

config = Config()