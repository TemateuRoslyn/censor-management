from dash import Input, Output, html

from views.acceuil.acceuil_view import AcceuilView
from views.statistiques.statistiques_view import StatistiqueView
from views.about.about_view import AboutView


class RenderCallback:
    def __init__(self, app) -> None:
        self.app = app
        self.acceuil = AcceuilView()
        self.statistique = StatistiqueView()
        self.about = AboutView()

    def register(self):
        @self.app.callback(
            Output("main-wrapper", "children"),
            [
                Input("url", "pathname"),
            ],
            prevent_update=True,
        )
        def render_pages(pathname):
            if pathname == "/acceuil":
                return self.acceuil.render()
            elif pathname == "/statistiques":
                return self.statistique.render()
            elif pathname == "/about":
                return self.about.render()
            return html.H1("Page d'erreur")
