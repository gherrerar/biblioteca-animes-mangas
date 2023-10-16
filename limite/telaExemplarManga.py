from limite.abstractTela import AbstractTela


class TelaExemplarManga(AbstractTela):
    def __init__(self):
        pass

    def mostra_opcoes(self) -> int:
        print(f"{'EXEMPLARES MANGAS':-^30}")
        print("1 - Listar")
        print("2 - Cadastrar")
        print("0 - Voltar")

        opcao = super().le_num_inteiro("Escolha uma opcao: ", range(3))
        return opcao

    def mostra_exemplar(self, dados_exemplar: {}):
        if not dados_exemplar:
            self.mostra_mensagem("Nenhum exemplar de manga foi cadastrado")
        else:
            print(f"{'MANGA:':<15} {dados_exemplar['manga'].titulo}")
            print(f"{'ESTADO:':<15} {dados_exemplar['etiqueta'].value}")
            print()

    def mostra_etiqueta_estado(self, valor_etiqueta: str):
        print(valor_etiqueta)
        print()

    def recolhe_dados_exemplar(self) -> str:
        print(f"{'DADOS EXEMPLAR':-^30}")
        manga = super().le_texto("Título: ")
        return manga
