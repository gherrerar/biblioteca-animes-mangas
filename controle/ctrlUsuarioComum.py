from controle.abstractCtrl import AbstractCtrl
from limite.telaUsuarioComum import TelaUsuarioComum
from entidade.usuarioComum import UsuarioComum


class CtrlUsuarioComum(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__usuarios_comum = []
        self.__tela_usuario_comum = TelaUsuarioComum()
        super().__init__(ctrl_principal)

    def abrir_tela(self):
        opcoes = {
            1: self.listar_usuarios_comum,
            2: self.incluir_usuario_comum,
            0: self.retornar
        }

        while True:
            if self.__usuarios_comum:
                opcoes[3] = self.abrir_tela_animes
                opcoes[4] = self.abrir_tela_mangas
            opcoes[self.__tela_usuario_comum.mostra_opcoes(self.__usuarios_comum)]()

    def listar_usuarios_comum(self):
        if self.__usuarios_comum:
            for usuario in self.__usuarios_comum:
                self.__tela_usuario_comum.mostra_usuario({
                    'nome': usuario.nome,
                    'animes': ', '.join(exemplar.anime.titulo for exemplar in usuario.animes),
                    'mangas': ', '.join(exemplar.manga.titulo for exemplar in usuario.mangas)
                })
        else:
            self.__tela_usuario_comum.mostra_usuario(None)

    def incluir_usuario_comum(self):
        dados_usuario= self.__tela_usuario_comum.recolhe_dados_usuario()
        usuario = self.find_usuario_by_nome(dados_usuario['nome'])
        if usuario != None:
            self.__tela_usuario_comum.mostra_mensagem("Atencao! Este usuario comum ja existe!")
        else:
            usuario = UsuarioComum(
                dados_usuario['nome'],
                dados_usuario['senha']
            )
            self.__usuarios_comum.append(usuario)
            self.__tela_usuario_comum.mostra_mensagem("Usuario cadastrado!\n")

    def retornar_usuario_comum(self):
        self.abrir_tela()

    def abrir_tela_animes(self):
        opcoes = {
            1: self.listar_animes,
            2: self.incluir_anime,
            3: self.remover_anime,
            4: self.alterar_etiqueta_anime,
            5: self.calcular_total_horas_assistidas,
            6: self.listar_ultimos_animes,
            7: self.listar_principal_genero_animes,
            0: self.retornar_usuario_comum
        }

        while True:
            opcoes[self.__tela_usuario_comum.mostra_opcoes_anime()]()

    def listar_animes(self):
        usuario = self.__existe_usuario()
        if usuario.animes:
            for exemplar in usuario.animes:
                self.__tela_usuario_comum.mostra_anime({
                    'titulo': exemplar.anime.titulo,
                    'ano': exemplar.anime.ano_lancamento,
                    'genero': exemplar.anime.genero,
                    'estudio': exemplar.anime.estudio,
                    'num_temporadas': exemplar.anime.num_temporadas,
                    'temporadas': exemplar.anime.temporadas,
                    'estado': exemplar.etiqueta.value
                })
        else:
            self.__tela_usuario_comum.mostra_mensagem("Atencao! Nao existem animes vinculados a este usuario!")

    def incluir_anime(self):
        def inner(exemplar, usuario, ctrl):
            self.__tela_usuario_comum.mostra_mensagem("Atencao! Este anime ja esta vinculado a este usuario!")

        def alter_inner(exemplar, usuario, ctrl, anime):
            if exemplar == None:
                ctrl.incluir_exemplar(anime)
                exemplar = ctrl.find_exemplar_by_anime(anime.titulo)
            usuario.add_anime(exemplar)
            self.__tela_usuario_comum.mostra_mensagem("Anime vinculado a este usuario!")
        self.__existe_exemplar_anime(inner, alter_inner)

    def remover_anime(self):
        def inner(exemplar, usuario, ctrl):
            usuario.rem_anime(exemplar)
            self.__tela_usuario_comum.mostra_mensagem("Anime removido deste usuario!")
        self.__existe_exemplar_anime(inner)

    def alterar_etiqueta_anime(self):
        def inner(exemplar, usuario, ctrl):
            ctrl.editar_etiqueta_exemplar(exemplar)
        self.__existe_exemplar_anime(inner)

    def calcular_total_horas_assistidas(self):
        self.__calcular_total_consumo('anime', 'total_horas_assistidas')

    def listar_ultimos_animes(self):
        usuario = self.__existe_usuario()
        ultimos_animes = usuario.ultimos_animes()
        if ultimos_animes:
            for exemplar in ultimos_animes:
                self.__tela_usuario_comum.mostra_anime({
                    'titulo': exemplar.anime.titulo,
                    'ano': exemplar.anime.ano_lancamento,
                    'genero': exemplar.anime.genero,
                    'estudio': exemplar.anime.estudio,
                    'num_temporadas': exemplar.anime.num_temporadas,
                    'temporadas': exemplar.anime.temporadas,
                    'estado': exemplar.etiqueta.value
                })
        else:
            self.__tela_usuario_comum.mostra_mensagem("Atencao! Nao existem animes vinculados a este usuario!")

    def listar_principal_genero_animes(self):
        self.__listar_principal_genero('anime', 'principal_genero_animes')

    def abrir_tela_mangas(self):
        opcoes = {
            1: self.listar_mangas,
            2: self.incluir_manga,
            3: self.remover_manga,
            4: self.alterar_etiqueta_manga,
            5: self.calcular_total_paginas_lidas,
            6: self.listar_ultimos_mangas,
            7: self.listar_principal_genero_mangas,
            0: self.retornar_usuario_comum
        }
    
        while True:
            opcoes[self.__tela_usuario_comum.mostra_opcoes_manga()]()

    def listar_mangas(self):
        usuario = self.__existe_usuario()
        if usuario.mangas:
            for exemplar in usuario.mangas:
                self.__tela_usuario_comum.mostra_manga({
                    'titulo': exemplar.manga.titulo,
                    'ano': exemplar.manga.ano_lancamento,
                    'genero': exemplar.manga.genero,
                    'autor': exemplar.manga.autor,
                    'num_volumes': exemplar.manga.num_volumes,
                    'volumes': exemplar.manga.volumes,
                    'estado': exemplar.etiqueta.value
                })
        else:
            self.__tela_usuario_comum.mostra_mensagem("Atencao! Nao existem mangas vinculados a este usuario!")

    def incluir_manga(self):
        def inner(exemplar, usuario, ctrl):
            self.__tela_usuario_comum.mostra_mensagem("Atencao! Este manga ja esta vinculado a este usuario!")

        def alter_inner(exemplar, usuario, ctrl, manga):
            if exemplar == None:
                ctrl.incluir_exemplar(manga)
                exemplar = ctrl.find_exemplar_by_manga(manga.titulo)
            usuario.add_manga(exemplar)
            self.__tela_usuario_comum.mostra_mensagem("manga vinculado a este usuario!")
        self.__existe_exemplar_manga(inner, alter_inner)

    def remover_manga(self):
        def inner(exemplar, usuario, ctrl):
            usuario.rem_manga(exemplar)
            self.__tela_usuario_comum.mostra_mensagem("Manga removido deste usuario!")
        self.__existe_exemplar_manga(inner)

    def alterar_etiqueta_manga(self):
        def inner(exemplar, usuario, ctrl):
            ctrl.editar_etiqueta_exemplar(exemplar)
        self.__existe_exemplar_manga(inner)

    def calcular_total_paginas_lidas(self):
        self.__calcular_total_consumo('manga', 'total_paginas_lidas')

    def listar_ultimos_mangas(self):
        usuario = self.__existe_usuario()
        ultimos_mangas = usuario.ultimos_mangas()
        if ultimos_mangas:
            for exemplar in ultimos_mangas:
                self.__tela_usuario_comum.mostra_manga({
                    'titulo': exemplar.manga.titulo,
                    'ano': exemplar.manga.ano_lancamento,
                    'genero': exemplar.manga.genero,
                    'autor': exemplar.manga.autor,
                    'num_volumes': exemplar.manga.num_volumes,
                    'volumes': exemplar.manga.volumes,
                    'estado': exemplar.etiqueta.value
                })
        else:
            self.__tela_usuario_comum.mostra_mensagem("Atencao! Nao existem mangas vinculados a este usuario!")

    def listar_principal_genero_mangas(self):
        self.__listar_principal_genero('manga', 'principal_genero_mangas')

    def __calcular_total_consumo(self, obra: str, metodo: str):
        usuario = self.__existe_usuario()
        metodo = getattr(usuario, metodo)
        total_consumo = metodo()
        self.__tela_usuario_comum.mostra_total_consumo(obra, total_consumo)

    def __listar_principal_genero(self, obra: str, metodo: str):
        usuario = self.__existe_usuario()
        metodo = getattr(usuario, metodo)
        principal_genero = metodo()
        if principal_genero != None:
            self.__tela_usuario_comum.mostra_genero(principal_genero)
        else:
            self.__tela_usuario_comum.mostra_mensagem(f"Atencao! Nao existem {obra}s vinculados a este usuario")

    def __existe_usuario(self):
        self.listar_usuarios_comum()
        while True:
            nome = self.__tela_usuario_comum.seleciona_usuario()
            usuario = self.find_usuario_by_nome(nome)
            if usuario != None:
                return usuario
            else:
                self.__tela_usuario_comum.mostra_mensagem("Atencao! Este usuario nao existe!\n")

    def __existe_anime(self):
        ctrl_anime = self.ctrl_principal.ctrl_anime
        ctrl_anime.listar_animes()
        while True:
            titulo_anime = self.__tela_usuario_comum.seleciona_anime()
            anime = ctrl_anime.find_anime_by_titulo(titulo_anime)
            if anime != None:
                return anime
            else:
                self.__tela_usuario_comum.mostra_mensagem("Atencao! Este anime nao existe!\n")

    def __existe_manga(self):
        ctrl_manga = self.ctrl_principal.ctrl_manga
        ctrl_manga.listar_mangas()
        while True:
            titulo_manga = self.__tela_usuario_comum.seleciona_manga()
            manga = ctrl_manga.find_manga_by_titulo(titulo_manga)
            if manga != None:
                return manga
            else:
                self.__tela_usuario_comum.mostra_mensagem("Atencao! Este manga nao existe!\n")

    def __existe_exemplar_anime(self, func, not_func = None):
        usuario = self.__existe_usuario()
        anime = self.__existe_anime()
        ctrl_exemplar_anime = self.ctrl_principal.ctrl_exemplar_anime
        exemplar = ctrl_exemplar_anime.find_exemplar_by_anime(anime.titulo)
        if exemplar in usuario.animes:
            func(exemplar, usuario, ctrl_exemplar_anime)
        else:
            if not not_func:
                self.__tela_usuario_comum.mostra_mensagem("Atencao! Este anime nao esta vinculado a este usuario!")
            else:
                not_func(exemplar, usuario, ctrl_exemplar_anime, anime)

    def __existe_exemplar_manga(self, func, not_func = None):
        usuario = self.__existe_usuario()
        manga = self.__existe_manga()
        ctrl_exemplar_manga = self.ctrl_principal.ctrl_exemplar_manga
        exemplar = ctrl_exemplar_manga.find_exemplar_by_manga(manga.titulo)
        if exemplar in usuario.mangas:
            func(exemplar, usuario, ctrl_exemplar_manga)
        else:
            if not not_func:
                self.__tela_usuario_comum.mostra_mensagem("Atencao! Este manga nao esta vinculado a este usuario!")
            else:
                not_func(exemplar, usuario, ctrl_exemplar_manga, manga)

    def find_usuario_by_nome(self, nome: str) -> UsuarioComum | None:
        if self.__usuarios_comum and isinstance(nome, str):
            for usuario in self.__usuarios_comum:
                if usuario.nome == nome:
                    return usuario
            return None
