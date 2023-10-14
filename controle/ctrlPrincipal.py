from controle.ctrlAnime import CtrlAnime
from controle.ctrlManga import CtrlManga
from controle.ctrlGenero import CtrlGenero
from controle.ctrlEstudio import CtrlEstudio
from controle.ctrlAutor import CtrlAutor
from controle.ctrlUsuarioAdministrador import CtrlUsuarioAdministrador
from controle.ctrlUsuarioComum import CtrlUsuarioComum
from controle.ctrlExemplarAnime import CtrlExemplarAnime
from controle.ctrlExemplarManga import CtrlExemplarManga


class CtrlPrincipal:
    def __init__(self):
        self.__ctrl_anime = CtrlAnime(self)
        self.__ctrl_manga = CtrlManga(self)
        self.__ctrl_genero = CtrlGenero(self)
        self.__ctrl_estudio = CtrlEstudio(self)
        self.__ctrl_autor = CtrlAutor(self)
        self.__ctrl_exemplar_anime = CtrlExemplarAnime(self)
        self.__ctrl_exemplar_manga = CtrlExemplarManga(self)
        self.__ctrl_usuario_admin = CtrlUsuarioAdministrador(self)
        self.__ctrl_usuario_comum = CtrlUsuarioComum(self)

    @property
    def ctrl_anime(self):
        return self.__ctrl_anime

    @property
    def ctrl_manga(self):
        return self.__ctrl_manga

    @property
    def ctrl_genero(self):
        return self.__ctrl_genero
