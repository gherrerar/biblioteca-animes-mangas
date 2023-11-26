from controle.abstractCtrl import AbstractCtrl
from limite.telaAutor import TelaAutor
from entidade.autor import Autor
from entidade.dao import DAO
from exceptions.existenceException import ExistenceException


class CtrlAutor(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__autor_dao = DAO('nome', str)
        self.__tela_autor = TelaAutor()
        super().__init__(ctrl_principal)

    def abrir_tela(self):
        opcoes = {
            1: self.exibir_autor,
            2: self.incluir_autor,
            3: self.incluir_manga,
            0: self.retornar
        }
    
        while True:
            op, self.__selecionado_autor = self.__tela_autor.mostra_opcoes(
                self.__autores)
            opcoes[op]()

    @property
    def autor_dao(self):
        return self.__autor_dao

    @property
    def __autores(self):
        return self.__autor_dao.get_all()

    def exibir_autor(self):
        if self.__selecionado_autor:
            self.__tela_autor.mostra_autor({
                'nome': self.__selecionado_autor.nome,
                'mangas': ', '.join(manga.titulo for manga in self.__selecionado_autor.mangas_produzidos)
            })
        else:
            self.__tela_autor.mostra_autor(None)

    def incluir_autor(self):
        filtered_mangas = self.__mangas_sem_autor()
        dados_autor = self.__tela_autor.recolhe_dados_autor(
            filtered_mangas)
        if dados_autor == 'CANC':
            self.abrir_tela()
        try:
            if self.find_autor_by_nome(dados_autor) != None:
                raise ExistenceException("autor")
            else:
                autor = Autor(dados_autor)
                self.__autor_dao.add(autor)
                self.__tela_autor.mostra_mensagem("Autor cadastrado!")
        except ExistenceException as error:
            self.__tela_autor.mostra_mensagem(f"{error}")

    def incluir_manga(self):
        if self.__autores:
            autor = self.__existe_autor()
            filtered_mangas = self.__mangas_sem_autor()
            dados_autor = self.__tela_autor.recolhe_dados_autor(
                filtered_mangas, autor)
            if dados_autor == 'CANC':
                self.abrir_tela()
            
            for manga in dados_autor:
                if manga != None and autor != None:
                    if manga in autor.mangas_produzidos:
                        self.__tela_autor.mostra_mensagem(
                            f"{manga.titulo}:\nAtencao! Este autor e manga ja estao associados!")
                    else:
                        autor.add_manga(manga)
                        self.__tela_autor.mostra_mensagem(
                            f"{manga.titulo}:\nAutor e manga associados!")
                        self.__autor_dao.add(autor)
                        manga_dao = self.ctrl_principal.ctrl_manga.manga_dao
                        manga_dao.add(manga)
        else:
            self.__tela_autor.mostra_mensagem(
                "Nenhum autor foi cadastrado!")

    def __existe_autor(self):
        autor = self.__selecionado_autor
        try:
            if autor != None:
                return autor
            else:
                raise ExistenceException("autor", False)
        except ExistenceException as error:
            self.__tela_autor.mostra_mensagem(f"{error}")
            self.abrir_tela()
    
    def __mangas_sem_autor(self):
        mangas = self.ctrl_principal.ctrl_manga.mangas
        return list(filter(
            lambda x: x.autor == None, mangas))

    def find_autor_by_nome(self, nome: str) -> Autor | None:
        if isinstance(nome, str):
            autor = self.__autor_dao.get(nome)
            if autor:
                return autor
            return None

    def retornar(self):
        self.ctrl_principal.ctrl_manga.abrir_tela()
