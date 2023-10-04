

class Genero:
    def __init__(self, nome: str):
        self.__nome = None
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if isinstance(nome, str):
            self.__nome = nome
