from controle.abstractCtrl import AbstractCtrl
from entidade.exemplarManga import ExemplarManga
from entidade.exemplar import Estado
from limite.telaExemplarManga import TelaExemplarManga


class CtrlExemplarManga(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__exemplares_manga = []
        self.__tela_exemplar_manga = TelaExemplarManga()
        super().__init__(ctrl_principal)

    def abrir_tela(self):
        opcoes = {
            1: self.listar_exemplares,
            2: self.incluir_exemplar,
            0: self.retornar
        }

        while True:
            opcoes[self.__tela_exemplar_manga.mostra_opcoes()]()

    def listar_exemplares(self):
        if self.__exemplares_manga:
            for exemplar in self.__exemplares_manga:
                self.__tela_exemplar_manga.mostra_exemplar({
                    'manga': exemplar.manga,
                    'etiqueta': exemplar.etiqueta
                })
        else:
            self.__tela_exemplar_manga.mostra_exemplar(None)

    def incluir_exemplar(self, out_manga = None):
        def inner(manga):
            exemplar = self.find_exemplar_by_manga(manga.titulo)
            if exemplar != None:
                self.__tela_exemplar_manga.mostra_mensagem("Atencao! Este exmplar de manga ja existe!")
            else:
                exemplar = ExemplarManga(manga, Estado.NAO_INICIADO)
                self.__exemplares_manga.append(exemplar)
                self.__tela_exemplar_manga.mostra_mensagem("Exemplar cadastrado!\n")
        if out_manga:
            exemplar = ExemplarManga(out_manga, Estado.EM_ANDAMENTO)
            self.__exemplares_manga.append(exemplar)
            return exemplar
        self.__existe_manga(inner)

    def __existe_manga(self, func):
        ctrl_manga = self.ctrl_principal.ctrl_manga
        while True:
            titulo_manga = self.__tela_exemplar_manga.recolhe_dados_exemplar()
            manga = ctrl_manga.find_manga_by_titulo(titulo_manga)
            if manga != None:
                func(manga)
                break
            else:
                self.__tela_exemplar_manga.mostra_mensagem("Atencao! Este manga nao existe!")

    def find_exemplar_by_manga(self, titulo_manga: str) -> ExemplarManga | None:
        if self.__exemplares_manga and isinstance(titulo_manga, str):
            for exemplar in self.__exemplares_manga:
                if exemplar.manga.titulo == titulo_manga:
                    return exemplar
            return None
