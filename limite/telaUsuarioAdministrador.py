from limite.abstractTela import AbstractTela
import PySimpleGUI as sg


class TelaUsuarioAdministrador(AbstractTela):
    def __init__(self):
        pass

    def init_components(self, usuario_logado, usuarios):
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.B(image_filename="limite/assets/images/login_btn.png", p=(0, 15), expand_x=True,
                  key=3) if not usuario_logado else sg.B(image_filename="limite/assets/images/logout_btn.png", key=3)],
            [sg.Listbox(
                usuarios,
                s=(None, 10), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                background_color='#525255', highlight_background_color='white',
                highlight_text_color='black', sbar_relief=sg.RELIEF_FLAT,
                sbar_background_color='#cbcbcc', font=12,
                expand_x=True, key='-LB-')],
            [sg.B(image_filename="limite/assets/images/add_btn.png",
                  p=(0, 10), expand_x=True, key=2)],

            ([sg.T('_'*49, text_color='#525255',
                   justification='center', expand_x=True)],
             [sg.B(image_filename="limite/assets/images/manga_btn.png", p=(5, 10), key=5),
             sg.B(image_filename="limite/assets/images/anime_btn.png", p=(5, 10), key=4)]) if usuario_logado else []
        ], grab_anywhere=True)

    def mostra_opcoes(self, usuario_logado, usuarios) -> int:
        self.init_components(usuario_logado, usuarios)
        event, values = self.open()
        # print(event, values)
        self.close()

        return event if event is not None else 0

    def recolhe_dados_usuario(self) -> dict:
        self.__window = sg.Window('Biblioteca de Animes e Mangas', [
            [sg.T('DADOS USUÁRIO ADMIN', justification='center', expand_x=True)],
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
            if event == 'Cancelar' or nome and senha:
                break
        self.close()
        return {'nome': nome, 'senha': senha} if event != 'Cancelar' else {}

    def open(self):
        return self.__window.Read()

    def close(self):
        self.__window.Close()
