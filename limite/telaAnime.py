from limite.abstractTela import AbstractTela
import PySimpleGUI as sg


class TelaAnime(AbstractTela):
    def __init__(self):
        pass

    def mostra_opcoes(self, objs, type: str) -> int:
        methods = {
            'anime': self.init_components,
            'temporada': self.init_components_temporada,
            'episodio': self.init_components_episodio
        }
        methods[type](list(objs))
        event, values = self.open()
        self.close()

        selecionado = values['-LB-']
        return event if event is not None else 0, selecionado[0] if selecionado else None

    def init_components(self, anime_list):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('ANIMES', justification='center', expand_x=True)],
            [sg.Listbox(
                anime_list,
                s=(None, 10),
                background_color='#525255', highlight_background_color='white',
                highlight_text_color='black', sbar_relief=sg.RELIEF_FLAT,
                sbar_background_color='#cbcbcc', font=12,
                expand_x=True, key='-LB-')],
            [sg.B(image_filename="limite/assets/images/read_btn.png",
                  expand_x=True, tooltip='Mostrar', key=1),
             sg.B(image_filename="limite/assets/images/edit_btn.png",
                  expand_x=True, tooltip='Editar', key=3),
             sg.B(image_filename="limite/assets/images/remove_btn.png",
                  expand_x=True, tooltip='Remover', key=4)],

            [sg.B(image_filename="limite/assets/images/add_btn.png",
                  p=(0, 10), expand_x=True, key=2)],
            [sg.T('_'*49, text_color='#525255',
                   justification='center', expand_x=True)],
            [sg.B(image_filename="limite/assets/images/estudio_btn.png",
                  p=(0, 10), expand_x=True, key=5)]
        ], grab_anywhere=True)

    def mostra_anime(self, dados_animes: {}):
        if not dados_animes:
            self.mostra_mensagem("Nenhum anime foi selecionado!")
        else:
            self.__window = sg.Window('Biblioteca de Animes e Mangas', [
                [sg.Col([
                    [sg.T('TITULO:')],
                    [sg.T('ANO:')],
                    [sg.T('GENERO:')],
                    [sg.T('ESTUDIO:')],
                    [sg.T('TEMPORADAS:')]
                ]),
                 sg.Col([
                     [sg.T(dados_animes['titulo'])],
                     [sg.T(dados_animes['ano'])],
                     [sg.T(dados_animes['genero'].nome)],
                     [sg.T(dados_animes['estudio'].nome
                           if dados_animes['estudio']
                         else 'Nenhum vinculado')],
                     [sg.T(str(len(dados_animes['temporadas']))
                           + ' / '
                           + str(dados_animes['num_temporadas']))]
                 ])]
            ], modal=True).Read(close=True)

    def recolhe_dados_anime(self, selecionado = None) -> dict:
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('DADOS ANIME', justification='center', expand_x=True)],
            [sg.Fr("Título", [
                [sg.In(selecionado and selecionado.titulo,
                    key='titulo', p=(5, 10), s=(
                    37, None), font=12, focus=True)]
            ], expand_x=True)],
            [sg.Fr("Ano", [
                [sg.In(selecionado and selecionado.ano_lancamento,
                    key='ano', p=(5, 10), s=(37, None), font=12)]
            ], expand_x=True)],
            [sg.Fr("Gênero", [
                [sg.In(selecionado and selecionado.genero.nome,
                    key='genero', p=(5, 10), s=(37, None), font=12)]
            ], expand_x=True)],
            [sg.Fr("Nº Temporadas", [
                [sg.In(selecionado and selecionado.num_temporadas,
                    key='num_temporadas', p=(5, 10), s=(37, None), font=12)]
            ], expand_x=True)],
            [
                sg.B(image_filename="limite/assets/images/confirm_btn.png",
                     p=(5, 20), key='Confirmar'),
                sg.B(image_filename="limite/assets/images/cancel_btn.png",
                     p=(5, 20), key='Cancelar')
            ],
            (
                [sg.T('_'*49, text_color='#525255',
                      justification='center', expand_x=True)],
                [sg.B(image_filename="limite/assets/images/temporada_btn.png",
                      p=(0, 10), expand_x=True, key='Temporada')]
            ) if selecionado else []
        ], grab_anywhere=True)

        while True:
            event, values = self.open()

            if event == 'Confirmar':
                titulo = super().le_texto("Título", values['titulo'])
                ano = super().le_num_inteiro(
                    "Ano", values['ano'], minimo=1000, maximo=2024)
                genero = super().le_texto("Gênero", values['genero'])
                num_temporadas = super().le_num_inteiro(
                    "Nº Temporadas", values['num_temporadas'], minimo=1)
            elif event == 'Cancelar':
                self.close()
                return 'CANC'
            elif event == 'Temporada':
                self.close()
                return 'TEMP'
            if all([titulo, ano, genero, num_temporadas]):
                break
        self.close()
        return {'titulo': titulo, 'ano': ano, 'genero': genero, 'num_temporadas': num_temporadas}

    def init_components_temporada(self, temporada_list):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('TEMPORADAS ANIME', justification='center', expand_x=True)],
            [sg.Listbox(
                temporada_list,
                s=(None, 10),
                background_color='#525255', highlight_background_color='white',
                highlight_text_color='black', sbar_relief=sg.RELIEF_FLAT,
                sbar_background_color='#cbcbcc', font=12,
                expand_x=True, key='-LB-')],
            [sg.B(image_filename="limite/assets/images/read_btn.png",
                  expand_x=True, tooltip='Mostrar', key=1),
             sg.B(image_filename="limite/assets/images/edit_btn.png",
                  expand_x=True, tooltip='Editar', key=4),
             sg.B(image_filename="limite/assets/images/remove_btn.png",
                  expand_x=True, tooltip='Remover', key=3)],

            [sg.B(image_filename="limite/assets/images/add_btn.png",
                  p=(0, 10), expand_x=True, key=2)]
        ], grab_anywhere=True)

    def mostra_temporada(self, dados_temporada: {}):
        if not dados_temporada:
            self.mostra_mensagem("Nenhuma temporada foi selecionada!")
        else:
            self.__window = sg.Window('Biblioteca de Animes e Mangas', [
                [sg.Col([
                    [sg.T('NUMERO:')],
                    [sg.T('EPISODIOS:')]
                ]),
                    sg.Col([
                        [sg.T(dados_temporada['numero'])],
                        [sg.T(str(len(dados_temporada['episodios']))
                            + ' / '
                            + str(dados_temporada['num_episodios']))]
                    ])]
            ], modal=True).Read(close=True)

    def recolhe_dados_temporada(self, n_temps: int, selecionado = None) -> dict:
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('DADOS TEMPORADA', justification='center', expand_x=True)],
            [sg.Fr("Número", [
                [sg.In(selecionado and selecionado.numero,
                       key='numero', p=(5, 10), s=(
                           37, None), font=12, focus=True)]
            ], expand_x=True)],
            [sg.Fr("Nº Episódios", [
                [sg.In(selecionado and selecionado.num_episodios,
                       key='num_episodios', p=(5, 10), s=(37, None), font=12)]
            ], expand_x=True)],
            [
                sg.B(image_filename="limite/assets/images/confirm_btn.png",
                     p=(5, 20), key='Confirmar'),
                sg.B(image_filename="limite/assets/images/cancel_btn.png",
                     p=(5, 20), key='Cancelar')
            ]
        ], grab_anywhere=True)

        while True:
            event, values = self.open()

            if event == 'Confirmar':
                numero = super().le_num_inteiro(
                    "Número", values['numero'], minimo=1, maximo=n_temps)
                num_episodios = super().le_num_inteiro(
                    "Nº Episódios", values['num_episodios'], minimo=1)
            elif event == 'Cancelar':
                self.close()
                return 'CANC'
            if all([numero, num_episodios]):
                break
        self.close()
        return {'numero': numero, 'num_episodios': num_episodios}

    def init_components_episodio(self, episodio_list):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('EPISODIOS TEMPORADA ANIME', justification='center', expand_x=True)],
            [sg.Listbox(
                episodio_list,
                s=(None, 10),
                background_color='#525255', highlight_background_color='white',
                highlight_text_color='black', sbar_relief=sg.RELIEF_FLAT,
                sbar_background_color='#cbcbcc', font=12,
                expand_x=True, key='-LB-')],
            [sg.B(image_filename="limite/assets/images/read_btn_2.png",
                  expand_x=True, tooltip='Mostrar', key=1),
             sg.B(image_filename="limite/assets/images/remove_btn_3.png",
                  expand_x=True, tooltip='Remover', key=3)],

            [sg.B(image_filename="limite/assets/images/add_btn.png",
                  p=(0, 10), expand_x=True, key=2)]
        ], grab_anywhere=True)

    def mostra_episodio(self, dados_episodio: {}):
        if not dados_episodio:
            self.mostra_mensagem("Nenhum episodio foi selecionado!")
        else:
            self.__window = sg.Window('Biblioteca de Animes e Mangas', [
                [sg.Col([
                    [sg.T('NUMERO:')],
                    [sg.T('DURACAO (min):')]
                ]),
                sg.Col([
                    [sg.T(dados_episodio['numero'])],
                    [sg.T(dados_episodio['duracao'])]
                ])]
            ], modal=True).Read(close=True)

    def recolhe_dados_episodio(self, n_eps: int) -> dict:
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('DADOS EPISODIO', justification='center', expand_x=True)],
            [sg.Fr("Número", [
                [sg.In(key='numero', p=(5, 10), s=(
                           37, None), font=12, focus=True)]
            ], expand_x=True)],
            [sg.Fr("Duração (min)", [
                [sg.In(key='duracao', p=(5, 10), s=(37, None), font=12)]
            ], expand_x=True)],
            [
                sg.B(image_filename="limite/assets/images/confirm_btn.png",
                     p=(5, 20), key='Confirmar'),
                sg.B(image_filename="limite/assets/images/cancel_btn.png",
                     p=(5, 20), key='Cancelar')
            ]
        ], grab_anywhere=True)

        while True:
            event, values = self.open()

            if event == 'Confirmar':
                numero = super().le_num_inteiro(
                    "Número", values['numero'], minimo=1, maximo=n_eps)
                duracao = super().le_num_inteiro(
                    "Duração (min)", values['duracao'], minimo=5)
            elif event == 'Cancelar':
                self.close()
                return 'CANC'
            if all([numero, duracao]):
                break
        self.close()
        return {'numero': numero, 'duracao': duracao}

    def open(self):
        return self.__window.Read()

    def close(self):
        self.__window.Close()
