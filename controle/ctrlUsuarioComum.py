from controle.abstractCtrl import AbstractCtrl
from limite.telaUsuarioComum import TelaUsuarioComum
from entidade.usuarioComum import UsuarioComum
from entidade.exemplarAnime import ExemplarAnime
from entidade.exemplarManga import ExemplarManga
from entidade.exemplar import Estado
from entidade.dao import DAO
from exceptions.existenceException import ExistenceException


class CtrlUsuarioComum(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__usuario_comum_dao = DAO('nome', str)
        self.__usuario_logado = None
        self.__tela_usuario_comum = TelaUsuarioComum()
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
            op, self.__selecionado_usuario = self.__tela_usuario_comum.mostra_opcoes(
                self.__usuario_logado, self.__usuarios, 'usuario')
            opcoes[op]()

    @property
    def __usuarios(self):
        return self.__usuario_comum_dao.get_all()

    def incluir_usuario(self):
        dados_usuario = self.__tela_usuario_comum.recolhe_dados_usuario()
        if dados_usuario:
            usuario = self.find_usuario_by_nome(dados_usuario['nome'])
        else:
            self.abrir_tela()
        try:
            if usuario != None:
                raise ExistenceException("usuario commum")
            else:
                usuario = UsuarioComum(
                    dados_usuario['nome'],
                    dados_usuario['senha']
                )
                self.__usuario_comum_dao.add(usuario)
                self.__tela_usuario_comum.mostra_mensagem("Usuário cadastrado!\n")
        except ExistenceException as error:
            self.__tela_usuario_comum.mostra_mensagem(f"{error}")

    def login_usuario(self):
        dados_usuario = self.__tela_usuario_comum.recolhe_dados_usuario()
        if dados_usuario:
            usuario = self.find_usuario_by_nome(dados_usuario['nome'])
        else:
            self.abrir_tela()
        try:
            if usuario != None:
                if usuario.senha != dados_usuario['senha']:
                    self.__tela_usuario_comum.mostra_mensagem("Atencao! Senha incorreta!")
                else:
                    self.__usuario_logado = usuario
                    self.__tela_usuario_comum.mostra_mensagem(f"Bem vindo(a), {usuario.nome}!")
            else:
                raise ExistenceException("usuario comum", False)
        except ExistenceException as error:
            self.__tela_usuario_comum.mostra_mensagem(f"{error}")

    def logout_usuario(self):
        self.__tela_usuario_comum.mostra_mensagem(
            f"Até logo, {self.__usuario_logado.nome}!")
        self.__usuario_logado = None

    def abrir_tela_animes(self):
        opcoes = {
            1: self.exibir_anime,
            2: self.incluir_anime,
            3: self.editar_anime,
            4: self.remover_anime,
            5: self.calcular_total_horas_assistidas,
            6: self.listar_ultimos_animes,
            7: self.listar_principal_genero_animes,
            0: self.abrir_tela
        }

        while True:
            op, self.__selecionado_ani = self.__tela_usuario_comum.mostra_opcoes(
                self.__usuario_logado, self.__usuario_logado.animes, 'anime')
            opcoes[op]()

    def exibir_anime(self):
        if self.__selecionado_ani:
            self.__tela_usuario_comum.mostra_exemplar_anime({
                'etiqueta': self.__selecionado_ani.etiqueta,
                'titulo': self.__selecionado_ani.anime.titulo,
                'ano': self.__selecionado_ani.anime.ano_lancamento,
                'genero': self.__selecionado_ani.anime.genero,
                'estudio': self.__selecionado_ani.anime.estudio,
                'num_temporadas': self.__selecionado_ani.anime.num_temporadas,
                'temporadas': self.__selecionado_ani.anime.temporadas
            })
        else:
            self.__tela_usuario_comum.mostra_exemplar_anime(None)

    def incluir_anime(self):
        def logica_criacao():
            usuario = self.__usuario_logado
            animes = self.ctrl_principal.ctrl_anime.animes
            anime = self.__tela_usuario_comum.recolhe_dados_exemplar_anime(list(animes))
            if anime == "CANC":
                self.abrir_tela_animes()
            exemplar = self.find_exemplar_by_anime(anime.titulo, usuario)
            if exemplar is not None:
                self.__tela_usuario_comum.mostra_mensagem("Atencao! Este anime ja esta vinculado a este usuario!")
            else:
                exemplar = ExemplarAnime(anime, Estado.EM_ANDAMENTO)
                usuario.add_anime(exemplar)
                self.__tela_usuario_comum.mostra_mensagem(f"{anime.titulo}:\nAnime vinculado a este usuario!")
        self.__executa_se_existe_exemplar_anime(logica_criacao, True)

    def editar_anime(self):
        def logica_alteracao(exemplar):
            animes = self.ctrl_principal.ctrl_anime.animes
            valor_etiqueta = self.__tela_usuario_comum.recolhe_dados_exemplar_anime(animes, [e.value for e in Estado], self.__selecionado_ani)
            if valor_etiqueta == "CANC":
                self.abrir_tela_animes()
            etiqueta = self.find_etiqueta_by_estado(valor_etiqueta)
            if etiqueta != None:
                exemplar.etiqueta = etiqueta
                self.__tela_usuario_comum.mostra_mensagem(f"{exemplar.anime.titulo}:\nEtiqueta alterada!\n")
            else:
                self.__tela_usuario_comum.mostra_mensagem(
                    "Atenção! Este não é um valor válido para a etiqueta"
                )
        self.__executa_se_existe_exemplar_anime(logica_alteracao)

    def remover_anime(self):
        def logica_remocao(exemplar):
            usuario = self.__usuario_logado
            usuario.rem_anime(exemplar)
            self.__tela_usuario_comum.mostra_mensagem(f"{exemplar.anime.titulo}:\nAnime removido deste usuario!")
        self.__executa_se_existe_exemplar_anime(logica_remocao)

    def calcular_total_horas_assistidas(self):
        self.__calcular_total_consumo('anime', 'total_horas_assistidas')

    def listar_ultimos_animes(self):
        usuario = self.__usuario_logado
        ultimos_animes = usuario.ultimos_animes()
        if ultimos_animes:
            for exemplar in ultimos_animes:
                self.__tela_usuario_comum.mostra_exemplar_anime({
                    'etiqueta': exemplar.etiqueta,
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
            1: self.exibir_manga,
            2: self.incluir_manga,
            3: self.editar_manga,
            4: self.remover_manga,
            5: self.calcular_total_paginas_lidas,
            6: self.listar_ultimos_mangas,
            7: self.listar_principal_genero_mangas,
            0: self.abrir_tela
        }

        while True:
            op, self.__selecionado_manga = self.__tela_usuario_comum.mostra_opcoes(
                self.__usuario_logado, self.__usuario_logado.mangas, 'manga')
            opcoes[op]()

    def exibir_manga(self):
        if self.__selecionado_manga:
            self.__tela_usuario_comum.mostra_exemplar_manga({
                'etiqueta': self.__selecionado_manga.etiqueta,
                'titulo': self.__selecionado_manga.manga.titulo,
                'ano': self.__selecionado_manga.manga.ano_lancamento,
                'genero': self.__selecionado_manga.manga.genero,
                'autor': self.__selecionado_manga.manga.autor,
                'num_volumes': self.__selecionado_manga.manga.num_volumes,
                'volumes': self.__selecionado_manga.manga.volumes
            })
        else:
            self.__tela_usuario_comum.mostra_exemplar_manga(None)

    def incluir_manga(self):
        def logica_criacao():
            usuario = self.__usuario_logado
            mangas = self.ctrl_principal.ctrl_manga.mangas
            manga = self.__tela_usuario_comum.recolhe_dados_exemplar_manga(list(mangas))
            if manga == "CANC":
                self.abrir_tela_mangas()
            exemplar = self.find_exemplar_by_manga(manga.titulo, usuario)
            if exemplar is not None:
                self.__tela_usuario_comum.mostra_mensagem("Atencao! Este manga ja esta vinculado a este usuario!")
            else:
                exemplar = ExemplarManga(manga, Estado.EM_ANDAMENTO)
                usuario.add_manga(exemplar)
                self.__tela_usuario_comum.mostra_mensagem(f"{manga.titulo}:\nManga vinculado a este usuario!")
        self.__executa_se_existe_exemplar_manga(logica_criacao, True)

    def editar_manga(self):
        def logica_alteracao(exemplar):
            mangas = self.ctrl_principal.ctrl_manga.mangas
            valor_etiqueta = self.__tela_usuario_comum.recolhe_dados_exemplar_manga(mangas, [e.value for e in Estado], self.__selecionado_manga)
            if valor_etiqueta == "CANC":
                self.abrir_tela_mangas()
            etiqueta = self.find_etiqueta_by_estado(valor_etiqueta)
            if etiqueta != None:
                exemplar.etiqueta = etiqueta
                self.__tela_usuario_comum.mostra_mensagem(f"{exemplar.manga.titulo}:\nEtiqueta alterada!\n")
            else:
                self.__tela_usuario_comum.mostra_mensagem(
                    "Atenção! Este não é um valor válido para a etiqueta"
                )
        self.__executa_se_existe_exemplar_manga(logica_alteracao)

    def remover_manga(self):
        def logica_remocao(exemplar):
            usuario = self.__usuario_logado
            usuario.rem_manga(exemplar)
            self.__tela_usuario_comum.mostra_mensagem(f"{exemplar.manga.titulo}:\nManga removido deste usuario!")
        self.__executa_se_existe_exemplar_manga(logica_remocao)

    def calcular_total_paginas_lidas(self):
        self.__calcular_total_consumo('manga', 'total_paginas_lidas')

    def listar_ultimos_mangas(self):
        usuario = self.__usuario_logado
        ultimos_mangas = usuario.ultimos_mangas()
        if ultimos_mangas:
            for exemplar in ultimos_mangas:
                self.__tela_usuario_comum.mostra_exemplar_manga({
                    'etiqueta': exemplar.etiqueta,
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

    def __executa_se_existe_exemplar_anime(self, func_crud, create_case = False):
        usuario = self.__usuario_logado
        exemplar = self.__selecionado_ani
        if exemplar is not None:
            if create_case:
                self.__tela_usuario_comum.mostra_mensagem("Atencao! Este anime ja esta vinculado a este usuario!")
            else:
                func_crud(exemplar)
                self.__usuario_comum_dao.add(usuario)
        else:
            if not create_case:
                self.__tela_usuario_comum.mostra_mensagem("Atencao! Nenhum exemplar foi selecionado!")
            else:
                func_crud()
                self.__usuario_comum_dao.add(usuario)

    def __executa_se_existe_exemplar_manga(self, func_crud, create_case = False):
        usuario = self.__usuario_logado
        exemplar = self.__selecionado_manga
        if exemplar is not None:
            if create_case:
                self.__tela_usuario_comum.mostra_mensagem("Atencao! Este manga ja esta vinculado a este usuario!")
            else:
                func_crud(exemplar)
                self.__usuario_comum_dao.add(usuario)
        else:
            if not create_case:
                self.__tela_usuario_comum.mostra_mensagem("Atencao! Nenhum exemplar foi selecionado!")
            else:
                func_crud()
                self.__usuario_comum_dao.add(usuario)

    def find_usuario_by_nome(self, nome: str) -> UsuarioComum | None:
        if isinstance(nome, str):
            usuario = self.__usuario_comum_dao.get(nome)
            if usuario:
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
