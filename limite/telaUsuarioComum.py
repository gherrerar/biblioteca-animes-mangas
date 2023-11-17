from limite.abstractTela import AbstractTela


class TelaUsuarioComum(AbstractTela):
    def __init__(self):
        pass

    def mostra_opcoes(self, usuarios_comum: []) -> int:
        print(f"{'USUARIO COMUM':-^30}")
        print("1 - Listar")
        print("2 - Cadastrar")
        if usuarios_comum:
            print("3 - Opcoes Anime")
            print("4 - Opcoes Manga")
        print("0 - Voltar")

        opcao = super().le_num_inteiro("Escolha uma opcao: ", range(5 if usuarios_comum else 3))
        return opcao

    def mostra_opcoes_anime(self) -> int:
        print(f"{'USUARIO COMUM - ANIMES':-^30}")
        print("1 - Listar")
        print("2 - Cadastrar")
        print("3 - Remover")
        print("4 - Alterar Estado")
        print("5 - Horas Assistidas")
        print("6 - Listar Ultimos")
        print("7 - Principal Genero")
        print("0 - Voltar")

        opcao = super().le_num_inteiro("Escolha uma opcao: ", range(8))
        return opcao

    def mostra_opcoes_manga(self) -> int:
        print(f"{'USUARIO COMUM - MANGAS':-^30}")
        print("1 - Listar")
        print("2 - Cadastrar")
        print("3 - Remover")
        print("4 - Alterar Estado")
        print("5 - Paginas Lidas")
        print("6 - Listar Ultimos")
        print("7 - Principal Genero")
        print("0 - Voltar")

        opcao = super().le_num_inteiro("Escolha uma opcao: ", range(8))
        return opcao

    def mostra_usuario(self, dados_usuario_comum: {}):
        if not dados_usuario_comum:
            self.mostra_mensagem("Nenhum usuario comum foi cadastrado!")
        else:
            print("NOME:", dados_usuario_comum['nome'])
            print("ANIMES:", dados_usuario_comum['animes'] or 'Nenhum vinculado')
            print("MANGAS:", dados_usuario_comum['mangas'] or 'Nenhum vinculado')
            print()

    def recolhe_dados_usuario(self) -> dict:
        print(f"{'DADOS USUARIO COMUM':-^30}")
        nome = super().le_texto("Nome: ")
        senha = super().le_texto("Senha: ")
        
        return {'nome': nome, 'senha': senha}

    def recolhe_dados_etiqueta(self) -> str:
        print(f"{'DADOS ETIQUETA':-^30}")
        valor_etiqueta = super().le_texto("Estado: ")
        return valor_etiqueta

    def seleciona_usuario(self) -> str:
        print(f"{'SELECIONAR USUARIO':-^30}")
        nome = super().le_texto("Nome: ")
        return nome

    def mostra_anime(self, dados_anime: {}):
        if not dados_anime:
            self.mostra_mensagem("Nenhum exemplar de anime foi cadastrado!")
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
            print(f"{'ETIQUETA:':<15} {dados_anime['estado']}")
            print()

    def mostra_manga(self, dados_manga: {}):
        if not dados_manga:
            self.mostra_mensagem("Nenhum exemplar de manga foi cadastrado!")
        else:
            print(f"{'TITULO:':<15} {dados_manga['titulo']}")
            print(f"{'ANO:':<15} {dados_manga['ano']}")
            print(f"{'GENERO:':<15} {dados_manga['genero'].nome}")
            print(f"{'AUTOR:':<15} "
                  "{}".format(
                      dados_manga['autor'].nome
                      if dados_manga['autor']
                      else 'Nenhum vinculado')
                )
            print(f"{'TEMPORADAS:':<15} "
                  "{}".format(
                      str(len(dados_manga['volumes']))
                      +' / '
                      +str(dados_manga['num_volumes'])
                  )
                )
            print(f"{'ETIQUETA:':<15} {dados_manga['estado']}")
            print()

    def mostra_etiqueta_estado(self, etiqueta):
        print(">> Valores de etiqueta:")
        for estado in etiqueta:
            print(f"• {estado.value}")

    def seleciona_anime(self) -> str:
        print(f"{'SELECIONAR ANIME':-^30}")
        titulo = super().le_texto("Titulo: ")
        return titulo

    def seleciona_manga(self) -> str:
        print(f"{'SELECIONAR MANGA':-^30}")
        titulo = super().le_texto("Titulo: ")
        return titulo

    def mostra_total_consumo(self, obra: str, consumo: str):
        if obra == 'anime':
            print(f"{'TOTAL DE HORAS ASSISTIDAS:':<15} {consumo:.2f}h")
        else:
            print(f"{'TOTAL DE PAGINAS LIDAS:':<15} {consumo} paginas")

    def mostra_genero(self, genero):
        print(f"{'PRINCIPAL GENERO:':<15} {genero.nome}")
