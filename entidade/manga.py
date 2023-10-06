from obra import Obra
from genero import Genero
from volume import Volume


class Manga(Obra):
    def __init__(self,
                 titulo: str,
                 ano: int,
                 genero: Genero,
                 num_volumes: int,
                 numero_vol: int,
                 num_capitulos_vol: int):
        super().__init__(titulo, ano, genero)
        self.__autor = None
        self.__num_volumes = None
        self.__volumes = []
        if isinstance(num_volumes, int):
            self.__num_volumes = num_volumes
        if isinstance(numero_vol, int) and isinstance(num_capitulos_vol, int):
            self.__volumes.append(Volume(numero_vol, num_capitulos_vol))

    @property
    def autor(self):
        return self.__autor

    def config_autor(self, autor):
        self.__autor = autor

    @property
    def num_volumes(self) -> int:
        return self.__num_volumes

    @num_volumes.setter
    def num_volumes(self, num_volumes):
        if isinstance(num_volumes, int):
            self.__num_volumes = num_volumes

    @property
    def volumes(self) -> list[Volume]:
        return self.__volumes

    def add_volume(self, numero_vol: int, num_capitulos_vol: int) -> Volume:
        if self.find_volume_by_numero(numero_vol) == None:
            volume = Volume(numero_vol, num_capitulos_vol)
            self.__volumes.append(volume)
            return volume

    def rem_volume(self, numero_vol: int):
        self.__existe_volume(numero_vol, self.__volumes.remove)

    def add_capitulo_volume(self, numero_vol: int, numero_cap: int, num_paginas_cap: int):
        self.__existe_volume(numero_vol, 'add_capitulo', numero_cap, num_paginas_cap)

    def rem_capitulo_volume(self, numero_vol: int, numero_cap: int):
        self.__existe_volume(numero_vol, 'rem_capitulo', numero_cap)

    def __existe_volume(self, numero_vol: int, metodo, *args):
        volume = self.find_volume_by_numero(numero_vol)
        if volume != None:
            if isinstance(metodo, str):
                metodo = getattr(volume, metodo)
            metodo(*args if args else [volume])

    def find_volume_by_numero(self, numero_vol: int) -> Volume | None:
        if self.__volumes and isinstance(numero_vol, int):
            for vol in self.__volumes:
                if vol.numero == numero_vol:
                    return vol
            return None

    def total_capitulos(self) -> int:
        return sum([vol.num_capitulos for vol in self.__volumes])
