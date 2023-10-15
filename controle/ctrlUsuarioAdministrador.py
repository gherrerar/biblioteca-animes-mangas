from controle.abstractCtrl import AbstractCtrl
from entidade.usuarioAdministrador import UsuarioAdministrador
from limite.telaUsuarioAdministrador import TelaUsuarioAdministrador


class CtrlUsuarioAdministrador(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__usuarios_admin = []
        self.__tela_usuario_admin = TelaUsuarioAdministrador()
        super().__init__(ctrl_principal)

    def abrir_tela(self):
        opcoes = {
            1: self.listar_usuarios,
            2: self.incluir_usuario,
            0: self.retornar
        }

        while True:
            if self.__usuarios_admin:
                opcoes[3] = self.abrir_tela_animes
                opcoes[4] = self.abrir_tela_mangas
            opcoes[self.__tela_usuario_admin.mostra_opcoes(self.__usuarios_admin)]()

    def abrir_tela_animes(self):
        self.ctrl_principal.ctrl_anime.abrir_tela()

    def abrir_tela_mangas(self):
        self.ctrl_principal.ctrl_manga.abrir_tela()

    def listar_usuarios(self):
        if self.__usuarios_admin:
            for usuario in self.__usuarios_admin:
                self.__tela_usuario_admin.mostra_usuario(usuario.nome)
        else:
            self.__tela_usuario_admin.mostra_usuario(None)

    def incluir_usuario(self):
        dados_usuario = self.__tela_usuario_admin.recolhe_dados_usuario()
        usuario = self.find_usuario_by_nome(dados_usuario['nome'])
        if usuario != None:
            self.__tela_usuario_admin.mostra_mensagem("Atenção! Este usuário administrador já existe")
        else:
            usuario = UsuarioAdministrador(
                dados_usuario['nome'],
                dados_usuario['senha']
            )
            self.__usuarios_admin.append(usuario)
            self.__tela_usuario_admin.mostra_mensagem("Usuário cadastrado!\n")

    def find_usuario_by_nome(self, nome: str) -> UsuarioAdministrador | None:
        if self.__usuarios_admin and isinstance(nome, str):
            for usuario in self.__usuarios_admin:
                if usuario.nome == nome:
                    return usuario
            return None
