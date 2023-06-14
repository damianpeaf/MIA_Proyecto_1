from view.frames import login_frame, dashboard_frame
from commands.config import Store


def main():
    while True:
        if Store.IS_LOGGED is None:
            break
        elif Store.IS_LOGGED:
            dashboard_frame()
        else:
            login_frame()


if __name__ == '__main__':
    main()
