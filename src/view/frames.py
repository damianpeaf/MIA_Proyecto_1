import PySimpleGUI as sg
from commands.config import Store
from auth import validate_user


def login_frame():
    layout = [
        [sg.Text('Usuario')], [
            sg.InputText(key='-USER-')],
        [sg.Text('Contraseña')], [
            sg.InputText(key='-PASSWORD-')],
        [sg.Button('Ingresar')]]

    window = sg.Window('Inicio de sesión', layout, size=(
        400, 200), element_justification='l', font=('Helvetica', 14))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            Store.IS_LOGGED = None
            break
        if event == 'Ingresar':
            response = validate_user(
                values['-USER-'], values['-PASSWORD-'])
            if response['ok']:
                sg.popup('Bienvenido ' + response['username'] + '!')
                Store.IS_LOGGED = True
                break
            else:
                sg.popup_error(
                    'Usuario o contraseña incorrectos', title='Error', keep_on_top=True)
                window['-USER-'].update('')
                window['-PASSWORD-'].update('')
    window.close()


def dashboard_frame():
    size_button = (10, 1)
    size_window = (900, 400)

    col = [
        [sg.T('Comandos', font=('Helvetica', 14))],
        [sg.Button('Configure', size=size_button),
         sg.Button('Transfer', size=size_button)],
        [sg.Button('Create', size=size_button),
         sg.Button('Rename', size=size_button)],
        [sg.Button('Delete', size=size_button),
         sg.Button('Modify', size=size_button)],
        [sg.Button('Copy', size=size_button),
         sg.Button('Add', size=size_button)],
        [sg.Button('Backup', size=size_button),
         sg.Button('Exec', size=size_button)],
        [sg.Button('Cerrar sesión', size=(size_button[0] * 2, size_button[1]))]
    ]

    layout = [
        [sg.Text('Consola', size=(40, 1), justification='left')],
        [sg.Multiline(size=(80, 50)), sg.Column(col)],
    ]

    window = sg.Window('Dashboard', layout, size=size_window,
                       element_justification='l', font=('Helvetica', 14))

    while True:  # Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            Store.IS_LOGGED = None
            break
        if event == 'Cerrar sesión':
            Store.IS_LOGGED = False
            break

    window.close()


def configure() -> dict:
    pass


def create() -> dict:
    pass


def delete() -> dict:
    pass


def update() -> dict:
    pass
