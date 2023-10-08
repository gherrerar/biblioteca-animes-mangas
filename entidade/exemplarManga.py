from entidade.exemplar import Estado, Exemplar
from entidade.manga import Manga


class ExemplarManga(Exemplar):
    def __init__(self, manga: Manga, etiqueta: Estado):
        super().__init__(etiqueta)
        self.__manga = None
        if isinstance(manga, Manga):
            self.__manga = manga

    @property
    def manga(self) -> Manga:
        return self.__manga

    @manga.setter
    def manga(self, manga: Manga):
        if isinstance(manga, Manga):
            self.__manga = manga
