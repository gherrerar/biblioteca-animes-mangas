from limite.abstractTela import AbstractTela


class TelaPrincipal(AbstractTela):
    def __init__(self):
        pass

    def mostra_opcoes(self) -> int:
        print(f"{'SISTEMA':-^30}")
        print("1 - Usuário Administrador")
        print("2 - Usuário Comum")
        print("0 - Encerrar")

        opcao = super().le_num_inteiro("Escolha uma opcao: ", range(3))
        return opcao
