

class Episodio:
    def __init__(self, numero: int, duracao: int):
        self.__numero = None
        self.__duracao = None
        if isinstance(numero, int):
            self.__numero = numero
        if isinstance(duracao, int):
            self.__duracao = duracao

    @property
    def numero(self) -> int:
        return self.__numero

    @numero.setter
    def numero(self, numero: int):
        if isinstance(numero, int):
            self.__numero = numero

    @property
    def duracao(self) -> int:
        return self.__duracao

    @duracao.setter
    def duracao(self, duracao: int):
        if isinstance(duracao, int):
            self.__duracao = duracao
