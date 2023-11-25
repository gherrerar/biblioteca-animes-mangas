from controle.ctrlAnime import CtrlAnime
from controle.ctrlManga import CtrlManga
from controle.ctrlGenero import CtrlGenero
from controle.ctrlEstudio import CtrlEstudio
from controle.ctrlAutor import CtrlAutor
from controle.ctrlUsuarioAdministrador import CtrlUsuarioAdministrador
from controle.ctrlUsuarioComum import CtrlUsuarioComum
from limite.telaPrincipal import TelaPrincipal


class CtrlPrincipal:
    def __init__(self):
        self.__ctrl_anime = CtrlAnime(self)
        self.__ctrl_manga = CtrlManga(self)
        self.__ctrl_genero = CtrlGenero(self)
        self.__ctrl_estudio = CtrlEstudio(self)
        self.__ctrl_autor = CtrlAutor(self)
        self.__ctrl_usuario_admin = CtrlUsuarioAdministrador(self)
        self.__ctrl_usuario_comum = CtrlUsuarioComum(self)
        self.__tela_principal = TelaPrincipal()

    @property
    def ctrl_anime(self):
        return self.__ctrl_anime

    @property
    def ctrl_manga(self):
        return self.__ctrl_manga

    @property
    def ctrl_genero(self):
        return self.__ctrl_genero

    @property
    def ctrl_estudio(self):
        return self.__ctrl_estudio

    @property
    def ctrl_autor(self):
        return self.__ctrl_autor

    def abrir_tela(self):
        opcoes = {
            1: self.acessar_usuario_admin,
            2: self.acessar_usuario_comum,
            0: self.encerrar_sistema
        }

        while True:
            opcoes[self.__tela_principal.mostra_opcoes()]()

    def inicializar_sistema(self):
        self.abrir_tela()

    def acessar_usuario_admin(self):
        self.__ctrl_usuario_admin.abrir_tela()

    def acessar_usuario_comum(self):
        self.__ctrl_usuario_comum.abrir_tela()

    def encerrar_sistema(self):
        exit(0)
