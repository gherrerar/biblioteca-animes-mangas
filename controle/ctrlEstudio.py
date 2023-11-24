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
            1: self.listar_estudios,
            2: self.incluir_estudio,
            3: self.incluir_anime,
            0: self.retornar
        }
    
        while True:
            opcoes[self.__tela_estudio.mostra_opcoes()]()

    @property
    def estudio_dao(self):
        return self.__estudio_dao

    @property
    def __estudios(self):
        return self.__estudio_dao.get_all()

    def listar_estudios(self):
        if self.__estudios:
            for estudio in self.__estudios:
                self.__tela_estudio.mostra_estudio({
                    'nome': estudio.nome,
                    'animes': ', '.join(anime.titulo for anime in estudio.animes_produzidos)
                })
        else:
            self.__tela_estudio.mostra_estudio(None)

    def incluir_estudio(self):
        nome_estudio = self.__tela_estudio.recolhe_dados_estudio()
        try:
            if self.find_estudio_by_nome(nome_estudio) != None:
                raise ExistenceException("estudio")
            else:
                estudio = Estudio(nome_estudio)
                self.__estudio_dao.add(estudio)
                self.__tela_estudio.mostra_mensagem("Estudio cadastrado!")
        except ExistenceException as error:
            self.__tela_estudio.mostra_mensagem(f"{error}")

    def incluir_anime(self):
        if self.__estudios:
            estudio = self.__existe_estudio()
            anime = self.__existe_anime()
            if anime != None and estudio != None:
                if anime in estudio.animes_produzidos:
                    self.__tela_estudio.mostra_mensagem("Atencao! Este estudio e anime ja estao associados!")
                else:
                    estudio.add_anime(anime)
                    self.__tela_estudio.mostra_mensagem("Estudio e anime associados!")
                    self.__estudio_dao.add(estudio)
                    anime_dao = self.ctrl_principal.ctrl_anime.anime_dao
                    anime_dao.add(anime)
        else:
            self.__tela_estudio.mostra_mensagem("Nenhum estudio foi cadastrado!")

    def __existe_estudio(self):
        self.listar_estudios()
        nome_estudio = self.__tela_estudio.seleciona_estudio()
        estudio = self.find_estudio_by_nome(nome_estudio)
        try:
            if estudio != None:
                return estudio
            else:
                raise ExistenceException("estudio", False)
        except ExistenceException as error:
            self.__tela_estudio.mostra_mensagem(f"{error}")
            self.abrir_tela()

    def __existe_anime(self):
        ctrl_anime = self.ctrl_principal.ctrl_anime
        ctrl_anime.listar_animes()
        titulo_anime = self.__tela_estudio.seleciona_anime()
        anime = ctrl_anime.find_anime_by_titulo(titulo_anime)
        try:
            if anime != None:
                return anime
            else:
                raise ExistenceException("anime", False)
        except ExistenceException as error:
            self.__tela_estudio.mostra_mensagem(f"{error}")
            self.abrir_tela()

    def find_estudio_by_nome(self, nome: str) -> Estudio | None:
        if isinstance(nome, str):
            estudio = self.__estudio_dao.get(nome)
            if estudio:
                return estudio
            return None

    def retornar(self):
        self.ctrl_principal.ctrl_anime.abrir_tela()
