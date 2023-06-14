from auth import validate_user
from analyzer.lexer import lexer


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
    lexer.input(
        'create -name->"prueba 2.txt" -path->/"carpeta 2"/-body->"Este es el contenido del archivo 2"')
    lexer.input(
        'delete -path->/"carpeta 2"/'
    )
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


if __name__ == '__main__':
    main()
