from anime import Anime


class Estudio:
    def __init__(self, nome: str):
        self.__nome = None
        self.__animes_produzidos = []
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if isinstance(nome, str):
            self.__nome = nome

    def add_anime(self, anime: Anime):
        if isinstance(anime, Anime) and anime not in self.__animes_produzidos:
            anime.config_estudio(self)
            self.__animes_produzidos.append(anime)
