from dash import Dash

from layouts.app_layout import AppLayout
class App :
    def __init__(self) -> None:
        self.layout = AppLayout()
        self.app = Dash(
            __name__,
            suppress_callback_exceptions=True
        )

    def run_app(self):
        self.app.layout = self.layout.render()

        self.app.run_server(
            debug=True,
            port=8089
        )

if __name__ == '__main__':
    print("START APP")
    App().run_app()
