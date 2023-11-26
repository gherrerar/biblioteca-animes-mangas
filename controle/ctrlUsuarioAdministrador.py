from controle.abstractCtrl import AbstractCtrl
from entidade.usuarioAdministrador import UsuarioAdministrador
from limite.telaUsuarioAdministrador import TelaUsuarioAdministrador
from entidade.dao import DAO
from exceptions.existenceException import ExistenceException


class CtrlUsuarioAdministrador(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__usuario_admin_dao = DAO('nome', str)
        self.__usuario_logado = None
        self.__tela_usuario_admin = TelaUsuarioAdministrador()
        super().__init__(ctrl_principal)

    def abrir_tela(self):
        opcoes = {
            1: self.incluir_usuario,
            2: self.login_usuario,
            0: self.retornar
        }

        while True:
            if self.__usuario_logado:
                opcoes[2] = self.logout_usuario
                opcoes[3] = self.abrir_tela_animes
                opcoes[4] = self.abrir_tela_mangas
            else:
                opcoes[2] = self.login_usuario
            opcoes[self.__tela_usuario_admin.mostra_opcoes(
                self.__usuario_logado, self.__usuarios)]()

    def abrir_tela_animes(self):
        self.ctrl_principal.ctrl_anime.abrir_tela()

    def abrir_tela_mangas(self):
        self.ctrl_principal.ctrl_manga.abrir_tela()

    @property
    def __usuarios(self):
        return self.__usuario_admin_dao.get_all()

    def incluir_usuario(self):
        dados_usuario = self.__tela_usuario_admin.recolhe_dados_usuario()
        if dados_usuario:
            usuario = self.find_usuario_by_nome(dados_usuario['nome'])
        else:
            self.abrir_tela()
        try:
            if usuario != None:
                raise ExistenceException("usuario administrador")
            else:
                usuario = UsuarioAdministrador(
                    dados_usuario['nome'],
                    dados_usuario['senha']
                )
                self.__usuario_admin_dao.add(usuario)
                self.__tela_usuario_admin.mostra_mensagem("Usuário cadastrado!\n")
        except ExistenceException as error:
            self.__tela_usuario_admin.mostra_mensagem(f"{error}")

    def login_usuario(self):
        dados_usuario = self.__tela_usuario_admin.recolhe_dados_usuario()
        if dados_usuario:
            usuario = self.find_usuario_by_nome(dados_usuario['nome'])
        else:
            self.abrir_tela()
        try:
            if usuario != None:
                if usuario.senha != dados_usuario['senha']:
                    self.__tela_usuario_admin.mostra_mensagem("Atencao! Senha incorreta!")
                else:
                    self.__usuario_logado = usuario
                    self.__tela_usuario_admin.mostra_mensagem(f"Bem vindo(a), {usuario.nome}!")
            else:
                raise ExistenceException("usuario administrador", False)
        except ExistenceException as error:
            self.__tela_usuario_admin.mostra_mensagem(f"{error}")

    def logout_usuario(self):
        self.__tela_usuario_admin.mostra_mensagem(
            f"Até logo, {self.__usuario_logado.nome}!")
        self.__usuario_logado = None

    def find_usuario_by_nome(self, nome: str) -> UsuarioAdministrador | None:
        if isinstance(nome, str):
            usuario = self.__usuario_admin_dao.get(nome)
            if usuario:
                return usuario
            return None
