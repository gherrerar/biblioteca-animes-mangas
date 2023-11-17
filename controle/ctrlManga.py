from controle.abstractCtrl import AbstractCtrl
from limite.telaManga import TelaManga
from entidade.manga import Manga


class CtrlManga(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__mangas = []
        self.__tela_manga = TelaManga()
        super().__init__(ctrl_principal)

    def abrir_tela(self):
        opcoes = {
            1: self.listar_mangas,
            2: self.incluir_manga,
            3: self.editar_manga,
            4: self.remover_manga,
            5: self.abrir_tela_volume,
            6: self.abrir_tela_autor,
            0: self.retornar
        }

        while True:
            opcoes[self.__tela_manga.mostra_opcoes()]()

    def abrir_tela_volume(self):
        opcoes = {
            1: self.listar_volumes_manga,
            2: self.incluir_volume_manga,
            3: self.remover_volume_manga,
            4: self.incluir_capitulos_volume,
            5: self.remover_capitulo_volume,
            0: self.abrir_tela
        }

        while True:
            opcoes[self.__tela_manga.mostra_opcoes_volume()]()

    def abrir_tela_autor(self):
        self.ctrl_principal.ctrl_autor.abrir_tela()

    @property
    def tela_manga(self):
        return self.__tela_manga

    def listar_mangas(self):
        if self.__mangas:
            for manga in self.__mangas:
                self.__tela_manga.mostra_manga({
                    'titulo': manga.titulo,
                    'ano': manga.ano_lancamento,
                    'genero': manga.genero,
                    'autor': manga.autor,
                    'num_volumes': manga.num_volumes,
                    'volumes': manga.volumes
                })
        else:
            self.__tela_manga.mostra_manga(None)

    def incluir_manga(self):
        self.ctrl_principal.ctrl_genero.listar_generos()
        dados_manga = self.__tela_manga.recolhe_dados_manga()
        self.__cria_genero(dados_manga)

        if self.find_manga_by_titulo(dados_manga['titulo']) != None:
            self.__tela_manga.mostra_mensagem("Atencao! Esse manga ja existe!\n")
        else:
            manga = Manga(
                dados_manga['titulo'],
                dados_manga['ano'],
                dados_manga['genero'],
                dados_manga['num_volumes']
            )
            self.__mangas.append(manga)
            self.__tela_manga.mostra_mensagem("Manga cadastrado!\n")

    def editar_manga(self):
        def logica_edicao(manga):
            dados_manga = self.__tela_manga.recolhe_dados_manga()
            self.__cria_genero(dados_manga)

            manga.titulo = dados_manga['titulo']
            manga.ano_lancamento = dados_manga['ano']
            manga.genero = dados_manga['genero']
            manga.num_volumes = dados_manga['num_volumes']
            self.__tela_manga.mostra_mensagem("Manga alterado!\n")
        self.__executa_se_existe_manga(logica_edicao)

    def remover_manga(self):
        def logica_remocao(manga):
            self.__mangas.remove(manga)
            self.__tela_manga.mostra_mensagem("Manga removido!\n")
        self.__executa_se_existe_manga(logica_remocao)

    def listar_volumes_manga(self):
        def logica_lista_volume(manga):
            if manga.volumes:
                for vol in manga.volumes:
                    self.__tela_manga.mostra_volume({
                        'numero': vol.numero,
                        'num_capitulos': vol.num_capitulos,
                        'capitulos': vol.capitulos
                    })
            else:
                self.__tela_manga.mostra_volume({})
        self.__executa_se_existe_manga(logica_lista_volume)

    def incluir_volume_manga(self):
        def logica_inclusao_volume(manga):
            while True:
                dados_volume = self.__tela_manga.recolhe_dados_volume(manga.num_volumes)
                volume = manga.add_volume(
                    dados_volume['numero'],
                    dados_volume['num_capitulos']
                )
                if volume != None:
                    self.__tela_manga.mostra_mensagem("Volume inserido!\n")
                    break
                else:
                    self.__tela_manga.mostra_mensagem("Atencao! Este volume ja existe!\n")
        self.__executa_se_existe_manga(logica_inclusao_volume)

    def remover_volume_manga(self):
        def seleciona_manga(manga):
            def logica_remocao_volume(volume):
                manga.rem_volume(volume.numero)
                self.__tela_manga.mostra_mensagem("Volume removido!\n")
            self.__executa_se_existe_volume_manga(manga, logica_remocao_volume)
        self.__executa_se_existe_manga(seleciona_manga)

    def incluir_capitulos_volume(self):
        def seleciona_manga(manga):
            def logica_inclusao_capitulos(volume):
                for _ in range(abs(len(volume.capitulos)-volume.num_capitulos)):
                    while True:
                        dados_capitulos = self.__tela_manga.recolhe_dados_capitulo(volume.num_capitulos)
                        capitulo = volume.find_capitulo_by_numero(dados_capitulos['numero'])
                        if capitulo != None:
                            self.__tela_manga.mostra_mensagem("Atencao! Este capitulo ja existe!\n")
                        else:
                            manga.add_capitulo_volume(
                                volume.numero,
                                dados_capitulos['numero'],
                                dados_capitulos['num_paginas']
                            )
                            self.__tela_manga.mostra_mensagem("Capitulo inserido!\n")
                            break
            self.__executa_se_existe_volume_manga(manga, logica_inclusao_capitulos)
        self.__executa_se_existe_manga(seleciona_manga)

    def remover_capitulo_volume(self):
        def seleciona_manga(manga):
            def logica_remocao_capitulo(volume):
                if volume.capitulos:
                    while True:
                        numero_cap = self.__tela_manga.seleciona_capitulo(volume.num_capitulos)
                        capitulo = volume.find_capitulo_by_numero(numero_cap)
                        if capitulo != None:
                            manga.rem_capitulo_volume(
                                volume.numero,
                                numero_cap
                            )
                            self.__tela_manga.mostra_mensagem("Capitulo removido!\n")
                            break
                        else:
                            self.__tela_manga.mostra_mensagem("Atencao! Este capitulo nao existe!\n")
                else:
                    self.__tela_manga.mostra_mensagem("Nenhum capitulo foi cadastrado neste volume\n")
            self.__executa_se_existe_volume_manga(manga, logica_remocao_capitulo)
        self.__executa_se_existe_manga(seleciona_manga)

    def __cria_genero(self, dados_manga: {}):
        ctrl_genero = self.ctrl_principal.ctrl_genero
        nome_genero = dados_manga['genero']
        ctrl_genero.incluir_genero(nome_genero)
        dados_manga['genero'] = ctrl_genero.find_genero_by_nome(nome_genero)

    def __executa_se_existe_manga(self, func_crud):
        self.listar_mangas()
        if self.__mangas:
            while True:
                titulo = self.__tela_manga.seleciona_manga()
                manga = self.find_manga_by_titulo(titulo)
                if manga != None:
                    func_crud(manga)
                    break
                else:
                    self.__tela_manga.mostra_mensagem("Atencao! Este manga nao existe!\n")

    def __executa_se_existe_volume_manga(self, manga, func_crud):
        if manga.volumes:
            numero_vol = self.__tela_manga.seleciona_volume(manga.num_volumes)
            volume = manga.find_volume_by_numero(numero_vol)
            if volume != None:
                func_crud(volume)
            else:
                self.__tela_manga.mostra_mensagem("Atenção! Este volume não existe!\n")
        else:
            self.__tela_manga.mostra_mensagem("Nenhum volume foi cadastrado neste manga\n")

    def find_manga_by_titulo(self, titulo: str = '') -> Manga | None:
        if self.__mangas and isinstance(titulo, str):
            for manga in self.__mangas:
                if manga.titulo == titulo:
                    return manga
            return None

    def retornar(self):
        self.ctrl_principal.acessar_usuario_admin()
