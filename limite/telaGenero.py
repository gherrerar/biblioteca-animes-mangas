from limite.abstractTela import AbstractTela


class TelaGenero(AbstractTela):
    def __init__(self):
        pass

    def mostra_opcoes(self) -> int:
        print(f"{'GENEROS':-^30}")
        print("1 - Listar")
        print("2 - Cadastrar")
        print("0 - Voltar")

        opcao = super().le_num_inteiro("Escolha uma opcao: ", range(3))
        return opcao

    def mostra_genero(self, nome_genero: str):
        if not nome_genero:
            self.mostra_mensagem("Nenhum gênero foi cadastrado")
        else:
            print(nome_genero)

    def recolhe_dados_genero(self) -> str:
        print(f"{'DADOS GENERO':-^30}")
        nome = super().le_texto("Nome: ")
        return nome
