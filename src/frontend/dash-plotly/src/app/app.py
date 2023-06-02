from dash import Dash

from layouts.app_layout import AppLayout
from layouts.auth_layout import AuthLayout

from callbacks.main_callback import MainCallback


class App:
    def __init__(self) -> None:
        self.layout = AppLayout()
        self.app = Dash(__name__, title='Censor Managment', update_title='Chargement...', suppress_callback_exceptions=True,)

        self.callback = MainCallback(self.app)

    def run_app(self):
        self.app.layout = self.layout.render()

        self.app.run_server(debug=True, port=8089)


if __name__ == "__main__":
    print("START APP")
    App().run_app()
