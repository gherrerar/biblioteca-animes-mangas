from limite.abstractTela import AbstractTela


class TelaUsuarioComum(AbstractTela):
    def __init__(self):
        pass

    def mostra_opcoes(self, usuario_logado) -> int:
        print(f"{'USUARIO COMUM':-^30}")
        print("1 - Listar")
        print("2 - Cadastrar")
        print("3 - Login")
        if usuario_logado:
            print("4 - Logout")
            print("5 - Opcoes Anime")
            print("6 - Opcoes Manga")
        print("0 - Voltar")

        opcao = super().le_num_inteiro("Escolha uma opcao: ", 
                                       range(7 if usuario_logado else 5))
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

    def mostra_etiqueta(self, etiqueta: str):
        print(f"{'ETIQUETA:':<15} {etiqueta}")

    def mostra_valores_etiqueta(self, etiqueta):
        print(">> Valores de etiqueta:")
        for estado in etiqueta:
            print(f"• {estado.value}")

    def mostra_total_consumo(self, obra: str, consumo: str):
        if obra == 'anime':
            print(f"{'TOTAL DE HORAS ASSISTIDAS:':<15} {consumo:.2f}h")
        else:
            print(f"{'TOTAL DE PAGINAS LIDAS:':<15} {consumo} paginas")

    def mostra_genero(self, genero):
        print(f"{'PRINCIPAL GENERO:':<15} {genero.nome}")
