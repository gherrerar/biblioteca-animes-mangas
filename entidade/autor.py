from manga import Manga


class Autor:
    def __init__(self, nome: str):
        self.__nome = None
        self.__mangas_produzidos = []
        if isinstance(nome, str):
            self.__nome = nome

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if isinstance(nome, str):
            self.__nome = nome

    def add_manga(self, manga: Manga):
        if isinstance(manga, Manga):
            self.__mangas_produzidos.append(manga)
