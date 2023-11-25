from entidade.usuario import Usuario


class UsuarioAdministrador(Usuario):
    def __init__(self, nome: str, senha: str):
        super().__init__(nome, senha)

    def __repr__(self) -> str:
        return f"{self.nome}"
