from dash import html, Output, Input, State

# import dash_boottrap_components as dbc


class AcceuilCallback:
    def __init__(self, app) -> None:
        self.app = app

    def register(self):
        @self.app.callback(
            Output("modal", "className"),
            Input("modal-btn", "n_clicks"),
            State("modal", "className"),
        )
        def modal(n_open, is_open):
            print("Open modal", n_open, is_open)
            if n_open:
                return not is_open
            return is_open
