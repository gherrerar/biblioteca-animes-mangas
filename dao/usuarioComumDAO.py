from dao.dao import DAO
from entidade.usuarioComum import UsuarioComum


class UsuarioComumDAO(DAO):
    def __init__(self):
        super().__init__('usuarioComum.pkl')

    def add(self, usuario: UsuarioComum):
        if isinstance(usuario, UsuarioComum):
            super().add(usuario.nome, usuario)

    def get(self, nome: str):
        if isinstance(nome, str):
            return super().get(nome)

    def remove(self, nome: str):
        if isinstance(nome, str):
            return super().remove(nome)
