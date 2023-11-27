from entidade.usuario import Usuario
from entidade.exemplarAnime import ExemplarAnime
from entidade.exemplarManga import ExemplarManga
from entidade.genero import Genero
from entidade.exemplar import Estado


class UsuarioComum(Usuario):
    def __init__(self, nome: str, senha: str):
        super().__init__(nome, senha)
        self.__animes = []
        self.__mangas = []

    def __repr__(self) -> int:
        return f"{self.nome}"

    @property
    def animes(self) -> list[ExemplarAnime]:
        return self.__animes

    @property
    def mangas(self) -> list[ExemplarManga]:
        return self.__mangas

    def add_anime(self, exemplar: ExemplarAnime) -> ExemplarAnime:
        if (isinstance(exemplar, ExemplarAnime) and
                self.find_anime_by_titulo(exemplar.anime.titulo) == None):
            self.__animes.append(exemplar)
            return exemplar

    def rem_anime(self, exemplar: ExemplarAnime):
        anime = self.find_anime_by_titulo(exemplar.anime.titulo)
        if anime != None:
            self.__animes.remove(anime)

    def add_manga(self, exemplar: ExemplarManga) -> ExemplarManga:
        if (isinstance(exemplar, ExemplarManga) and
                self.find_manga_by_titulo(exemplar.manga.titulo) == None):
            self.__mangas.append(exemplar)
            return exemplar

    def rem_manga(self, exemplar: ExemplarManga):
        manga = self.find_manga_by_titulo(exemplar.manga.titulo)
        if manga != None:
            self.__mangas.remove(manga)

    def editar_etiqueta_anime(self, titulo: str, etiqueta: Estado):
        exemplar = self.find_anime_by_titulo(titulo)
        if exemplar != None and isinstance(etiqueta, Estado):
            exemplar.etiqueta = etiqueta

    def editar_etiqueta_manga(self, titulo: str, etiqueta: Estado):
        exemplar = self.find_manga_by_titulo(titulo)
        if exemplar != None and isinstance(etiqueta, Estado):
            exemplar.etiqueta = etiqueta

    def find_anime_by_titulo(self, titulo: str) -> ExemplarAnime | None:
        if self.__animes and isinstance(titulo, str):
            for exemplar in self.__animes:
                if exemplar.anime.titulo == titulo:
                    return exemplar
            return None

    def find_manga_by_titulo(self, titulo: str) -> ExemplarManga | None:
        if self.__mangas and isinstance(titulo, str):
            for exemplar in self.__mangas:
                if exemplar.manga.titulo == titulo:
                    return exemplar
            return None

    def total_horas_assistidas(self) -> float:
        return sum(
            episodio.duracao
            for exemplar in self.__animes
            if exemplar.etiqueta.value == "Completo"
            for temporada in exemplar.anime.temporadas
            for episodio in temporada.episodios
        )/60

    def total_paginas_lidas(self) -> int:
        return sum(
            capitulo.num_paginas
            for exemplar in self.__mangas
            if exemplar.etiqueta.value == "Completo"
            for volume in exemplar.manga.volumes
            for capitulo in volume.capitulos
        )

    def ultimos_animes(self) -> list[ExemplarAnime]:
        return self.__animes[-3:][::-1]

    def ultimos_mangas(self) -> list[ExemplarManga]:
        return self.__mangas[-3:][::-1]

    def principal_genero_animes(self) -> Genero | None:
        lista_generos = [exemplar.anime.genero for exemplar in self.__animes]
        if lista_generos:
            principal_genero = max(lista_generos, key=lista_generos.count)
            return principal_genero
        return None

    def principal_genero_mangas(self) -> Genero | None:
        lista_generos = [exemplar.manga.genero for exemplar in self.__mangas]
        if lista_generos:
            principal_genero = max(lista_generos, key=lista_generos.count)
            return principal_genero
        return None
