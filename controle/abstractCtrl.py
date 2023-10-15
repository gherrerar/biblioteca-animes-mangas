from abc import ABC, abstractmethod


class AbstractCtrl(ABC):
    @abstractmethod
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal

    @property
    def ctrl_principal(self):
        return self.__ctrl_principal

    def retornar(self):
        self.__ctrl_principal.abrir_tela()
