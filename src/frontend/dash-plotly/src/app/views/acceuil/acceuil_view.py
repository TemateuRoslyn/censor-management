from dash import html

from components.header import HeaderComponent

class AcceuilView:
    def __init__(self) -> None:
        self.header = HeaderComponent()

    def render(self):
        return html.Div([
            self.header.render(),
            html.Section([
                html.Div([
                    html.H1("Bonjour le genie Rushclin")
                ], className="container-fluid")
        ], className="section")]
        )