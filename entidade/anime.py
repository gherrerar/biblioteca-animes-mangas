from entidade.obra import Obra
from entidade.genero import Genero
from entidade.temporada import Temporada


class Anime(Obra):
    def __init__(self,
                 titulo: str,
                 ano: int,
                 genero: Genero,
                 num_temporadas: int,
                 numero_temp: int,
                 num_episodios_temp: int):
        super().__init__(titulo, ano, genero)
        self.__estudio = None
        self.__num_temporadas = None
        self.__temporadas = []
        if isinstance(num_temporadas, int):
            self.__num_temporadas = num_temporadas
        if isinstance(numero_temp, int) and isinstance(num_episodios_temp, int):
            self.__temporadas.append(Temporada(numero_temp, num_episodios_temp))

    @property
    def estudio(self):
        return self.__estudio

    def config_estudio(self, estudio):
        self.__estudio = estudio

    @property
    def num_temporadas(self) -> int:
        return self.__num_temporadas

    @num_temporadas.setter
    def num_temporadas(self, num_temporadas: int):
        if isinstance(num_temporadas, int):
            self.__num_temporadas = num_temporadas

    @property
    def temporadas(self) -> list[Temporada]:
        return self.__temporadas

    def add_temporada(self, numero_temp: int, num_episodios_temp: int) -> Temporada:
        if self.find_temporada_by_numero(numero_temp) == None:
            temporada = Temporada(numero_temp, num_episodios_temp)
            self.__temporadas.append(temporada)
            return temporada

    def rem_temporada(self, numero_temp: int):
        self.__existe_temporada(numero_temp, self.__temporadas.remove)

    def add_episodio_temporada(self, numero_temp: int, numero_ep: int, duracao_ep: int):
        self.__existe_temporada(numero_temp, 'add_episodio', numero_ep, duracao_ep)

    def rem_episodio_temporada(self, numero_temp: int, numero_ep: int):
        self.__existe_temporada(numero_temp, 'rem_episodio', numero_ep)

    def __existe_temporada(self, numero_temp: int, metodo, *args):
        temporada = self.find_temporada_by_numero(numero_temp)
        if temporada != None:
            if isinstance(metodo, str):
                metodo = getattr(temporada, metodo)
            metodo(*args if args else [temporada])

    def find_temporada_by_numero(self, numero_temp: int) -> Temporada | None:
        if self.__temporadas and isinstance(numero_temp, int):
            for temp in self.__temporadas:
                if temp.numero == numero_temp:
                    return temp
            return None

    def total_episodios(self) -> int:
        return sum([temp.num_episodios for temp in self.__temporadas])
