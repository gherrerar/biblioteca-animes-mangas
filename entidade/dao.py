import inspect
import importlib
import pickle


class DAO:
    def __init__(self, identifier: str, id_type):
        self.__handle_class_reference()
        self.__identifier = identifier
        self.__id_type = id_type
        self.__cache = {}
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __handle_class_reference(self):
        class_name = inspect.currentframe(
        ).f_back.f_back.f_locals["self"].__class__.__name__.replace('Ctrl', '')

        self.__datasource = class_name[0].lower() + class_name[1:] + '.pkl'
        self.__class = getattr(importlib.import_module(
            f'entidade.{self.__datasource[:-4]}'), class_name)

    def __dump(self):
        pickle.dump(self.__cache, open(self.__datasource, 'wb'))

    def __load(self):
        self.__cache = pickle.load(open(self.__datasource, 'rb'))

    def add(self, obj):
        if isinstance(obj, self.__class):
            key = getattr(obj, self.__identifier)
            self.__cache[key] = obj
            self.__dump()

    def get(self, key):
        if isinstance(key, self.__id_type):
            try:
                return self.__cache[key]
            except KeyError:
                pass

    def remove(self, key):
        if isinstance(key, self.__id_type):
            try:
                self.__cache.pop(key)
                self.__dump()
            except KeyError:
                pass

    def get_all(self):
        return self.__cache.values()
