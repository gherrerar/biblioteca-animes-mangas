from limite.abstractTela import AbstractTela


class TelaAnime(AbstractTela):
    def __init__(self):
        pass

    def mostra_opcoes(self) -> int:
        print(f"{'ANIMES':-^30}")
        print("1 - Listar")
        print("2 - Cadastrar")
        print("3 - Editar")
        print("4 - Remover")
        print("5 - Temporadas")
        print("6 - Estúdios")
        print("0 - Voltar")

        opcao = super().le_num_inteiro("Escolha uma opcao: ", range(7))
        return opcao

    def mostra_opcoes_temporada(self) -> int:
        print(f"{'TEMPORADAS':-^30}")
        print("1 - Listar")
        print("2 - Cadastrar")
        print("3 - Remover")
        print("4 - Incluir Episódio")
        print("5 - Remover Episódio")
        print("0 - Voltar")

        opcao = super().le_num_inteiro("Escolha uma opcao: ", range(6))
        return opcao

    def mostra_anime(self, dados_anime: {}):
        if not dados_anime:
            self.mostra_mensagem("Nenhum anime foi cadastrado")
        else:
            print(f"{'TITULO:':<15} {dados_anime['titulo']}")
            print(f"{'ANO:':<15} {dados_anime['ano']}")
            print(f"{'GENERO:':<15} {dados_anime['genero'].nome}")
            print(f"{'ESTUDIO:':<15} "
                  "{}".format(
                      dados_anime['estudio'].nome
                      if dados_anime['estudio']
                      else 'Nenhum vinculado')
                )
            print(f"{'TEMPORADAS:':<15} "
                  "{}".format(
                      str(len(dados_anime['temporadas']))
                      +' / '
                      +str(dados_anime['num_temporadas'])
                  )
                )
            print()

    def recolhe_dados_anime(self) -> dict:
        print(f"{'DADOS ANIME':-^30}")
        titulo = super().le_texto("Título: ")
        ano = super().le_num_inteiro("Ano: ", minimo=1000, maximo=2024)
        genero = super().le_texto("Gênero: ")
        num_temporadas = super().le_num_inteiro("Nº Temporadas: ", minimo=1)

        return {'titulo': titulo, 'ano': ano, 'genero': genero, 'num_temporadas': num_temporadas}

    def seleciona_anime(self) -> str:
        print(f"{'SELECIONAR ANIME':-^30}")
        titulo = super().le_texto("Título: ")
        return titulo

    def mostra_temporada(self, dados_temporada: {}):
        if not dados_temporada:
            self.mostra_mensagem("Nenhuma temporada cadastrada neste anime")
        else:
            print(f"{'NUMERO:':<15} {dados_temporada['numero']}")
            print(f"{'Nº EPISODIOS:':<15} {dados_temporada['num_episodios']}")
            print()

    def recolhe_dados_temporada(self, n_temps: int) -> dict:
        print(f"{'DADOS TEMPORADA':-^30}")
        numero = super().le_num_inteiro("Número: ", minimo=1, maximo=n_temps)
        num_episodios = super().le_num_inteiro("Nº Episódios: ", minimo=1)

        return {'numero': numero, 'num_episodios': num_episodios}

    def recolhe_dados_episodio(self, n_eps: int) -> dict:
        print(f"{'DADOS EPISODIO':-^30}")
        numero = super().le_num_inteiro("Número: ", minimo=1, maximo=n_eps)
        duracao = super().le_num_inteiro("Duração (min): ", minimo=5)

        return {'numero': numero, 'duracao': duracao}

    def seleciona_temporada(self, n_temps: int) -> int:
        print(f"{'SELECIONAR TEMPORADA':-^30}")
        numero = super().le_num_inteiro("Número: ", minimo=1, maximo=n_temps)
        return numero

    def seleciona_episodio(self, n_eps: int) -> int:
        print(f"{'SELECIONAR EPISODIO':-^30}")
        numero = super().le_num_inteiro("Número: ", minimo=1, maximo=n_eps)
        return numero
