from limite.abstractTela import AbstractTela
import PySimpleGUI as sg


class TelaPrincipal(AbstractTela):
    def __init__(self):
        pass

    def init_components(self):
        sg.theme_add_new('ProjectTheme', {
            'BACKGROUND': '#212429',
            'TEXT': 'white',
            'INPUT': '#525255',
            'TEXT_INPUT': '#000000',
            'SCROLL': '#525255',
            'BUTTON': ('#212429', '#212429'),
            'PROGRESS': ('#01826B', '#D0D0D0'),
            'BORDER': 0,
            'SLIDER_DEPTH': 0,
            'PROGRESS_DEPTH': 0
        })
        sg.theme('ProjectTheme')
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [
                sg.B(image_filename="limite/assets/images/usuario_adm_btn.png", p=(5, 20), tooltip="Usuário Administrador", key=1),
                sg.B(image_filename="limite/assets/images/usuario_comum_btn.png", p=(5, 20), tooltip="Usuário Comum", key=2)
            ],
            [sg.B(image_filename="limite/assets/images/quit_btn.png", expand_x=True, key=0)]
        ], grab_anywhere=True)

    def mostra_opcoes(self) -> int:
        self.init_components()
        event, values = self.open()

        return event if event is not None else 0

    def open(self):
        return self.__window.Read(close=True)

    def close(self):
        self.__window.Close()
