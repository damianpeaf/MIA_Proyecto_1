import PySimpleGUI as sg


sg.theme('BluePurple')


def login():

    layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(15, 1), key='output1')],
              [sg.Input(key='input1')],
              [sg.Button('Show'), sg.Button('Exit')]]

    window = sg.Window('Inicio de sesión', layout)

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Show':
            # Update the "output" text element to be the value of "input" element
            window['output1'].update(values['input1'])

    window.close()


def configure() -> dict:
    pass


def create() -> dict:
    pass


def delete() -> dict:
    pass


def update() -> dict:
    pass
