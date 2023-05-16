import yaml


class Data:
    def __init__(self, app_name, path):
        self.flag = True

        with open(path) as f:
            try:
                self.data = yaml.full_load(f)[app_name]
            except Exception:
                self.flag = False
                pass
