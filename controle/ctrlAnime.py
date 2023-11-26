from controle.abstractCtrl import AbstractCtrl
from entidade.anime import Anime
from limite.telaAnime import TelaAnime
from entidade.dao import DAO
from exceptions.existenceException import ExistenceException


class CtrlAnime(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__anime_dao = DAO('titulo', str)
        self.__tela_anime = TelaAnime()
        super().__init__(ctrl_principal)

    def abrir_tela(self):
        opcoes = {
            1: self.exibir_anime,
            2: self.incluir_anime,
            3: self.editar_anime,
            4: self.remover_anime,
            5: self.abrir_tela_estudio,
            0: self.retornar
        }

        while True:
            op, self.__selecionado_ani = self.__tela_anime.mostra_opcoes(
                self.__animes, 'anime')
            opcoes[op]()

    def abrir_tela_temporada(self):
        opcoes = {
            1: self.exibir_temporada_anime,
            2: self.incluir_temporada_anime,
            3: self.remover_temporada_anime,
            4: self.abrir_tela_episodio,
            0: self.abrir_tela
        }

        while True:
            op, self.__selecionado_temp = self.__tela_anime.mostra_opcoes(
                self.__selecionado_ani.temporadas if self.__selecionado_ani else [], 'temporada')
            opcoes[op]()

    def abrir_tela_episodio(self):
        if self.__selecionado_temp != None:
            opcoes = {
                1: self.exibir_episodio_temporada,
                2: self.incluir_episodios_temporada,
                3: self.remover_episodio_temporada,
                0: self.abrir_tela_temporada
            }

            while True:
                op, self.__selecionado_ep = self.__tela_anime.mostra_opcoes(
                    self.__selecionado_temp.episodios if self.__selecionado_temp else [], 'episodio')
                opcoes[op]()
        else:
            self.__tela_anime.mostra_mensagem("Nenhuma temporada foi selecionada")

    def abrir_tela_estudio(self):
        self.ctrl_principal.ctrl_estudio.abrir_tela()

    @property
    def anime_dao(self):
        return self.__anime_dao

    @property
    def __animes(self):
        return self.__anime_dao.get_all()

    @property
    def tela_anime(self):
        return self.__tela_anime

    def exibir_anime(self):
        if self.__selecionado_ani:
            self.__tela_anime.mostra_anime({
                'titulo': self.__selecionado_ani.titulo,
                'ano': self.__selecionado_ani.ano_lancamento,
                'genero': self.__selecionado_ani.genero,
                'estudio': self.__selecionado_ani.estudio,
                'num_temporadas': self.__selecionado_ani.num_temporadas,
                'temporadas': self.__selecionado_ani.temporadas
            })
        else:
            self.__tela_anime.mostra_anime(None)

    def incluir_anime(self):
        self.ctrl_principal.ctrl_genero.listar_generos()
        dados_anime = self.__tela_anime.recolhe_dados_anime()
        if dados_anime == 'CANC':
            self.abrir_tela()
        try:
            if self.find_anime_by_titulo(dados_anime['titulo']) != None:
                raise ExistenceException("anime")
            else:
                self.__cria_genero(dados_anime)
                anime = Anime(
                    dados_anime['titulo'],
                    dados_anime['ano'],
                    dados_anime['genero'],
                    dados_anime['num_temporadas']
                )
                self.__anime_dao.add(anime)
                self.__tela_anime.mostra_mensagem("Anime cadastrado!\n")
        except ExistenceException as error:
            self.__tela_anime.mostra_mensagem(f"{error}")

    def editar_anime(self):
        def logica_edicao(anime):
            dados_anime = self.__tela_anime.recolhe_dados_anime(anime)
            if dados_anime == 'CANC':
                self.abrir_tela()
            elif dados_anime == 'TEMP':
                self.abrir_tela_temporada()
            self.__cria_genero(dados_anime)
            
            anime.titulo = dados_anime['titulo']
            anime.ano_lancamento = dados_anime['ano']
            anime.genero = dados_anime['genero']
            anime.num_temporadas = dados_anime['num_temporadas']
            self.__tela_anime.mostra_mensagem("Anime alterado!\n")
        self.__executa_se_existe_anime(logica_edicao)

    def remover_anime(self):
        def logica_remocao(anime):
            estudio = anime.estudio
            if estudio:
                estudio.animes_produzidos.remove(anime)
                estudio_dao = self.ctrl_principal.ctrl_estudio.estudio_dao
                estudio_dao.add(estudio)
            self.__anime_dao.remove(anime.titulo)
            self.__tela_anime.mostra_mensagem("Anime removido!\n")
        self.__executa_se_existe_anime(logica_remocao, True)

    def exibir_temporada_anime(self):
        if self.__selecionado_temp:
            self.__tela_anime.mostra_temporada({
                'numero': self.__selecionado_temp.numero,
                'num_episodios': self.__selecionado_temp.num_episodios,
                'episodios': self.__selecionado_temp.episodios
            })
        else:
            self.__tela_anime.mostra_temporada(None)

    def incluir_temporada_anime(self):
        def logica_inclusao_temporada(anime):
            if abs(len(anime.temporadas)-anime.num_temporadas) != 0:
                while True:
                    try:
                        dados_temporada = self.__tela_anime.recolhe_dados_temporada(anime.num_temporadas)
                        if dados_temporada == 'CANC':
                            self.abrir_tela_temporada()
                        temporada = anime.add_temporada(
                            dados_temporada['numero'],
                            dados_temporada['num_episodios']
                        )
                        if temporada != None:
                            self.__tela_anime.mostra_mensagem("Temporada inserida!\n")
                            break
                        else:
                            raise ExistenceException("temporada")
                    except ExistenceException as error:
                        self.__tela_anime.mostra_mensagem(f"{error}")
            else:
                self.__tela_anime.mostra_mensagem(
                    "Nao ha temporadas para incluir neste anime!\n")
        self.__executa_se_existe_anime(logica_inclusao_temporada)

    def remover_temporada_anime(self):
        def seleciona_anime(anime):
            def logica_remocao_temporada(temporada):
                anime.rem_temporada(temporada.numero)
                self.__tela_anime.mostra_mensagem("Temporada removida!\n")
            self.__executa_se_existe_temporada_anime(anime, logica_remocao_temporada)
        self.__executa_se_existe_anime(seleciona_anime)

    def exibir_episodio_temporada(self):
        if self.__selecionado_ep:
            self.__tela_anime.mostra_episodio({
                'numero': self.__selecionado_ep.numero,
                'duracao': self.__selecionado_ep.duracao
            })
        else:
            self.__tela_anime.mostra_episodio(None)

    def incluir_episodios_temporada(self):
        def seleciona_anime(anime):
            def logica_inclusao_episodios(temporada):
                for _ in range(abs(len(temporada.episodios)-temporada.num_episodios)):
                    while True:
                        try:
                            dados_episodio = self.__tela_anime.recolhe_dados_episodio(temporada.num_episodios)
                            if dados_episodio == 'CANC':
                                self.abrir_tela_episodio()
                            episodio = temporada.find_episodio_by_numero(
                                dados_episodio['numero'])
                            if episodio != None:
                                raise ExistenceException("episodio")
                            else:
                                anime.add_episodio_temporada(
                                    temporada.numero,
                                    dados_episodio['numero'],
                                    dados_episodio['duracao']
                                )
                                self.__tela_anime.mostra_mensagem("Episódio inserido!\n")
                                break
                        except ExistenceException as error:
                            self.__tela_anime.mostra_mensagem(f"{error}")
                self.__tela_anime.mostra_mensagem("Temporada completa!\n")
            self.__executa_se_existe_temporada_anime(anime, logica_inclusao_episodios)
        self.__executa_se_existe_anime(seleciona_anime)

    def remover_episodio_temporada(self):
        def seleciona_anime(anime):
            def logica_remocao_episodio(temporada):
                if temporada.episodios:
                    while True:
                        try:
                            episodio = self.__selecionado_ep
                            if episodio != None:
                                anime.rem_episodio_temporada(
                                    temporada.numero,
                                    episodio.numero
                                )
                                self.__tela_anime.mostra_mensagem("Episódio removido!\n")
                                break
                            else:
                                raise ExistenceException("episodio", False)
                        except ExistenceException as error:
                            self.__tela_anime.mostra_mensagem(f"{error}")
                else:
                    self.__tela_anime.mostra_mensagem("Nenhum episodio foi cadastrado nesta temporada\n")
            self.__executa_se_existe_temporada_anime(anime, logica_remocao_episodio)
        self.__executa_se_existe_anime(seleciona_anime)

    def __cria_genero(self, dados_anime: {}):
        ctrl_genero = self.ctrl_principal.ctrl_genero
        nome_genero = dados_anime['genero']
        ctrl_genero.incluir_genero(nome_genero)
        dados_anime['genero'] = ctrl_genero.find_genero_by_nome(nome_genero)

    def __executa_se_existe_anime(self, func_crud, remove_case = False):
        if self.__animes:
            try:
                anime = self.__selecionado_ani
                if anime != None:
                    func_crud(anime)
                    if not remove_case:
                        self.__anime_dao.add(anime)
                else:
                    raise ExistenceException("anime", False)
            except ExistenceException as error:
                self.__tela_anime.mostra_mensagem(f"{error}")

    def __executa_se_existe_temporada_anime(self, anime, func_crud):
        if anime.temporadas:
            try:
                temporada = self.__selecionado_temp
                if temporada != None:
                    func_crud(temporada)
                else:
                    raise ExistenceException("temporada", False)
            except ExistenceException as error:
                self.__tela_anime.mostra_mensagem(f"{error}")
        else:
            self.__tela_anime.mostra_mensagem("Nenhuma temporada foi cadastrada neste anime\n")

    def find_anime_by_titulo(self, titulo: str) -> Anime | None:
        if isinstance(titulo, str):
            anime = self.__anime_dao.get(titulo)
            if anime:
                return anime
            return None

    def retornar(self):
        self.ctrl_principal.acessar_usuario_admin()
