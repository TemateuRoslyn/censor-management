from dash import html
from components.header.header_component import HeaderComponent

class AboutView:
    def __init__(self)-> None:
        self.header = HeaderComponent()

    def render(self):
        return  html.Div([
            self.header.render(),
        ])
