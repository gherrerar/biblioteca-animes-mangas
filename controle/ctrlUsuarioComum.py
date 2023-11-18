from controle.abstractCtrl import AbstractCtrl
from limite.telaUsuarioComum import TelaUsuarioComum
from entidade.usuarioComum import UsuarioComum
from entidade.exemplarAnime import ExemplarAnime
from entidade.exemplarManga import ExemplarManga
from entidade.exemplar import Estado


class CtrlUsuarioComum(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__usuarios_comum = []
        self.__usuario_logado = None
        self.__tela_usuario_comum = TelaUsuarioComum()
        super().__init__(ctrl_principal)

    def abrir_tela(self):
        opcoes = {
            1: self.listar_usuarios_comum,
            2: self.incluir_usuario_comum,
            3: self.login_usuario,
            0: self.retornar
        }

        while True:
            if self.__usuario_logado:
                opcoes[4] = self.logout_usuario
                opcoes[5] = self.abrir_tela_animes
                opcoes[6] = self.abrir_tela_mangas
            opcoes[self.__tela_usuario_comum.mostra_opcoes(
                self.__usuario_logado)]()

    def listar_usuarios_comum(self, logado: UsuarioComum = None):
        if self.__usuarios_comum:
            for usuario in [logado] if logado else self.__usuarios_comum:
                self.__tela_usuario_comum.mostra_usuario({
                    'nome': usuario.nome,
                    'animes': ', '.join(exemplar.anime.titulo for exemplar in usuario.animes),
                    'mangas': ', '.join(exemplar.manga.titulo for exemplar in usuario.mangas)
                })
        else:
            self.__tela_usuario_comum.mostra_usuario(None)

    def incluir_usuario_comum(self):
        dados_usuario = self.__tela_usuario_comum.recolhe_dados_usuario()
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
        usuario = self.__usuario_logado
        if usuario.animes:
            for exemplar in usuario.animes:
                self.__tela_usuario_comum.mostra_etiqueta(exemplar.etiqueta.value)
                self.ctrl_principal.ctrl_anime.tela_anime.mostra_anime({
                    'titulo': exemplar.anime.titulo,
                    'ano': exemplar.anime.ano_lancamento,
                    'genero': exemplar.anime.genero,
                    'estudio': exemplar.anime.estudio,
                    'num_temporadas': exemplar.anime.num_temporadas,
                    'temporadas': exemplar.anime.temporadas,
                })
        else:
            self.__tela_usuario_comum.mostra_mensagem("Atencao! Nao existem animes vinculados a este usuario!")

    def incluir_anime(self):
        def logica_criacao(anime):
            usuario = self.__usuario_logado
            exemplar = ExemplarAnime(anime, Estado.EM_ANDAMENTO)
            usuario.add_anime(exemplar)
            self.__tela_usuario_comum.mostra_mensagem("Anime vinculado a este usuario!\n")
            self.listar_usuarios_comum(usuario)
        self.__executa_se_existe_exemplar_anime(logica_criacao, True)

    def remover_anime(self):
        def logica_remocao(exemplar):
            usuario = self.__usuario_logado
            usuario.rem_anime(exemplar)
            self.__tela_usuario_comum.mostra_mensagem("Anime removido deste usuario!")
            self.listar_usuarios_comum(usuario)
        self.__executa_se_existe_exemplar_anime(logica_remocao)

    def alterar_etiqueta_anime(self):
        def logica_alteracao(exemplar):
            self.__tela_usuario_comum.mostra_valores_etiqueta(Estado)
            valor_etiqueta = self.__tela_usuario_comum.recolhe_dados_etiqueta()
            etiqueta = self.find_etiqueta_by_estado(valor_etiqueta)
            if etiqueta != None:
                exemplar.etiqueta = etiqueta
                self.__tela_usuario_comum.mostra_mensagem("Etiqueta alterada!\n")
            else:
                self.__tela_usuario_comum.mostra_mensagem(
                    "Atenção! Este não é um valor válido para a etiqueta"
                )
        self.__executa_se_existe_exemplar_anime(logica_alteracao)

    def calcular_total_horas_assistidas(self):
        self.__calcular_total_consumo('anime', 'total_horas_assistidas')

    def listar_ultimos_animes(self):
        usuario = self.__usuario_logado
        ultimos_animes = usuario.ultimos_animes()
        if ultimos_animes:
            for exemplar in ultimos_animes:
                self.__tela_usuario_comum.mostra_etiqueta(exemplar.etiqueta.value)
                self.ctrl_principal.ctrl_anime.tela_anime.mostra_anime({
                    'titulo': exemplar.anime.titulo,
                    'ano': exemplar.anime.ano_lancamento,
                    'genero': exemplar.anime.genero,
                    'estudio': exemplar.anime.estudio,
                    'num_temporadas': exemplar.anime.num_temporadas,
                    'temporadas': exemplar.anime.temporadas,
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
        usuario = self.__usuario_logado
        if usuario.mangas:
            for exemplar in usuario.mangas:
                self.__tela_usuario_comum.mostra_etiqueta(exemplar.etiqueta.value)
                self.ctrl_principal.ctrl_manga.tela_manga.mostra_manga({
                    'titulo': exemplar.manga.titulo,
                    'ano': exemplar.manga.ano_lancamento,
                    'genero': exemplar.manga.genero,
                    'autor': exemplar.manga.autor,
                    'num_volumes': exemplar.manga.num_volumes,
                    'volumes': exemplar.manga.volumes,
                })
        else:
            self.__tela_usuario_comum.mostra_mensagem("Atencao! Nao existem mangas vinculados a este usuario!")

    def incluir_manga(self):
        def logica_criacao(manga):
            usuario = self.__usuario_logado
            exemplar = ExemplarManga(manga, Estado.EM_ANDAMENTO)
            usuario.add_manga(exemplar)
            self.__tela_usuario_comum.mostra_mensagem("Manga vinculado a este usuario!\n")
            self.listar_usuarios_comum(usuario)
        self.__executa_se_existe_exemplar_manga(logica_criacao, True)

    def remover_manga(self):
        def logica_remocao(exemplar):
            usuario = self.__usuario_logado
            usuario.rem_manga(exemplar)
            self.__tela_usuario_comum.mostra_mensagem("Manga removido deste usuario!")
            self.listar_usuarios_comum(usuario)
        self.__executa_se_existe_exemplar_manga(logica_remocao)

    def alterar_etiqueta_manga(self):
        def logica_alteracao(exemplar):
            self.__tela_usuario_comum.mostra_valores_etiqueta(Estado)
            valor_etiqueta = self.__tela_usuario_comum.recolhe_dados_etiqueta()
            etiqueta = self.find_etiqueta_by_estado(valor_etiqueta)
            if etiqueta != None:
                exemplar.etiqueta = etiqueta
                self.__tela_usuario_comum.mostra_mensagem("Etiqueta alterada!\n")
            else:
                self.__tela_usuario_comum.mostra_mensagem(
                    "Atenção! Este não é um valor válido para a etiqueta"
                )
        self.__executa_se_existe_exemplar_manga(logica_alteracao)

    def calcular_total_paginas_lidas(self):
        self.__calcular_total_consumo('manga', 'total_paginas_lidas')

    def listar_ultimos_mangas(self):
        usuario = self.__usuario_logado
        ultimos_mangas = usuario.ultimos_mangas()
        if ultimos_mangas:
            for exemplar in ultimos_mangas:
                self.__tela_usuario_comum.mostra_etiqueta(exemplar.etiqueta.value)
                self.ctrl_principal.ctrl_manga.tela_manga.mostra_manga({
                    'titulo': exemplar.manga.titulo,
                    'ano': exemplar.manga.ano_lancamento,
                    'genero': exemplar.manga.genero,
                    'autor': exemplar.manga.autor,
                    'num_volumes': exemplar.manga.num_volumes,
                    'volumes': exemplar.manga.volumes,
                })
        else:
            self.__tela_usuario_comum.mostra_mensagem("Atencao! Nao existem mangas vinculados a este usuario!")

    def listar_principal_genero_mangas(self):
        self.__listar_principal_genero('manga', 'principal_genero_mangas')

    def login_usuario(self):
        dados_usuario = self.__tela_usuario_comum.recolhe_dados_usuario()
        usuario = self.find_usuario_by_nome(dados_usuario['nome'])
        if usuario != None:
            if usuario.senha != dados_usuario['senha']:
                self.__tela_usuario_comum.mostra_mensagem("Atencao! Senha incorreta!")
            else:
                self.__usuario_logado = usuario
                self.__tela_usuario_comum.mostra_mensagem(f"Bem vindo(a), {usuario.nome}!")
        else:
            self.__tela_usuario_comum.mostra_mensagem(
                "Atencao! Este usuario comum nao existe")

    def logout_usuario(self):
        self.__tela_usuario_comum.mostra_mensagem(
            f"Até logo, {self.__usuario_logado.nome}!")
        self.__usuario_logado = None

    def __calcular_total_consumo(self, obra: str, metodo: str):
        usuario = self.__usuario_logado
        metodo = getattr(usuario, metodo)
        total_consumo = metodo()
        self.__tela_usuario_comum.mostra_total_consumo(obra, total_consumo)

    def __listar_principal_genero(self, obra: str, metodo: str):
        usuario = self.__usuario_logado
        metodo = getattr(usuario, metodo)
        principal_genero = metodo()
        if principal_genero != None:
            self.__tela_usuario_comum.mostra_genero(principal_genero)
        else:
            self.__tela_usuario_comum.mostra_mensagem(f"Atencao! Nao existem {obra}s vinculados a este usuario")

    def __existe_anime(self):
        ctrl_anime = self.ctrl_principal.ctrl_anime
        ctrl_anime.listar_animes()
        titulo_anime = ctrl_anime.tela_anime.seleciona_anime()
        anime = ctrl_anime.find_anime_by_titulo(titulo_anime)
        if anime != None:
            return anime
        else:
            self.__tela_usuario_comum.mostra_mensagem("Atencao! Este anime nao existe!\n")
            self.abrir_tela_animes()

    def __existe_manga(self):
        ctrl_manga = self.ctrl_principal.ctrl_manga
        ctrl_manga.listar_mangas()
        titulo_manga = ctrl_manga.tela_manga.seleciona_manga()
        manga = ctrl_manga.find_manga_by_titulo(titulo_manga)
        if manga != None:
            return manga
        else:
            self.__tela_usuario_comum.mostra_mensagem("Atencao! Este manga nao existe!\n")
            self.abrir_tela_mangas()

    def __executa_se_existe_exemplar_anime(self, func_crud, create_case = False):
        usuario = self.__usuario_logado
        anime = self.__existe_anime()
        if anime is not None and usuario is not None:
            exemplar = self.find_exemplar_by_anime(anime.titulo, usuario)
            if exemplar is not None:
                if create_case:
                    self.__tela_usuario_comum.mostra_mensagem("Atencao! Este anime ja esta vinculado a este usuario!")
                else:
                    func_crud(exemplar)
            else:
                if not create_case:
                    self.__tela_usuario_comum.mostra_mensagem("Atencao! Este anime nao esta vinculado a este usuario!")
                else:
                    func_crud(anime)

    def __executa_se_existe_exemplar_manga(self, func_crud, create_case = False):
        usuario = self.__usuario_logado
        manga = self.__existe_manga()
        if manga is not None and usuario is not None:
            exemplar = self.find_exemplar_by_manga(manga.titulo, usuario)
            if exemplar is not None:
                if create_case:
                    self.__tela_usuario_comum.mostra_mensagem("Atencao! Este manga ja esta vinculado a este usuario!")
                else:
                    func_crud(exemplar)
            else:
                if not create_case:
                    self.__tela_usuario_comum.mostra_mensagem("Atencao! Este manga nao esta vinculado a este usuario!")
                else:
                    func_crud(manga)

    def find_usuario_by_nome(self, nome: str) -> UsuarioComum | None:
        if self.__usuarios_comum and isinstance(nome, str):
            for usuario in self.__usuarios_comum:
                if usuario.nome == nome:
                    return usuario
            return None

    def find_exemplar_by_anime(self, titulo_anime: str, usuario: UsuarioComum) -> ExemplarAnime | None:
        if usuario.animes and isinstance(titulo_anime, str):
            for exemplar in usuario.animes:
                if exemplar.anime.titulo == titulo_anime:
                    return exemplar
            return None

    def find_exemplar_by_manga(self, titulo_manga: str, usuario: UsuarioComum) -> ExemplarManga | None:
        if usuario.mangas and isinstance(titulo_manga, str):
            for exemplar in usuario.mangas:
                if exemplar.manga.titulo == titulo_manga:
                    return exemplar
            return None

    def find_etiqueta_by_estado(self, valor_etiqueta: str) -> Estado | None:
        if isinstance(valor_etiqueta, str):
            for estado in Estado:
                if estado.value == valor_etiqueta:
                    return estado
            return None
