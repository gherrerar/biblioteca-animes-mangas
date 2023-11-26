from controle.abstractCtrl import AbstractCtrl
from limite.telaManga import TelaManga
from entidade.manga import Manga
from entidade.dao import DAO
from exceptions.existenceException import ExistenceException


class CtrlManga(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__manga_dao = DAO("titulo", str)
        self.__tela_manga = TelaManga()
        super().__init__(ctrl_principal)

    def abrir_tela(self):
        opcoes = {
            1: self.exibir_manga,
            2: self.incluir_manga,
            3: self.editar_manga,
            4: self.remover_manga,
            5: self.abrir_tela_autor,
            0: self.retornar
        }

        while True:
            op, self.__selecionado_manga = self.__tela_manga.mostra_opcoes(
                self.__mangas, 'manga')
            opcoes[op]()

    def abrir_tela_volume(self):
        opcoes = {
            1: self.exibir_volume_manga,
            2: self.incluir_volume_manga,
            3: self.remover_volume_manga,
            4: self.abrir_tela_capitulo,
            0: self.abrir_tela
        }

        while True:
            op, self.__selecionado_vol = self.__tela_manga.mostra_opcoes(
                self.__selecionado_manga.volumes if self.__selecionado_manga else [], 'volume')
            opcoes[op]()

    def abrir_tela_capitulo(self):
        if self.__selecionado_vol != None:
            opcoes = {
                1: self.exibir_capitulo_volume,
                2: self.incluir_capitulos_volume,
                3: self.remover_capitulo_volume,
                0: self.abrir_tela_volume
            }
            
            while True:
                op, self.__selecionado_cap = self.__tela_manga.mostra_opcoes(
                    self.__selecionado_vol.capitulos if self.__selecionado_vol else [], 'capitulo')
                opcoes[op]()
        else:
            self.__tela_manga.mostra_mensagem("Nenhum volume foi selecionado")

    def abrir_tela_autor(self):
        self.ctrl_principal.ctrl_autor.abrir_tela()

    @property
    def manga_dao(self):
        return self.__manga_dao

    @property
    def __mangas(self):
        return self.__manga_dao.get_all()

    @property
    def tela_manga(self):
        return self.__tela_manga

    def exibir_manga(self):
        if self.__selecionado_manga:
            self.__tela_manga.mostra_manga({
                'titulo': self.__selecionado_manga.titulo,
                'ano': self.__selecionado_manga.ano_lancamento,
                'genero': self.__selecionado_manga.genero,
                'autor': self.__selecionado_manga.autor,
                'num_volumes': self.__selecionado_manga.num_volumes,
                'volumes': self.__selecionado_manga.volumes
            })
        else:
            self.__tela_manga.mostra_manga(None)

    def incluir_manga(self):
        self.ctrl_principal.ctrl_genero.listar_generos()
        dados_manga = self.__tela_manga.recolhe_dados_manga()
        if dados_manga == 'CANC':
            self.abrir_tela()
        try:
            if self.find_manga_by_titulo(dados_manga['titulo']) != None:
                raise ExistenceException("manga")
            else:
                self.__cria_genero(dados_manga)
                manga = Manga(
                    dados_manga['titulo'],
                    dados_manga['ano'],
                    dados_manga['genero'],
                    dados_manga['num_volumes']
                )
                self.__manga_dao.add(manga)
                self.__tela_manga.mostra_mensagem("Manga cadastrado!\n")
        except ExistenceException as error:
            self.__tela_manga.mostra_mensagem(f"{error}")

    def editar_manga(self):
        def logica_edicao(manga):
            dados_manga = self.__tela_manga.recolhe_dados_manga(manga)
            if dados_manga == 'CANC':
                self.abrir_tela()
            elif dados_manga == 'VOL':
                self.abrir_tela_volume()
            self.__cria_genero(dados_manga)

            manga.titulo = dados_manga['titulo']
            manga.ano_lancamento = dados_manga['ano']
            manga.genero = dados_manga['genero']
            manga.num_volumes = dados_manga['num_volumes']
            self.__tela_manga.mostra_mensagem("Manga alterado!\n")
        self.__executa_se_existe_manga(logica_edicao)

    def remover_manga(self):
        def logica_remocao(manga):
            autor = manga.autor
            if autor:
                autor.mangas_produzidos.remove(manga)
                autor_dao = self.ctrl_principal.ctrl_autor.autor_dao
                autor_dao.add(autor)
            self.__manga_dao.remove(manga.titulo)
            self.__tela_manga.mostra_mensagem("Manga removido!\n")
        self.__executa_se_existe_manga(logica_remocao, True)

    def exibir_volume_manga(self):
        if self.__selecionado_vol:
            self.__tela_manga.mostra_volume({
                'numero': self.__selecionado_vol.numero,
                'num_capitulos': self.__selecionado_vol.num_capitulos,
                'capitulos': self.__selecionado_vol.capitulos
            })

    def incluir_volume_manga(self):
        def logica_inclusao_volume(manga):
            if abs(len(manga.volumes) - manga.num_volumes) != 0:
                while True:
                    try:
                        dados_volume = self.__tela_manga.recolhe_dados_volume(manga.num_volumes)
                        if dados_volume == 'CANC':
                            self.abrir_tela_volume()
                        volume = manga.add_volume(
                            dados_volume['numero'],
                            dados_volume['num_capitulos']
                        )
                        if volume != None:
                            self.__tela_manga.mostra_mensagem("Volume inserido!\n")
                            break
                        else:
                            raise ExistenceException("volume")
                    except ExistenceException as error:
                        self.__tela_manga.mostra_mensagem(f"{error}")
            else:
                self.__tela_manga.mostra_mensagem(
                    "Nao ha volumes para incluir neste manga!\n")
        self.__executa_se_existe_manga(logica_inclusao_volume)

    def remover_volume_manga(self):
        def seleciona_manga(manga):
            def logica_remocao_volume(volume):
                manga.rem_volume(volume.numero)
                self.__tela_manga.mostra_mensagem("Volume removido!\n")
            self.__executa_se_existe_volume_manga(manga, logica_remocao_volume)
        self.__executa_se_existe_manga(seleciona_manga)

    def exibir_capitulo_volume(self):
        if self.__selecionado_cap:
            self.__tela_manga.mostra_capitulo({
                'numero': self.__selecionado_cap.numero,
                'num_paginas': self.__selecionado_cap.num_paginas
            })
        else:
            self.__tela_manga.mostra_capitulo(None)

    def incluir_capitulos_volume(self):
        def seleciona_manga(manga):
            def logica_inclusao_capitulos(volume):
                for _ in range(abs(len(volume.capitulos)-volume.num_capitulos)):
                    while True:
                        try:
                            dados_capitulos = self.__tela_manga.recolhe_dados_capitulo(volume.num_capitulos)
                            if dados_capitulos == 'CANC':
                                self.abrir_tela_capitulo()
                            capitulo = volume.find_capitulo_by_numero(
                                dados_capitulos['numero'])
                            if capitulo != None:
                                raise ExistenceException("capitulo")
                            else:
                                manga.add_capitulo_volume(
                                    volume.numero,
                                    dados_capitulos['numero'],
                                    dados_capitulos['num_paginas']
                                )
                                self.__tela_manga.mostra_mensagem("Capitulo inserido!\n")
                                break
                        except ExistenceException as error:
                            self.__tela_manga.mostra_mensagem(f"{error}")
                self.__tela_manga.mostra_mensagem("Volume completo!\n")
            self.__executa_se_existe_volume_manga(manga, logica_inclusao_capitulos)
        self.__executa_se_existe_manga(seleciona_manga)

    def remover_capitulo_volume(self):
        def seleciona_manga(manga):
            def logica_remocao_capitulo(volume):
                if volume.capitulos:
                    while True:
                        try:
                            capitulo = self.__selecionado_cap
                            if capitulo != None:
                                manga.rem_capitulo_volume(
                                    volume.numero,
                                    capitulo.numero
                                )
                                self.__tela_manga.mostra_mensagem("Capitulo removido!\n")
                                break
                            else:
                                raise ExistenceException("capitulo", False)
                        except ExistenceException as error:
                            self.__tela_manga.mostra_mensagem(f"{error}")
                else:
                    self.__tela_manga.mostra_mensagem("Nenhum capitulo foi cadastrado neste volume!\n")
            self.__executa_se_existe_volume_manga(manga, logica_remocao_capitulo)
        self.__executa_se_existe_manga(seleciona_manga)

    def __cria_genero(self, dados_manga: {}):
        ctrl_genero = self.ctrl_principal.ctrl_genero
        nome_genero = dados_manga['genero']
        ctrl_genero.incluir_genero(nome_genero)
        dados_manga['genero'] = ctrl_genero.find_genero_by_nome(nome_genero)

    def __executa_se_existe_manga(self, func_crud, remove_case = False):
        if self.__mangas:
            while True:
                try:
                    manga = self.__selecionado_manga
                    if manga != None:
                        func_crud(manga)
                        if not remove_case:
                            self.__manga_dao.add(manga)
                        break
                    else:
                        raise ExistenceException("manga", False)
                except ExistenceException as error:
                    self.__tela_manga.mostra_mensagem(f"{error}")

    def __executa_se_existe_volume_manga(self, manga, func_crud):
        if manga.volumes:
            try:
                volume = self.__selecionado_vol
                if volume != None:
                    func_crud(volume)
                else:
                    raise ExistenceException("volume", False)
            except ExistenceException as error:
                self.__tela_manga.mostra_mensagem(f"{error}")
        else:
            self.__tela_manga.mostra_mensagem("Nenhum volume foi cadastrado neste manga!\n")

    def find_manga_by_titulo(self, titulo: str) -> Manga | None:
        if isinstance(titulo, str):
            manga = self.__manga_dao.get(titulo)
            if manga:
                return manga
            return None

    def retornar(self):
        self.ctrl_principal.acessar_usuario_admin()
