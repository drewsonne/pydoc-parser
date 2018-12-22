"""
A library for parsing pydoc blocks
"""
from pydocparser.docblock import DocParser


class Parser(object):
    """
    Base parser class to handle self metadata and removing empty key values
    """
    type = ''

    @property
    def full_name(self):
        return '.'.join([self._parent, self.name])

    @property
    def name(self):
        return self._obj.__name__

    def __init__(self, obj, parent=None):
        """
        :param obj: An object like module, class, function, method, which can have a doc block extracted from it
        :param parent: A string representing the parent module path
        """

        if type(obj) == str:
            import importlib
            obj = importlib.import_module(obj)

        self._obj = obj
        self._parent = parent
        self._members = {}

    def self_member(self):
        import inspect
        self._members['type'] = self.type
        self._members['name'] = self.full_name
        self._members['short_name'] = self.name
        self._members['doc'] = DocParser(inspect.getdoc(self._obj)).start()

    def set(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        self._members[key] = value

    def get(self, key):
        return self._members[key]

    def _run(self):
        return {}

    def start(self):
        include = self._run()
        if (include == False) and (include is not None):
            return None
        self.self_member()
        return {k: v for k, v in self._members.items() if (v is not None)}


class ModuleParser(Parser):
    """
    Handle the parsing of Modules
    """
    type = 'module'

    @property
    def full_name(self):
        if self._parent is not None:
            return super().full_name
        return self.name

    def _run(self):
        # Keep the imports in here so they don't polute the inspection
        import inspect
        import pkgutil
        import sys
        import importlib

        name = self._obj.__name__

        def filter_func(func):
            def callback(m):
                if func(m):
                    if hasattr(m, '__module__'):
                        if m.__module__ == name:
                            return True
                    else:
                        return True
                return False

            return callback

        for member_type, func in {
            'classes': inspect.isclass,
            'functions': inspect.isfunction,
            'modules': inspect.ismodule,
        }.items():
            self.set(
                member_type,
                inspect.getmembers(
                    sys.modules[self._obj.__name__], filter_func(func))
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
        self.set('functions', [
            FunctionParser(f[1], self.full_name).start()
            for f in
            self.get('functions')
        ])


class ClassParser(Parser):
    """
    Creates a structure representing class object
    """
    type = 'class'

    def _run(self):
        import inspect
        for member_type, func in {
            'methods': inspect.isfunction
        }.items():
            self.set(member_type, inspect.getmembers(self._obj, func))
        self.set(
            'methods',
            filter(None, [
                FunctionParser(f[1], self.full_name).start()
                for f
                in self.get('methods')
            ])
        )
        self.set(
            'superclasses',
            [
                ".".join([n.__module__, n.__name__])
                for n in
                [
                    base for base
                    in self._obj.__bases__ if base != object
                ]
            ]
        )


class FunctionParser(Parser):
    """
    Creates a structure representing a function
    """
    type = 'function'

    def _run(self):
        from inspect import signature
        from collections import OrderedDict

        func_name_parts = self._obj.__qualname__.split(".")
        parent_parts = self._parent.split(".")
        real_path = ".".join(parent_parts[0:-1] + func_name_parts)

        # An inherited method
        if not real_path.startswith(self._parent):
            return False

        if not get('include_hidden'):
            if (self.name != '__init__') and (self.name.startswith('_')):
                return False

        sig = signature(self._obj)
        if get('json_friendly'):
            parsed_params = OrderedDict()
            for key, param in sig.parameters.items():
                if param.empty:
                    parsed_params[key] = None
                else:
                    parsed_params[key] = str(param.default)
            self.set(
                'params',
                parsed_params
            )
        else:
            self.set('params', sig.parameters)
            self.set('sig', sig)
        if self._parent is not None:
            self.set(
                'parent',
                self._parent
            )


__settings = {
    'include_hidden': False,
    'json_friendly': False
}


def set(key, value):
    __settings[key] = value


def get(key):
    if key not in __settings:
        return None
    return __settings[key]
