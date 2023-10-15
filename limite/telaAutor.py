from limite.abstractTela import AbstractTela


class TelaAutor(AbstractTela):
    def __init__(self):
        pass

    def mostra_opcoes(self) -> int:
        print(f"{'AUTOR':-^30}")
        print("1 - Listar")
        print("2 - Cadastrar")
        print("3 - Incluir Manga")
        print("0 - Voltar")

        opcao = super().le_num_inteiro("Escolha uma opcao: ", range(4))
        return opcao

    def mostra_autor(self, dados_autor: {}):
        if not dados_autor:
            self.mostra_mensagem("Nenhum autor foi cadastrado!")
        else:
            print("NOME:", dados_autor['nome'])
            print("MANGAS:", dados_autor['mangas'] or 'Nenhum vinculado')
            print()

    def recolhe_dados_autor(self) -> str:
        print(f"{'DADOS AUTOR':-^30}")
        nome = super().le_texto("Nome: ")
        return nome

    def seleciona_autor(self) -> str:
        print(f"{'SELECIONA AUTOR':-^30}")
        nome = super().le_texto("Nome: ")
        return nome

    def seleciona_manga(self) -> str:
        print(f"{'SELECIONA MANGA':-^30}")
        titulo = super().le_texto("Titulo: ")
        return titulo
