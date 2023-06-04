from dash import html
from components.header.header_component import HeaderComponent

class StatistiqueView:
    def __init__(self) -> None:
        self.header = HeaderComponent()

    def render(self):
        return html.Div([
            self.header.render(),
            html.Section([
                html.Div("Hello",className="container-fluid"),],className="section")
        ])