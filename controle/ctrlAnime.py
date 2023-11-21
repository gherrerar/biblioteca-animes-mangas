from controle.abstractCtrl import AbstractCtrl
from entidade.anime import Anime
from limite.telaAnime import TelaAnime
from dao.animeDAO import AnimeDAO


class CtrlAnime(AbstractCtrl):
    def __init__(self, ctrl_principal):
        self.__anime_dao = AnimeDAO()
        self.__tela_anime = TelaAnime()
        super().__init__(ctrl_principal)

    def abrir_tela(self):
        opcoes = {
            1: self.listar_animes,
            2: self.incluir_anime,
            3: self.editar_anime,
            4: self.remover_anime,
            5: self.abrir_tela_temporada,
            6: self.abrir_tela_estudio,
            0: self.retornar
        }

        while True:
            opcoes[self.__tela_anime.mostra_opcoes()]()

    def abrir_tela_temporada(self):
        opcoes = {
            1: self.listar_temporadas_anime,
            2: self.incluir_temporada_anime,
            3: self.remover_temporada_anime,
            4: self.incluir_episodios_temporada,
            5: self.remover_episodio_temporada,
            0: self.abrir_tela
        }

        while True:
            opcoes[self.__tela_anime.mostra_opcoes_temporada()]()

    def abrir_tela_estudio(self):
        self.ctrl_principal.ctrl_estudio.abrir_tela()

    @property
    def __animes(self):
        return self.__anime_dao.get_all()

    @property
    def tela_anime(self):
        return self.__tela_anime

    def listar_animes(self):
        if self.__animes:
            for ani in self.__animes:
                self.__tela_anime.mostra_anime({
                    'titulo': ani.titulo,
                    'ano': ani.ano_lancamento,
                    'genero': ani.genero,
                    'estudio': ani.estudio,
                    'num_temporadas': ani.num_temporadas,
                    'temporadas': ani.temporadas
                })
        else:
            self.__tela_anime.mostra_anime(None)

    def incluir_anime(self):
        self.ctrl_principal.ctrl_genero.listar_generos()
        dados_anime = self.__tela_anime.recolhe_dados_anime()
        self.__cria_genero(dados_anime)

        if self.find_anime_by_titulo(dados_anime['titulo']) != None:
            self.__tela_anime.mostra_mensagem("Atenção! Este anime já existe!\n")
        else:
            anime = Anime(
                dados_anime['titulo'],
                dados_anime['ano'],
                dados_anime['genero'],
                dados_anime['num_temporadas']
            )
            self.__anime_dao.add(anime)
            self.__tela_anime.mostra_mensagem("Anime cadastrado!\n")

    def editar_anime(self):
        def logica_edicao(anime):
            dados_anime = self.__tela_anime.recolhe_dados_anime()
            self.__cria_genero(dados_anime)
            
            anime.titulo = dados_anime['titulo']
            anime.ano_lancamento = dados_anime['ano']
            anime.genero = dados_anime['genero']
            anime.num_temporadas = dados_anime['num_temporadas']
            self.__tela_anime.mostra_mensagem("Anime alterado!\n")
        self.__executa_se_existe_anime(logica_edicao)

    def remover_anime(self):
        def logica_remocao(anime):
            self.__anime_dao.remove(anime.titulo)
            self.__tela_anime.mostra_mensagem("Anime removido!\n")
        self.__executa_se_existe_anime(logica_remocao, True)

    def listar_temporadas_anime(self):
        def logica_lista_temporada(anime):
            if anime.temporadas:
                for temp in anime.temporadas:
                    self.__tela_anime.mostra_temporada({
                        'numero': temp.numero,
                        'num_episodios': temp.num_episodios,
                        'episodios': temp.episodios
                    })
            else:
                self.__tela_anime.mostra_temporada({})
        self.__executa_se_existe_anime(logica_lista_temporada)

    def incluir_temporada_anime(self):
        def logica_inclusao_temporada(anime):
            while True:
                dados_temporada = self.__tela_anime.recolhe_dados_temporada(anime.num_temporadas)
                temporada = anime.add_temporada(
                    dados_temporada['numero'],
                    dados_temporada['num_episodios']
                )
                if temporada != None:
                    self.__tela_anime.mostra_mensagem("Temporada inserida!\n")
                    break
                else:
                    self.__tela_anime.mostra_mensagem("Atenção! Esta temporada já existe\n")
        self.__executa_se_existe_anime(logica_inclusao_temporada)

    def remover_temporada_anime(self):
        def seleciona_anime(anime):
            def logica_remocao_temporada(temporada):
                anime.rem_temporada(temporada.numero)
                self.__tela_anime.mostra_mensagem("Temporada removida!\n")
            self.__executa_se_existe_temporada_anime(anime, logica_remocao_temporada)
        self.__executa_se_existe_anime(seleciona_anime)

    def incluir_episodios_temporada(self):
        def seleciona_anime(anime):
            def logica_inclusao_episodios(temporada):
                for _ in range(abs(len(temporada.episodios)-temporada.num_episodios)):
                    while True:
                        dados_episodios = self.__tela_anime.recolhe_dados_episodio(temporada.num_episodios)
                        episodio = temporada.find_episodio_by_numero(dados_episodios['numero'])
                        if episodio != None:
                            self.__tela_anime.mostra_mensagem("Atenção! Este episódio já existe\n")
                        else:
                            anime.add_episodio_temporada(
                                temporada.numero,
                                dados_episodios['numero'],
                                dados_episodios['duracao']
                            )
                            self.__tela_anime.mostra_mensagem("Episódio inserido!\n")
                            break
                self.__tela_anime.mostra_mensagem("Temporada completa!\n")
            self.__executa_se_existe_temporada_anime(anime, logica_inclusao_episodios)
        self.__executa_se_existe_anime(seleciona_anime)

    def remover_episodio_temporada(self):
        def seleciona_anime(anime):
            def logica_remocao_episodio(temporada):
                if temporada.episodios:
                    while True:
                        numero_ep = self.__tela_anime.seleciona_episodio(temporada.num_episodios)
                        episodio = temporada.find_episodio_by_numero(numero_ep)
                        if episodio != None:
                            anime.rem_episodio_temporada(
                                temporada.numero,
                                numero_ep
                            )
                            self.__tela_anime.mostra_mensagem("Episódio removido!\n")
                            break
                        else:
                            self.__tela_anime.mostra_mensagem("Atenção! Este episódio não existe\n")
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
        self.listar_animes()
        if self.__animes:
            while True:
                titulo = self.__tela_anime.seleciona_anime()
                anime = self.find_anime_by_titulo(titulo)
                if anime != None:
                    func_crud(anime)
                    if not remove_case:
                        self.__anime_dao.add(anime)
                    break
                else:
                    self.__tela_anime.mostra_mensagem("Atenção! Este anime não existe\n")

    def __executa_se_existe_temporada_anime(self, anime, func_crud):
        if anime.temporadas:
            numero_temp = self.__tela_anime.seleciona_temporada(anime.num_temporadas)
            temporada = anime.find_temporada_by_numero(numero_temp)
            if temporada != None:
                func_crud(temporada)
            else:
                self.__tela_anime.mostra_mensagem("Atenção! Esta temporada não existe\n")
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
