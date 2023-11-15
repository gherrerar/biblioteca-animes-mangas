from controle.abstractCtrl import AbstractCtrl
from limite.telaEstudio import TelaEstudio
from entidade.estudio import Estudio


class CtrlEstudio(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__estudios = []
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
        if self.find_estudio_by_nome(nome_estudio) != None:
            self.__tela_estudio.mostra_mensagem("Atencao! Este estudio ja existe!\n")
        else:
            estudio = Estudio(nome_estudio)
            self.__estudios.append(estudio)
            self.__tela_estudio.mostra_mensagem("Estudio cadastrado!")

    def incluir_anime(self):
        estudio = self.__existe_estudio()
        anime = self.__existe_anime()
        if anime in estudio.animes_produzidos:
            self.__tela_estudio.mostra_mensagem("Atencao! Este estudio e anime ja estao associados!")
        else:
            estudio.add_anime(anime)
            self.__tela_estudio.mostra_mensagem("Estudio e anime associados!")

    def __existe_estudio(self):
        self.listar_estudios()
        # while True:
        nome_estudio = self.__tela_estudio.seleciona_estudio()
        estudio = self.find_estudio_by_nome(nome_estudio)
        if estudio != None:
            return estudio
        else:
            self.__tela_estudio.mostra_mensagem("Atencao! Este estudio nao existe!\n")

    def __existe_anime(self):        
        ctrl_anime = self.ctrl_principal.ctrl_anime
        ctrl_anime.listar_animes()
        # while True:
        titulo_anime = self.__tela_estudio.seleciona_anime()
        anime = ctrl_anime.find_anime_by_titulo(titulo_anime)
        if anime != None:
            return anime
        else:
            self.__tela_estudio.mostra_mensagem("Atencao! Este anime nao existe!\n")

    def find_estudio_by_nome(self, nome: str) -> Estudio | None:
        if self.__estudios and isinstance(nome, str):
            for estudio in self.__estudios:
                if estudio.nome == nome:
                    return estudio
            return None

    def retornar(self):
        self.ctrl_principal.ctrl_anime.abrir_tela()
