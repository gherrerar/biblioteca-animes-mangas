from controle.abstractCtrl import AbstractCtrl
from limite.telaEstudio import TelaEstudio
from entidade.estudio import Estudio
from entidade.dao import DAO
from exceptions.existenceException import ExistenceException


class CtrlEstudio(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__estudio_dao = DAO('nome', str)
        self.__tela_estudio = TelaEstudio()
        super().__init__(ctrl_principal)

    def abrir_tela(self):
        opcoes = {
            1: self.exibir_estudio,
            2: self.incluir_estudio,
            3: self.incluir_anime,
            0: self.retornar
        }

        while True:
            op, self.__selecionado_estudio = self.__tela_estudio.mostra_opcoes(
                self.__estudios)
            opcoes[op]()

    @property
    def estudio_dao(self):
        return self.__estudio_dao

    @property
    def __estudios(self):
        return self.__estudio_dao.get_all()

    def exibir_estudio(self):
        if self.__selecionado_estudio:
            self.__tela_estudio.mostra_estudio({
                'nome': self.__selecionado_estudio.nome,
                'animes': ', '.join(anime.titulo for anime in self.__selecionado_estudio.animes_produzidos)
            })
        else:
            self.__tela_estudio.mostra_estudio(None)

    def incluir_estudio(self):
        filtered_animes = self.__animes_sem_estudio()
        dados_estudio = self.__tela_estudio.recolhe_dados_estudio(
            filtered_animes)
        if dados_estudio == 'CANC':
            self.abrir_tela()
        try:
            if self.find_estudio_by_nome(dados_estudio) != None:
                raise ExistenceException("estudio")
            else:
                estudio = Estudio(dados_estudio)
                self.__estudio_dao.add(estudio)
                self.__tela_estudio.mostra_mensagem("Estudio cadastrado!")
        except ExistenceException as error:
            self.__tela_estudio.mostra_mensagem(f"{error}")

    def incluir_anime(self):
        if self.__estudios:
            estudio = self.__existe_estudio()
            filtered_animes = self.__animes_sem_estudio()
            dados_estudio = self.__tela_estudio.recolhe_dados_estudio(
                filtered_animes, estudio)
            if dados_estudio == 'CANC':
                self.abrir_tela()

            for anime in dados_estudio:
                if anime != None and estudio != None:
                    if anime in estudio.animes_produzidos:
                        self.__tela_estudio.mostra_mensagem(
                            f"{anime.titulo}:\nAtencao! Este estudio e anime ja estao associados!")
                    else:
                        estudio.add_anime(anime)
                        self.__tela_estudio.mostra_mensagem(
                            f"{anime.titulo}:\nEstudio e anime associados!")
                        self.__estudio_dao.add(estudio)
                        anime_dao = self.ctrl_principal.ctrl_anime.anime_dao
                        anime_dao.add(anime)
        else:
            self.__tela_estudio.mostra_mensagem(
                "Nenhum estudio foi cadastrado!")

    def __existe_estudio(self):
        estudio = self.__selecionado_estudio
        try:
            if estudio != None:
                return estudio
            else:
                raise ExistenceException("estudio", False)
        except ExistenceException as error:
            self.__tela_estudio.mostra_mensagem(f"{error}")
            self.abrir_tela()

    def __animes_sem_estudio(self):
        animes = self.ctrl_principal.ctrl_anime.animes
        return list(filter(
            lambda x: x.estudio == None, animes))

    def find_estudio_by_nome(self, nome: str) -> Estudio | None:
        if isinstance(nome, str):
            estudio = self.__estudio_dao.get(nome)
            if estudio:
                return estudio
            return None

    def retornar(self):
        self.ctrl_principal.ctrl_anime.abrir_tela()
