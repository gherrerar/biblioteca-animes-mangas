from abc import ABC, abstractmethod


class Usuario(ABC):
    @abstractmethod
    def __init__(self, nome: str, senha: str):
        self.__nome = None
        self.__senha = None
        if isinstance(nome, str):
            self.__nome = nome
        if isinstance(senha, str):
            self.__senha = senha

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, senha: str):
        if isinstance(senha, str):
            self.__senha = senha
