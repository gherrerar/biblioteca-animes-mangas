from entidade.exemplar import Estado, Exemplar
from entidade.anime import Anime


class ExemplarAnime(Exemplar):
    def __init__(self, anime: Anime, etiqueta: Estado):
        super().__init__(etiqueta)
        self.__anime = None
        if isinstance(anime, Anime):
            self.__anime = anime

    @property
    def anime(self) -> Anime:
        return self.__anime

    @anime.setter
    def anime(self, anime: Anime):
        if isinstance(anime, Anime):
            self.__anime = anime

    def __repr__(self) -> int:
        return f"{self.anime.titulo}"
