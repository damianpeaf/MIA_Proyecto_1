from view.frame import Frame

form_components = [
    {
        'type': 'label',
        'text': 'Username',
        'row': 0,
        'column': 0,
    },
    {
        'type': 'entry',
        'textvariable': 'username',
        'row': 0,
        'column': 1,
    },
    {
        'type': 'label',
        'text': 'Password',
        'row': 1,
        'column': 0,
    },
    {
        'type': 'entry',
        'textvariable': 'password',
        'row': 1,
        'column': 1,
    },
    {
        'type': 'button',
        'text': 'Login',
        'command': 'login',
        'row': 2,
        'column': 0,
    }
]


def main():
    login = Frame(
        title='Login',
        height=300,
        width=400,
        form_components=form_components
    )
    login.mainloop()


if __name__ == '__main__':
    main()
