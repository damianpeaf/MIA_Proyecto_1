import PySimpleGUI as sg
from commands.config import Store
from auth import validate_user


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


def create_input_window(title, inputs, execute_callback):
    layout = [[sg.Text(label), sg.InputText(key=key)] for label, key in inputs]
    layout.append([sg.Button('Ejecutar')])

    window = sg.Window(title, layout, size=(400, 200),
                       element_justification='l', font=('Helvetica', 14))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'Ejecutar':
            execute_callback(values)
            break

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

    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED:
            Store.IS_LOGGED = None
            break
        if event == 'Add':
            create_input_window(
                'Add', [('Path', '-PATH-'), ('Body', '-BODY-')])
        if event == 'Backup':
            pass
        if event == 'Create':
            create_input_window(
                'Create', [('Name', '-NAME-'), ('Type', '-TYPE-'), ('Path', '-PATH-')])
        if event == 'Copy':
            create_input_window('Copy', [('From', '-FROM-'), ('To', '-TO-')])
        if event == 'Configure':
            create_input_window('Configure', [('Type', '-TYPE-'), ('Log encryption', '-LOG_ENCRYPTION-'),
                                              ('Read encryption',
                                               '-READ_ENCRYPTION-'),
                                              ('Encryption key', '-ENCRYPTION_KEY-')])
        if event == 'Delete':
            create_input_window(
                'Delete', [('Path', '-PATH-'), ('Name', '-NAME-')])
        if event == 'Exec':
            create_input_window('Exec', [('Path', '-PATH-')])
        if event == 'Modify':
            create_input_window(
                'Modify', [('Path', '-PATH-'), ('Body', '-BODY-')])
        if event == 'Rename':
            create_input_window(
                'Rename', [('Path', '-PATH-'), ('Name', '-NAME-')])
        if event == 'Transfer':
            create_input_window(
                'Transfer', [('From', '-FROM-'), ('To', '-TO-'), ('Mode', '-MODE-')])
        if event == 'Cerrar sesión':
            Store.IS_LOGGED = False
            break

    window.close()
