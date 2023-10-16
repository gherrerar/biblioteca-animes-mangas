from controle.abstractCtrl import AbstractCtrl
from entidade.exemplarAnime import ExemplarAnime
from entidade.exemplar import Estado
from limite.telaExemplarAnime import TelaExemplarAnime


class CtrlExemplarAnime(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__exemplares_anime = []
        self.__tela_exemplar_anime = TelaExemplarAnime()
        super().__init__(ctrl_principal)

    def abrir_tela(self):
        opcoes = {
            1: self.listar_exemplares,
            2: self.incluir_exemplar,
            0: self.retornar
        }

        while True:
            opcoes[self.__tela_exemplar_anime.mostra_opcoes()]()

    def listar_exemplares(self):
        if self.__exemplares_anime:
            for exemplar in self.__exemplares_anime:
                self.__tela_exemplar_anime.mostra_exemplar({
                    'anime': exemplar.anime,
                    'etiqueta': exemplar.etiqueta
                })
        else:
            self.__tela_exemplar_anime.mostra_exemplar(None)

    def incluir_exemplar(self, out_anime = None):
        def inner(anime):
            exemplar = self.find_exemplar_by_anime(anime.titulo)
            if exemplar != None:
                self.__tela_exemplar_anime.mostra_mensagem("Atenção! Este exemplar de anime já existe")
            else:
                exemplar = ExemplarAnime(anime, Estado.NAO_INICIADO)
                self.__exemplares_anime.append(exemplar)
                self.__tela_exemplar_anime.mostra_mensagem("Exemplar cadastrado!\n")
        if out_anime:
            exemplar = ExemplarAnime(out_anime, Estado.EM_ANDAMENTO)
            self.__exemplares_anime.append(exemplar)
            return exemplar
        self.__existe_anime(inner)

    def editar_etiqueta_exemplar(self, exemplar):
        for eti in Estado:
            self.__tela_exemplar_anime.mostra_etiqueta_estado(eti.value)
        valor_etiqueta = self.__tela_exemplar_anime.recolhe_dados_etiqueta()
        etiqueta = Estado(valor_etiqueta)
        if etiqueta in Estado:
            exemplar.etiqueta = etiqueta
            self.__tela_exemplar_anime.mostra_mensagem("Etiqueta alterada!\n")
        else:
            self.__tela_exemplar_anime.mostra_mensagem(
                "Atenção! Este não é um valor válido para a etiqueta"
            )

    def __existe_anime(self, func):
        ctrl_anime = self.ctrl_principal.ctrl_anime
        while True:
            titulo_anime = self.__tela_exemplar_anime.recolhe_dados_exemplar()
            anime = ctrl_anime.find_anime_by_titulo(titulo_anime)
            if anime != None:
                func(anime)
                break
            else:
                self.__tela_exemplar_anime.mostra_mensagem("Atenção! Este anime não existe")

    def find_exemplar_by_anime(self, titulo_anime: str) -> ExemplarAnime | None:
        if self.__exemplares_anime and isinstance(titulo_anime, str):
            for exemplar in self.__exemplares_anime:
                if exemplar.anime.titulo == titulo_anime:
                    return exemplar
            return None
