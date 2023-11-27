from limite.abstractTela import AbstractTela
import PySimpleGUI as sg


class TelaAutor(AbstractTela):
    def __init__(self):
        pass

    def init_components(self, autor_list):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.B(image_filename="limite/assets/images/back_btn.png",
                  p=(0, 15), key=0)],
            [sg.T('AUTORES', justification='center', expand_x=True)],
            [sg.Listbox(
                autor_list,
                s=(None, 10),
                background_color='#525255', highlight_background_color='white',
                highlight_text_color='black', sbar_relief=sg.RELIEF_FLAT,
                sbar_background_color='#cbcbcc', font=12,
                expand_x=True, key='-LB-')],
            [sg.B(image_filename="limite/assets/images/read_btn_2.png",
                  expand_x=True, tooltip='Mostrar', key=1),
             sg.B(image_filename="limite/assets/images/edit_btn_2.png",
                  expand_x=True, tooltip='Editar', key=3)],

            [sg.B(image_filename="limite/assets/images/add_btn.png",
                  p=(0, 10), expand_x=True, key=2)]
        ], grab_anywhere=True)

    def mostra_opcoes(self, autores) -> int:
        self.init_components(list(autores))
        event, values = self.open()
        self.close()

        selecionado = values['-LB-']
        return event if event is not None else 0, selecionado[0] if selecionado else None

    def mostra_autor(self, dados_autor: {}):
        if not dados_autor:
            self.mostra_mensagem("Nenhum autor foi selecionado!")
        else:
            self.__window = sg.Window('Biblioteca de Animes e Mangas', [
                [sg.Col([
                    [sg.T('NOME:')],
                    [sg.T('MANGAS:')]
                ]),
                    sg.Col([
                        [sg.T(dados_autor['nome'])],
                        [sg.T(dados_autor['mangas'] or 'Nenhum vinculado')]
                    ])]
            ], modal=True).Read(close=True)

    def recolhe_dados_autor(self, mangas, selecionado = None) -> str:
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('DADOS AUTOR', justification='center', expand_x=True)],
            [sg.Fr("Nome", [
                [sg.In(selecionado and selecionado.nome,
                       disabled=(selecionado is not None),
                       key='nome', p=(5, 10), s=(
                           37, None), font=12, focus=True)]
            ], expand_x=True)],
            [sg.Fr("Mangas", [
                [sg.Listbox(
                    mangas,
                    s=(None, 10), select_mode=sg.SELECT_MODE_MULTIPLE,
                    background_color='#525255', highlight_background_color='white',
                    highlight_text_color='black', sbar_relief=sg.RELIEF_FLAT,
                    sbar_background_color='#cbcbcc', font=12,
                    expand_x=True, key='-LB-')]
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
                if not selecionado:
                    attr = super().le_texto("Nome", values['nome'])
                    break
                else:
                    attr = values['-LB-']
                    break
            elif event in ('Cancelar', None):
                self.close()
                return 'CANC'
            if attr:
                break
        self.close()
        return attr

    def open(self):
        return self.__window.Read()

    def close(self):
        self.__window.Close()
