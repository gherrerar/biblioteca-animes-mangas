from abc import ABC, abstractmethod
from entidade.genero import Genero


class Obra(ABC):
    @abstractmethod
    def __init__(self, titulo: str, ano: int, genero: Genero):
        self.__titulo = None
        self.__ano_lancamento = None
        self.__genero = None
        if isinstance(titulo, str):
            self.__titulo = titulo
        if isinstance(ano, int):
            self.__ano_lancamento = ano
        if isinstance(genero, Genero):
            self.__genero = genero

    @property
    def titulo(self) -> str:
        return self.__titulo

    @titulo.setter
    def titulo(self, titulo):
        if isinstance(titulo, str):
            self.__titulo = titulo

    @property
    def ano_lancamento(self) -> int:
        return self.__ano_lancamento

    @ano_lancamento.setter
    def ano_lancamento(self, ano):
        if isinstance(ano, int):
            self.__ano_lancamento = ano

    @property
    def genero(self) -> Genero:
        return self.__genero

    @genero.setter
    def genero(self, genero):
        if isinstance(genero, Genero):
            self.__genero = genero
