from controle.abstractCtrl import AbstractCtrl
from limite.telaAutor import TelaAutor
from entidade.autor import Autor
from entidade.dao import DAO


class CtrlAutor(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__autor_dao = DAO('nome', str)
        self.__tela_autor = TelaAutor()
        super().__init__(ctrl_principal)

    def abrir_tela(self):
        opcoes = {
            1: self.listar_autores,
            2: self.incluir_autor,
            3: self.incluir_manga,
            0: self.retornar
        }
    
        while True:
            opcoes[self.__tela_autor.mostra_opcoes()]()

    @property
    def autor_dao(self):
        return self.__autor_dao

    @property
    def __autores(self):
        return self.__autor_dao.get_all()

    def listar_autores(self):
        if self.__autores:
            for autor in self.__autores:
                self.__tela_autor.mostra_autor({
                    'nome': autor.nome,
                    'mangas': ', '.join(manga.titulo for manga in autor.mangas_produzidos)
                })
        else:
            self.__tela_autor.mostra_autor(None)

    def incluir_autor(self):
        nome_autor = self.__tela_autor.recolhe_dados_autor()
        if self.find_autor_by_nome(nome_autor) != None:
            self.__tela_autor.mostra_mensagem("Atencao! Este autor ja existe!\n")
        else:
            autor = Autor(nome_autor)
            self.__autor_dao.add(autor)
            self.__tela_autor.mostra_mensagem("Autor cadastrado!")

    def incluir_manga(self):
        if self.__autores:
            autor = self.__existe_autor()
            manga = self.__existe_manga()
            if manga != None and autor != None:
                if manga in autor.mangas_produzidos:
                    self.__tela_autor.mostra_mensagem("Atencao! Este autor e manga ja estao associados!")
                else:
                    autor.add_manga(manga)
                    self.__tela_autor.mostra_mensagem("Autor e manga associados!")
                self.__autor_dao.add(autor)
                manga_dao = self.ctrl_principal.ctrl_manga.manga_dao
                manga_dao.add(manga)
        else:
            self.__tela_autor.mostra_mensagem("Nenhum autor foi cadastrado!")

    def __existe_autor(self):
        self.listar_autores()
        nome_autor = self.__tela_autor.seleciona_autor()
        autor = self.find_autor_by_nome(nome_autor)
        if autor != None:
            return autor
        else:
            self.__tela_autor.mostra_mensagem("Atencao! Este autor nao existe!\n")
            self.abrir_tela()
    
    def __existe_manga(self):        
        ctrl_manga = self.ctrl_principal.ctrl_manga
        ctrl_manga.listar_mangas()
        titulo_manga = self.__tela_autor.seleciona_manga()
        manga = ctrl_manga.find_manga_by_titulo(titulo_manga)
        if manga != None:
            return manga
        else:
            self.__tela_autor.mostra_mensagem("Atencao! Este manga nao existe!\n")
            self.abrir_tela()

    def find_autor_by_nome(self, nome: str) -> Autor | None:
        if isinstance(nome, str):
            autor = self.__autor_dao.get(nome)
            if autor:
                return autor
            return None

    def retornar(self):
        self.ctrl_principal.ctrl_manga.abrir_tela()
