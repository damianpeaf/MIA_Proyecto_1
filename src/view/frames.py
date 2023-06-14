import PySimpleGUI as sg
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

    while True:  # Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Ingresar':

            response = validate_user(
                values['-USER-'], values['-PASSWORD-'])
            if response['ok']:
                sg.popup('Bienvenido ' + response['username'] + '!')
                break
            else:
                sg.popup_error(
                    'Usuario o contraseña incorrectos', title='Error', keep_on_top=True)
                window['-USER-'].update('')
                window['-PASSWORD-'].update('')

    window.close()


def dashboard_frame():
    layout = [
        [sg.Text('Dashboard')]
    ]

    window = sg.Window('Dashboard', layout, size=(
        700, 700), element_justification='l', font=('Helvetica', 14))

    while True:  # Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break


def configure() -> dict:
    pass


def create() -> dict:
    pass


def delete() -> dict:
    pass


def update() -> dict:
    pass
