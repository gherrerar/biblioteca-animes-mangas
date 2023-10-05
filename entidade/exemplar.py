from abc import ABC, abstractmethod
from enum import Enum


class Estado(Enum):
    NAO_INICIADO = "Nao Iniciado"
    EM_ANDAMENTO = "Em Andamento"
    COMPLETO = "Completo"
    ABANDONADO = "Abandonado"

class Exemplar(ABC):
    @abstractmethod
    def __init__(self, etiqueta: Estado):
        self.__etiqueta = None
        if isinstance(etiqueta, Estado):
            self.__etiqueta = etiqueta

    @property
    def etiqueta(self) -> Estado:
        return self.__etiqueta

    @etiqueta.setter
    def etiqueta(self, etiqueta):
        if isinstance(etiqueta, Estado):
            self.__etiqueta = etiqueta
