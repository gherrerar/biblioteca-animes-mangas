from controle.abstractCtrl import AbstractCtrl
from entidade.genero import Genero
from limite.telaGenero import TelaGenero
from entidade.dao import DAO


class CtrlGenero(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__genero_dao = DAO('nome', str)
        self.__tela_genero = TelaGenero()
        super().__init__(ctrl_principal)

    @property
    def generos(self):
        return self.__generos

    @property
    def __generos(self):
        return self.__genero_dao.get_all()

    def listar_generos(self):
        if self.__generos:
            self.__tela_genero.mostra_generos(self.__generos)
        else:
            self.__tela_genero.mostra_generos(None)

    def incluir_genero(self, nome: str = ''):
        nome_genero = nome or self.__tela_genero.recolhe_dados_genero()
        if self.find_genero_by_nome(nome_genero) == None:
            genero = Genero(nome_genero)
            self.__genero_dao.add(genero)

    def find_genero_by_nome(self, nome: str) -> Genero | None:
        if isinstance(nome, str):
            genero = self.__genero_dao.get(nome)
            if genero:
                return genero
            return None
