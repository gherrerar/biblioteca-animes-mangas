from episodio import Episodio


class Temporada:
    def __init__(self, numero: int, num_episodios: int):
        self.__numero = None
        self.__num_episodios = None
        self.__episodios = []
        if isinstance(numero, int):
            self.__numero = numero
        if isinstance(num_episodios, int):
            self.__num_episodios = num_episodios

    @property
    def numero(self) -> int:
        return self.__numero

    @numero.setter
    def numero(self, numero: int):
        if isinstance(numero, int):
            self.__numero = numero

    @property
    def num_episodios(self) -> int:
        return self.__num_episodios

    @num_episodios.setter
    def num_episodios(self, num_episodios: int):
        if isinstance(num_episodios, int):
            self.__num_episodios = num_episodios

    @property
    def episodios(self) -> list[Episodio]:
        return self.__episodios

    def add_episodio(self, numero_ep: int, duracao_ep: int) -> Episodio:
        if self.find_episodio_by_numero(numero_ep) == None:
            episodio = Episodio(numero_ep, duracao_ep)
            self.__episodios.append(episodio)
            return episodio

    def rem_episodio(self, numero_ep: int):
        episodio = self.find_episodio_by_numero(numero_ep)
        if episodio != None:
            self.__episodios.remove(episodio)

    def find_episodio_by_numero(self, numero_ep: int) -> Episodio | None:
        if self.__episodios and isinstance(numero_ep, int):
            for ep in self.__episodios:
                if ep.numero == numero_ep:
                    return ep
            return None
