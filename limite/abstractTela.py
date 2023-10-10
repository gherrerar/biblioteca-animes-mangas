from abc import ABC, abstractmethod


class AbstractTela(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def le_num_inteiro(self, mensagem: str = "", nums_validos: [] = None) -> int:
        while True:
            valor = input(mensagem)
            try:
                inteiro = int(valor)
                if nums_validos and inteiro not in nums_validos:
                    raise ValueError
                return inteiro
            except ValueError:
                self.mostra_mensagem("Valor incorreto! Digite um número inteiro válido")
                if nums_validos:
                    self.mostra_mensagem(">>> Valores válidos: ", *nums_validos)

    def mostra_mensagem(self, *msg: str):
        print(*msg)
