from limite.abstractTela import AbstractTela


class TelaEstudio(AbstractTela):
    def __init__(self):
        pass

    def mostra_opcoes(self) -> int:
        print(f"{'ESTUDIO':-^30}")
        print("1 - Listar")
        print("2 - Cadastrar")
        print("3 - Incluir Anime")
        print("0 - Voltar")

        opcao = super().le_num_inteiro("Escolha uma opcao: ", range(4))
        return opcao

    def mostra_estudio(self, dados_estudio: {}):
        if not dados_estudio:
            self.mostra_mensagem("Nenhum estudio foi cadastrado!")
        else:
            print("NOME:", dados_estudio['nome'])
            print("ANIMES:", dados_estudio['animes'] or 'Nenhum vinculado')
            print()

    def recolhe_dados_estudio(self) -> str:
        print(f"{'DADOS ESTUDIO':-^30}")
        nome = super().le_texto("Nome: ")
        return nome

    def seleciona_estudio(self) -> str:
        print(f"{'SELECIONA ESTUDIO':-^30}")
        nome = super().le_texto("Nome: ")
        return nome

    def seleciona_anime(self) -> str:
        print(f"{'SELECIONA ANIME':-^30}")
        titulo = super().le_texto("Titulo: ")
        return titulo
