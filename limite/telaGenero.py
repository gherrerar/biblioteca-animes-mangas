from limite.abstractTela import AbstractTela
import PySimpleGUI as sg


class TelaGenero(AbstractTela):
    def __init__(self):
        pass

    def mostra_generos(self, generos):
        if not generos:
            self.mostra_mensagem("Nenhum genero foi cadastrado")
        else:
            msg = "LISTA DE GENEROS\n"
            for gen in generos:
                msg += f"{gen.nome}\n"
            self.mostra_mensagem(msg)

    def recolhe_dados_genero(self) -> str:
        print(f"{'DADOS GENERO':-^30}")
        nome = super().le_texto("Nome: ")
        return nome
