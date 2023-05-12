import yaml


class Data:
    def __init__(self, app_name, path):
        with open(path) as f:
            self.data = yaml.full_load(f)[app_name]