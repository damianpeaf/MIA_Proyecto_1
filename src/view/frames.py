from commands import Observer
from analyzer.parser import parser

import PySimpleGUI as sg
from commands import CommandProxy, Logger, OperationType
from commands.config import Store
from auth import validate_user

Logger.clear_logs()
proxy = CommandProxy()
proxy.reset()


def login_frame():
    layout = [
        [sg.Text('Usuario')],
        [sg.InputText(key='-USER-')],
        [sg.Text('Contraseña')],
        [sg.InputText(key='-PASSWORD-')],
        [sg.Button('Ingresar')]
    ]

    window = sg.Window('Inicio de sesión', layout, size=(
        400, 200), element_justification='l', font=('Helvetica', 14))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            Store.IS_LOGGED = None
            break
        if event == 'Ingresar':
            response = validate_user(values['-USER-'], values['-PASSWORD-'])
            if response['ok']:
                sg.popup('Bienvenido ' + response['username'] + '!')
                Store.IS_LOGGED = True
                break
            else:
                sg.popup_error('Usuario o contraseña incorrectos',
                               title='Error', keep_on_top=True)
                window['-USER-'].update('')
                window['-PASSWORD-'].update('')
    window.close()


def create_input_window(title, inputs: list, window_size=(550, 200)):
    layout = [
        input for input in inputs
    ]
    layout.append([sg.Button('Ejecutar')])

    window = sg.Window(title, layout, size=window_size,
                       element_justification='l', font=('Helvetica', 14), resizable=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'Ejecutar':
            window.close()
            return values

    window.close()


class ConsoleObserver(Observer):

    def __init__(self, window):
        self.window = window

    def update(self, data):
        # append new command to console
        self.window['-CONSOLE-'].update(
            self.window['-CONSOLE-'].get() + '\n' + data
        )


def dashboard_frame():
    size_button = (10, 1)
    size_window = (1280, 600)

    command_list_for_buttons = [
        ('Configure', 'Transfer'),
        ('Create', 'Rename'),
        ('Delete', 'Modify'),
        ('Copy', 'Add'),
        ('Backup', 'Exec')
    ]

    list_of_buttons = [
        (sg.Button(command_1, size=size_button), sg.Button(command_2, size=size_button))for command_1, command_2 in command_list_for_buttons
    ]

    col = [
        [sg.Text('Comandos', size=(40, 1), justification='left')],
        *list_of_buttons
    ] + [
        [sg.Button('Cerrar sesión', size=(size_button[0] * 2, size_button[1]))],
    ]

    layout = [
        [sg.Text('Consola', size=(40, 1), justification='left')],
        [sg.Multiline(size=(80, 20), key="-CONSOLE-",
                      disabled=True), sg.Column(col)],
        [sg.Input(key='-COMMAND-', size=(80, 1)), sg.Button('Ejecutar')]
    ]

    window = sg.Window('Dashboard', layout, size=size_window,
                       element_justification='l', font=('Helvetica', 14))

    proxy.reset_console_event()

    console_observer = ConsoleObserver(window)
    proxy.console_event.register_observer(console_observer)

    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED:
            Store.IS_LOGGED = None
            break
        if event == 'Ejecutar':
            command = window['-COMMAND-'].get()
            if command == '':
                continue
            window['-CONSOLE-'].update(
                window['-CONSOLE-'].get() + '\n' + command)
            if command:
                try:
                    resp = parser.parse(command)

                    if resp:
                        param_name, params = resp
                        proxy.execute(param_name, params)
                except Exception as e:
                    Logger.error(e, OperationType.INPUT)

            window['-COMMAND-'].update('')

        if event == 'Add':
            values = create_input_window(
                'Add', [
                    [sg.Text('Path'), sg.Input(key='-PATH-')],
                    [sg.Text('Body')],
                    [sg.Multiline(key='-BODY-', size=(60, 5))],
                ])
            if values:
                proxy.execute('add', {
                    'path': values['-PATH-'],
                    'body': values['-BODY-']
                })
        if event == 'Backup':
            proxy.execute('backup', {})
        if event == 'Create':
            value = create_input_window(
                'Create', [
                    [sg.Text('Name'), sg.Input(key='-NAME-')],
                    [sg.Text('Body')],
                    [sg.Multiline(key='-BODY-', size=(60, 5))],
                    [sg.Text('Path'), sg.Input(
                        key='-PATH-')],
                ],
                window_size=(550, 300))
            if value:
                proxy.execute('create', {
                    'name': value['-NAME-'],
                    'body': value['-BODY-'],
                    'path': value['-PATH-'] if value['-PATH-'] else '/'
                })

        if event == 'Copy':
            values = create_input_window(
                'Copy', [
                    [sg.Text('From')],
                    [sg.Input(key='-FROM-')],
                    [sg.Text('To')],
                    [sg.Input(key='-TO-')],
                ],
                window_size=(550, 200))
            if values:
                proxy.execute('copy', {
                    'from': values['-FROM-'],
                    'to': values['-TO-']
                })

        if event == 'Configure':
            values = create_input_window(
                'Configure', [
                    [sg.Text('Type'), sg.Combo(
                        key='-TYPE-', values=['Local', 'Cloud'], default_value='Local')],
                    [sg.Text('Log encryption'), sg.Combo(
                        key='-LOG_ENCRYPTION-', values=['True', 'False'], default_value='False')],
                    [sg.Text('Read encryption'), sg.Combo(
                        key='-READ_ENCRYPTION-', values=['True', 'False'], default_value='False')],
                    [sg.Text('Encryption key'), sg.Input(
                        key='-ENCRYPTION_KEY-')],
                ],
                window_size=(550, 200))
            if values:
                proxy.execute('configure', {
                    'type': values['-TYPE-'],
                    'encrypt_log': values['-LOG_ENCRYPTION-'],
                    'encrypt_read': values['-READ_ENCRYPTION-'],
                    'llave': values['-ENCRYPTION_KEY-']
                })

        if event == 'Delete':
            values = create_input_window(
                'Delete', [
                    [sg.Text('Path'), sg.Input(key='-PATH-')],
                    [sg.Text('Name'), sg.Input(key='-NAME-')],
                ],
                window_size=(550, 200))
            if values:
                proxy.execute('delete', {
                    'path': values['-PATH-'],
                    'name': values['-NAME-']
                })

        if event == 'Exec':

            values = create_input_window(
                'Exec', [
                    [sg.Text('Path'), sg.Input(key='-PATH-')]
                ],
                window_size=(550, 200))
            if values:
                proxy.execute('exec', {
                    'path': values['-PATH-']
                })

        if event == 'Modify':
            values = create_input_window(
                'Modify', [
                    [sg.Text('Path'), sg.Input(key='-PATH-')],
                    [sg.Text('Body')],
                    [sg.Multiline(key='-BODY-', size=(60, 5))],
                ],
                window_size=(550, 200))
            if values:
                proxy.execute('modify', {
                    'path': values['-PATH-'],
                    'body': values['-BODY-']
                })
        if event == 'Rename':
            values = create_input_window(
                'Rename', [
                    [sg.Text('Path'), sg.Input(key='-PATH-')],
                    [sg.Text('Name'), sg.Input(key='-NAME-')],
                ],
                window_size=(550, 200))
            if values:
                proxy.execute('rename', {
                    'path': values['-PATH-'],
                    'name': values['-NAME-']
                })
        if event == 'Transfer':

            values = create_input_window(
                'Transfer', [
                    [sg.Text('From')],
                    [sg.Input(key='-FROM-')],
                    [sg.Text('To')],
                    [sg.Input(key='-TO-')],
                    [sg.Text('Mode')],
                    [sg.Combo(key='-MODE-', values=['Local', 'Cloud'],
                              default_value='Local')],
                ],
                window_size=(550, 200))
            if values:
                proxy.execute('transfer', {
                    'from': values['-FROM-'],
                    'to': values['-TO-'],
                    'mode': values['-MODE-']
                })

        if event == 'Cerrar sesión':
            proxy.reset_console_event()
            Logger.info('Cerrando sesión', OperationType.AUTH)
            Store.IS_LOGGED = False
            break

    window.close()
