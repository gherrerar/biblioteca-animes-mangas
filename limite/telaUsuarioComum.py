from limite.abstractTela import AbstractTela
import PySimpleGUI as sg


class TelaUsuarioComum(AbstractTela):
    def __init__(self):
        pass

    def mostra_opcoes(self, usuario_logado, objs, type: str) -> int:
        methods = {
            'usuario': self.init_components,
            'anime': self.init_components_anime,
            'manga': self.init_components_manga
        }
        methods[type](usuario_logado, list(objs))
        event, values = self.open()
        self.close()

        selecionado = values['-LB-']
        return event if event is not None else 0, selecionado[0] if selecionado else None

    def init_components(self, usuario_logado, usuario_list):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.B(image_filename="limite/assets/images/back_btn.png",
                  p=(0, 15), key=0)],
            [sg.B(image_filename="limite/assets/images/login_btn.png",
                  p=(0, 15), expand_x=True,
                  key=2) if not usuario_logado else (
                        sg.B(image_filename="limite/assets/images/logout_btn.png",
                            p=(0, 15), expand_x=True, key=2))],
            [sg.Listbox(
                usuario_list,
                s=(None, 10), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                background_color='#525255', highlight_background_color='white',
                highlight_text_color='black', sbar_relief=sg.RELIEF_FLAT,
                sbar_background_color='#cbcbcc', font=12,
                expand_x=True, key='-LB-')],
            [sg.B(image_filename="limite/assets/images/add_btn.png",
                  p=(0, 10), expand_x=True, key=1)],

            ([sg.T('_'*49, text_color='#525255',
                   justification='center', expand_x=True)],
             [sg.B(image_filename="limite/assets/images/manga_btn.png", p=(5, 10), key=4),
             sg.B(image_filename="limite/assets/images/anime_btn.png", p=(5, 10), key=3)]) if usuario_logado else []
        ], grab_anywhere=True)

    def recolhe_dados_usuario(self) -> dict:
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('DADOS USUÁRIO COMUM', justification='center', expand_x=True)],
            [sg.Fr("Nome", [
                [sg.In(key='nome', p=(5, 10), s=(37, None), font=12, focus=True)]
            ], expand_x=True)],
            [sg.Fr("Senha", [
                [sg.In(key='senha', p=(5, 10), s=(37, None), font=12)]
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
                nome = super().le_texto('Nome', values['nome'])
                senha = super().le_texto('Senha', values['senha'])
            if event in ('Cancelar', None) or all([nome, senha]):
                break
        self.close()
        return {'nome': nome, 'senha': senha} if event not in ('Cancelar', None) else {}

    def init_components_anime(self, usuario_logado, anime_list):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.B(image_filename="limite/assets/images/back_btn.png",
                  p=(0, 15), key=0)],
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
            [sg.B(image_filename="limite/assets/images/horas_btn.png",
                  p=(0, 10), expand_x=True, key=5)],
            [sg.B(image_filename="limite/assets/images/ultimos_animes_btn.png",
                  p=(0, 10), expand_x=True, key=6)],
            [sg.B(image_filename="limite/assets/images/principal_genero_btn.png",
                  p=(0, 10), expand_x=True, key=7)],
        ], grab_anywhere=True)

    def recolhe_dados_exemplar_anime(self, animes, estado = None, selecionado = None):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T(f'DADOS EXEMPLAR ANIME\n{selecionado.anime.titulo if selecionado else ""}', justification='center', expand_x=True)],
            [sg.Fr("Animes", [
                [sg.Listbox(
                    animes,
                    s=(None, 10), select_mode=sg.SELECT_MODE_SINGLE,
                    background_color='#525255', highlight_background_color='white',
                    highlight_text_color='black', sbar_relief=sg.RELIEF_FLAT,
                    sbar_background_color='#cbcbcc', font=12,
                    expand_x=True, key='-LB-', disabled=(selecionado is not None))]
            ], expand_x=True)],
            [sg.Fr("Etiqueta", [
                [sg.Combo(estado,
                    key='etiqueta', p=(5, 10), s=(37, None),
                    font=12, readonly=True)]
            ], expand_x=True)] if selecionado else [],
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
                anime = values['-LB-'][0] if values['-LB-'] else None
                if selecionado is not None:
                    estado = values['etiqueta'] if values['etiqueta'] else None
                break
            elif event in ('Cancelar', None):
                self.close()
                return 'CANC'
        self.close()
        return estado if selecionado is not None else anime

    def mostra_exemplar_anime(self, dados_exemplar: {}):
        if not dados_exemplar:
            self.mostra_mensagem("Nenhum exemplar foi selecionado!")
        else:
            self.__window = sg.Window('Biblioteca de Animes e Mangas', [
                [sg.Col([
                    [sg.T('ESTADO:')],
                    [sg.T('TITULO:')],
                    [sg.T('ANO:')],
                    [sg.T('GENERO:')],
                    [sg.T('ESTUDIO:')],
                    [sg.T('TEMPORADAS:')]
                ]),
                 sg.Col([
                     [sg.T(dados_exemplar['etiqueta'].value)],
                     [sg.T(dados_exemplar['titulo'])],
                     [sg.T(dados_exemplar['ano'])],
                     [sg.T(dados_exemplar['genero'].nome)],
                     [sg.T(dados_exemplar['estudio'].nome
                           if dados_exemplar['estudio']
                         else 'Nenhum vinculado')],
                     [sg.T(str(len(dados_exemplar['temporadas']))
                           + ' / '
                           + str(dados_exemplar['num_temporadas']))]
                 ])]
            ], modal=True).Read(close=True)

    def init_components_manga(self, usuario_logado, manga_list):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.B(image_filename="limite/assets/images/back_btn.png",
                  p=(0, 15), key=0)],
            [sg.T('MANGAS', justification='center', expand_x=True)],
            [sg.Listbox(
                manga_list,
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
            [sg.B(image_filename="limite/assets/images/paginas_btn.png",
                  p=(0, 10), expand_x=True, key=5)],
            [sg.B(image_filename="limite/assets/images/ultimos_mangas_btn.png",
                  p=(0, 10), expand_x=True, key=6)],
            [sg.B(image_filename="limite/assets/images/principal_genero_btn.png",
                  p=(0, 10), expand_x=True, key=7)],
        ], grab_anywhere=True)

    def recolhe_dados_exemplar_manga(self, mangas, estado = None, selecionado = None):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T(f'DADOS EXEMPLAR MANGA\n{selecionado.manga.titulo if selecionado else ""}', justification='center', expand_x=True)],
            [sg.Fr("Mangas", [
                [sg.Listbox(
                    mangas,
                    s=(None, 10), select_mode=sg.SELECT_MODE_SINGLE,
                    background_color='#525255', highlight_background_color='white',
                    highlight_text_color='black', sbar_relief=sg.RELIEF_FLAT,
                    sbar_background_color='#cbcbcc', font=12,
                    expand_x=True, key='-LB-', disabled=(selecionado is not None))]
            ], expand_x=True)],
            [sg.Fr("Etiqueta", [
                [sg.Combo(estado,
                    key='etiqueta', p=(5, 10), s=(37, None),
                    font=12, readonly=True)]
            ], expand_x=True)] if selecionado else [],
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
                manga = values['-LB-'][0] if values['-LB-'] else None
                if selecionado is not None:
                    estado = values['etiqueta'] if values['etiqueta'] else None
                break
            elif event in ('Cancelar', None):
                self.close()
                return 'CANC'
        self.close()
        return estado if selecionado is not None else manga

    def mostra_exemplar_manga(self, dados_exemplar: {}):
        if not dados_exemplar:
            self.mostra_mensagem("Nenhum exemplar foi selecionado!")
        else:
            self.__window = sg.Window('Biblioteca de Animes e Mangas', [
                [sg.Col([
                    [sg.T('ESTADO:')],
                    [sg.T('TITULO:')],
                    [sg.T('ANO:')],
                    [sg.T('GENERO:')],
                    [sg.T('AUTOR:')],
                    [sg.T('VOLUMES:')]
                ]),
                 sg.Col([
                     [sg.T(dados_exemplar['etiqueta'].value)],
                     [sg.T(dados_exemplar['titulo'])],
                     [sg.T(dados_exemplar['ano'])],
                     [sg.T(dados_exemplar['genero'].nome)],
                     [sg.T(dados_exemplar['autor'].nome
                           if dados_exemplar['autor']
                         else 'Nenhum vinculado')],
                     [sg.T(str(len(dados_exemplar['volumes']))
                           + ' / '
                           + str(dados_exemplar['num_volumes']))]
                 ])]
            ], modal=True).Read(close=True)

    def mostra_total_consumo(self, obra: str, consumo: str):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
                [sg.Col([
                    [sg.T('TOTAL DE HORAS ASSISTIDAS:')] if obra == 'anime' else [sg.T('TOTAL DE PAGINAS LIDAS:')],
                ]),
                 sg.Col([
                    [sg.T(f'{consumo:.2f}h')] if obra == 'anime' else [sg.T(f'{consumo} paginas')],
                ])]
            ], modal=True).Read(close=True)

    def mostra_genero(self, genero):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
                [sg.Col([
                    [sg.T('PRINCIPAL GENERO:')],
                ]),
                 sg.Col([
                    [sg.T(f'{genero}')],
                ])]
            ], modal=True).Read(close=True)

    def open(self):
        return self.__window.Read()

    def close(self):
        self.__window.Close()
