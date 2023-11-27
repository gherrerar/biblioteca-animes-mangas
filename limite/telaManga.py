from limite.abstractTela import AbstractTela
import PySimpleGUI as sg


class TelaManga(AbstractTela):
    def __init__(self):
        pass

    def mostra_opcoes(self, objs, type: str) -> int:
        methods = {
            'manga': self.init_components,
            'volume': self.init_components_volume,
            'capitulo': self.init_components_capitulo
        }
        methods[type](list(objs))
        event, values = self.open()
        self.close()
        
        selecionado = values['-LB-']
        return event if event is not None else 0, selecionado[0] if selecionado else None

    def init_components(self, anime_list):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('MANGAS', justification='center', expand_x=True)],
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
            [sg.B(image_filename="limite/assets/images/autor_btn.png",
                  p=(0, 10), expand_x=True, key=5)]
        ], grab_anywhere=True)

    def mostra_manga(self, dados_manga: {}):
        if not dados_manga:
            self.mostra_mensagem("Nenhum manga foi selecionado!")
        else:
            self.__window = sg.Window('Biblioteca de Animes e Mangas', [
                [sg.Col([
                    [sg.T('TITULO:')],
                    [sg.T('ANO:')],
                    [sg.T('GENERO:')],
                    [sg.T('AUTOR:')],
                    [sg.T('VOLUMES:')]
                ]),
                 sg.Col([
                     [sg.T(dados_manga['titulo'])],
                     [sg.T(dados_manga['ano'])],
                     [sg.T(dados_manga['genero'].nome)],
                     [sg.T(dados_manga['autor'].nome
                           if dados_manga['autor']
                         else 'Nenhum vinculado')],
                     [sg.T(str(len(dados_manga['volumes']))
                           + ' / '
                           + str(dados_manga['num_volumes']))]
                 ])]
            ], modal=True).Read(close=True)

    def recolhe_dados_manga(self, selecionado = None) -> dict:
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('DADOS MANGA', justification='center', expand_x=True)],
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
            [sg.Fr("Nº Volumes", [
                [sg.In(selecionado and selecionado.num_volumes,
                    key='num_volumes', p=(5, 10), s=(37, None), font=12)]
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
                [sg.B(image_filename="limite/assets/images/volume_btn.png",
                      p=(0, 10), expand_x=True, key='Volume')]
            ) if selecionado else []
        ], grab_anywhere=True)
        
        while True:
            event, values = self.open()
            
            if event == 'Confirmar':
                titulo = super().le_texto("Título", values['titulo'])
                ano = super().le_num_inteiro(
                    "Ano", values['ano'], minimo=1000, maximo=2024)
                genero = super().le_texto("Gênero", values['genero'])
                num_volumes = super().le_num_inteiro(
                    "Nº Volumes", values['num_volumes'], minimo=1)
            elif event == 'Cancelar':
                self.close()
                return 'CANC'
            elif event == 'Volume':
                self.close()
                return 'VOL'
            if all([titulo, ano, genero, num_volumes]):
                break
        self.close()
        return {'titulo': titulo, 'ano': ano, 'genero': genero, 'num_volumes': num_volumes}

    def init_components_volume(self, volume_list):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('VOLUMES MANGA', justification='center', expand_x=True)],
            [sg.Listbox(
                volume_list,
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

    def mostra_volume(self, dados_volume: {}):
        if not dados_volume:
            self.mostra_mensagem("Nenhum volume foi selecionado!")
        else:
            self.__window = sg.Window('Biblioteca de Animes e Mangas', [
                [sg.Col([
                    [sg.T('NUMERO:')],
                    [sg.T('CAPITULOS:')]
                ]),
                    sg.Col([
                        [sg.T(dados_volume['numero'])],
                        [sg.T(str(len(dados_volume['capitulos']))
                            + ' / '
                            + str(dados_volume['num_capitulos']))]
                    ])]
            ], modal=True).Read(close=True)

    def recolhe_dados_volume(self, n_vols: int, selecionado = None) -> dict:
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('DADOS VOLUME', justification='center', expand_x=True)],
            [sg.Fr("Número", [
                [sg.In(selecionado and selecionado.numero,
                       key='numero', p=(5, 10), s=(
                           37, None), font=12, focus=True)]
            ], expand_x=True)],
            [sg.Fr("Nº Capítulos", [
                [sg.In(selecionado and selecionado.num_capitulos,
                       key='num_capitulos', p=(5, 10), s=(37, None), font=12)]
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
                    "Número", values['numero'], minimo=1, maximo=n_vols)
                num_capitulos = super().le_num_inteiro(
                    "Nº Capítulos", values['num_capitulos'], minimo=1)
            elif event == 'Cancelar':
                self.close()
                return 'CANC'
            if all([numero, num_capitulos]):
                break
        self.close()
        return {'numero': numero, 'num_capitulos': num_capitulos}

    def init_components_capitulo(self, capitulo_list):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('CAPITULOS VOLUME MANGA', justification='center', expand_x=True)],
            [sg.Listbox(
                capitulo_list,
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

    def mostra_capitulo(self, dados_capitulo: {}):
        if not dados_capitulo:
            self.mostra_mensagem("Nenhum capítulo foi selecionado!")
        else:
            self.__window = sg.Window('Biblioteca de Animes e Mangas', [
                [sg.Col([
                    [sg.T('NUMERO:')],
                    [sg.T('N° DE PAGINAS:')]
                ]),
                sg.Col([
                    [sg.T(dados_capitulo['numero'])],
                    [sg.T(dados_capitulo['num_paginas'])]
                ])]
            ], modal=True).Read(close=True)

    def recolhe_dados_capitulo(self, n_caps: int) -> dict:
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('DADOS CAPITULO', justification='center', expand_x=True)],
            [sg.Fr("Número", [
                [sg.In(key='numero', p=(5, 10), s=(
                           37, None), font=12, focus=True)]
            ], expand_x=True)],
            [sg.Fr("N° de Páginas", [
                [sg.In(key='num_paginas', p=(5, 10), s=(37, None), font=12)]
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
                    "Número", values['numero'], minimo=1, maximo=n_caps)
                num_paginas = super().le_num_inteiro(
                    "Duração (min)", values['num_paginas'], minimo=5)
            elif event == 'Cancelar':
                self.close()
                return 'CANC'
            if all([numero, num_paginas]):
                break
        self.close()
        return {'numero': numero, 'num_paginas': num_paginas}

    def open(self):
        return self.__window.Read()

    def close(self):
        self.__window.Close()
