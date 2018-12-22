class Parser(object):
    type = ''

    @property
    def full_name(self):
        return '.'.join([self._parent, self._obj.__name__])

    def __init__(self, obj, parent=None):
        self._obj = obj
        self._members = {}
        self._parent = parent

    def self_member(self):
        import inspect
        self._members['type'] = self.type
        self._members['name'] = self.full_name
        self._members['doc'] = inspect.getdoc(self._obj)

    def set(self, key, value):
        self._members[key] = value

    def get(self, key):
        return self._members[key]

    def start(self):
        self._run()
        self.self_member()
        return {k: v for k, v in self._members.items() if (v is not None) and (len(v) > 0)}


class ModuleParser(Parser):
    type = 'module'

    @property
    def full_name(self):
        if self._parent is not None:
            return super().full_name
        return self._obj.__name__

    def _run(self):
        # Keep the imports in here so they don't polute the inspection
        import inspect
        import pkgutil
        import sys
        import importlib
        for member_type, func in {
            'classes': inspect.isclass,
            'functions': inspect.isfunction,
            'modules': inspect.ismodule,
        }.items():
            self.set(
                member_type,
                inspect.getmembers(
                    sys.modules[self._obj.__name__],
                    lambda m: func(m) and m.__module__ == self._obj.__name__
                )
            )
        self.set(
            'classes',
            [
                ClassParser(c[1], self.full_name).start()
                for c
                in self.get('classes')
            ]
        )
        if hasattr(self._obj, '__path__'):
            submodules = list(
                pkgutil.walk_packages(self._obj.__path__, prefix=self._obj.__name__ + '.', onerror=lambda x: None))
            self.set(
                'modules',
                [
                    ModuleParser(importlib.import_module(m.name), None).start()
                    for m
                    in submodules
                ]
            )


class ClassParser(Parser):
    """
    Creates a structure representing class object
    """
    type = 'class'

    def _run(self):
        import inspect
        for member_type, func in {
            'methods': inspect.ismethod,
            'functions': inspect.isfunction
        }.items():
            self.set(member_type, inspect.getmembers(self._obj, func))
        self.set(
            'functions',
            [
                FunctionParser(f[1], self.full_name).start()
                for f
                in self.get('functions')
            ]
        )


class FunctionParser(Parser):
    type = 'function'

    def _run(self):
        return {}
