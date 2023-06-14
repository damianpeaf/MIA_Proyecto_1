from auth import validate_user


def main():
    # layout = [[sg.Text('Inicio de sesión')],
    #           [sg.Text('Usuario'), sg.InputText()],
    #           [sg.Text('Contraseña'), sg.InputText()],
    #           [sg.Button('Ingresar'), sg.Button('Cancelar')]]

    # frame = Frame('Login', layout)

    # while True:
    #     event, values = frame.read()
    #     print(event, values)
    #     if event == sg.WIN_CLOSED:
    #         break

    # frame.close()
    pass


if __name__ == '__main__':

    print('result: ' + str(validate_user('usuario1', 'junio1234')))
    print('result: ' + str(validate_user('Usuario2', 'ArchivoS_1234')))

    main()
