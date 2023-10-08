from entidade.capitulo import Capitulo


class Volume:
    def __init__(self, numero: int, num_capitulos: int):
        self.__numero = None
        self.__num_capitulos = None
        self.__capitulos = []
        if isinstance(numero, int):
            self.__numero = numero
        if isinstance(num_capitulos, int):
            self.__num_capitulos = num_capitulos

    @property
    def numero(self) -> int:
        return self.__numero

    @numero.setter
    def numero(self, numero: int):
        if isinstance(numero, int):
            self.__numero = numero

    @property
    def num_capitulos(self) -> int:
        return self.__num_capitulos

    @num_capitulos.setter
    def num_capitulos(self, num_capitulos: int):
        if isinstance(num_capitulos, int):
            self.__num_capitulos = num_capitulos

    @property
    def capitulos(self) -> list[Capitulo]:
        return self.__capitulos

    def add_capitulo(self, numero_cap: int, num_paginas_cap: int) -> Capitulo:
        if self.find_capitulo_by_numero(numero_cap) == None:
            capitulo = Capitulo(numero_cap, num_paginas_cap)
            self.__capitulos.append(capitulo)
            return capitulo

    def rem_capitulo(self, numero_cap: int):
        capitulo = self.find_capitulo_by_numero(numero_cap)
        if capitulo != None:
            self.__capitulos.remove(capitulo)

    def find_capitulo_by_numero(self, numero_cap: int) -> Capitulo | None:
        if self.__capitulos and isinstance(numero_cap, int):
            for cap in self.__capitulos:
                if cap.numero == numero_cap:
                    return cap
            return None
