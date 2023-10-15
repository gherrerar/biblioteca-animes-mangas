from limite.abstractTela import AbstractTela


class TelaExemplarAnime(AbstractTela):
    def __init__(self):
        pass

    def mostra_opcoes(self) -> int:
        print(f"{'EXEMPLARES ANIMES':-^30}")
        print("1 - Listar")
        print("2 - Cadastrar")
        print("0 - Voltar")

        opcao = super().le_num_inteiro("Escolha uma opcao: ", range(3))
        return opcao

    def mostra_exemplar(self, dados_exemplar: {}):
        if not dados_exemplar:
            self.mostra_mensagem("Nenhum exemplar de anime foi cadastrado")
        else:
            print(f"{'ANIME:':<15} {dados_exemplar['anime'].titulo}")
            print(f"{'ESTADO:':<15} {dados_exemplar['etiqueta'].value}")
            print()

    def recolhe_dados_exemplar(self) -> str:
        print(f"{'DADOS EXEMPLAR':-^30}")
        anime = super().le_texto("Título: ")
        return anime
