from limite.abstractTela import AbstractTela


class TelaUsuarioAdministrador(AbstractTela):
    def __init__(self):
        pass

    def mostra_opcoes(self, usuario_logado) -> int:
        print(f"{'USUARIOS ADMIN':-^30}")
        print("1 - Listar")
        print("2 - Cadastrar")
        print("3 - Login")
        if usuario_logado:
            print("4 - Logout")
            print("5 - Animes")
            print("6 - Mangás")
        print("0 - Voltar")

        opcao = super().le_num_inteiro("Escolha uma opcao: ",
                                       range(7 if usuario_logado else 5))
        return opcao

    def mostra_usuario(self, nome_usuario: str):
        if not nome_usuario:
            self.mostra_mensagem("Nenhum usuário administrador foi cadastrado")
        else:
            print(f"{'NOME:':<15} {nome_usuario}")
            print()

    def recolhe_dados_usuario(self) -> dict:
        print(f"{'DADOS USUARIO ADMIN':-^30}")
        nome = super().le_texto("Nome: ")
        senha = super().le_texto("Senha: ")
        
        return {'nome': nome, 'senha': senha}
