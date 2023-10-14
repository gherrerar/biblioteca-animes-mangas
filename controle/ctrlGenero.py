from entidade.genero import Genero
from limite.telaGenero import TelaGenero


class CtrlGenero:
    def __init__(self, ctrl_principal):
        self.__generos = []
        self.__tela_genero = TelaGenero()
        self.__ctrl_principal = ctrl_principal

    @property
    def generos(self):
        return self.__generos

    def abrir_tela(self):
        opcoes = {
            1: self.listar_generos,
            2: self.incluir_genero,
            0: self.retornar
        }

        while True:
            opcoes[self.__tela_genero.mostra_opcoes()]()

    def listar_generos(self):
        if self.__generos:
            for gen in self.__generos:
                self.__tela_genero.mostra_genero(gen.nome)
        else:
            self.__tela_genero.mostra_genero(None)

    def incluir_genero(self, nome: str = ''):
        nome_genero = nome or self.__tela_genero.recolhe_dados_genero()
        if self.find_genero_by_nome(nome_genero) == None:
            genero = Genero(nome_genero)
            self.__generos.append(genero)

    def find_genero_by_nome(self, nome: str) -> Genero | None:
        if self.__generos and isinstance(nome, str):
            for gen in self.__generos:
                if gen.nome == nome:
                    return gen
            return None

    def retornar(self):
        pass
