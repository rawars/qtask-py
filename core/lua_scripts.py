import os

class LuaScriptLoader:
    def __init__(self, redis_conn, base_path=None):
        self.redis = redis_conn
        self.scripts = {}
        if base_path is None:
            self.base_path = os.path.join(os.path.dirname(__file__), 'lua')
        else:
            self.base_path = base_path

    def load_script(self, name):
        path = os.path.join(self.base_path, f'{name}.lua')
        with open(path, 'r') as f:
            code = f.read()
        self.scripts[name] = self.redis.register_script(code)

    def run(self, name, keys=[], args=[]):
        if name not in self.scripts:
            self.load_script(name)
        return self.scripts[name](keys=keys, args=args)