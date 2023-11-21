from dao.dao import DAO
from entidade.anime import Anime


class AnimeDAO(DAO):
    def __init__(self):
        super().__init__('animes.pkl')

    def add(self, anime: Anime):
        if isinstance(anime, Anime):
            super().add(anime.titulo, anime)

    def get(self, titulo: str):
        if isinstance(titulo, str):
            return super().get(titulo)

    def remove(self, titulo: str):
        if isinstance(titulo, str):
            super().remove(titulo)
