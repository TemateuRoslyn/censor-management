from dash import Input, Output, html

from views.acceuil.acceuil_view import AcceuilView
from views.statistiques.statistiques_view import StatistiqueView
from views.about.about_view import AboutView
from views.login.login_view import LoginView


class RenderCallback:
    def __init__(self, app) -> None:
        self.app = app
        self.acceuil = AcceuilView()
        self.statistique = StatistiqueView()
        self.about = AboutView()
        self.login = LoginView()

        self.pages = {
            "/acceuil": {
                "content": self.acceuil.render(),
            },
            "/statistiques": {
                "content": self.statistique.render(),
            },
            "/about": {
                "content": self.about.render(),
            },
            "/": {
                "content": self.login.render(),
            },
        }

    def register(self):
        @self.app.callback(
            Output("main-wrapper", "children"),
            [
                Input("url", "pathname"),
            ],
            prevent_update=True,
        )
        def render_pages(pathname):
            if pathname in self.pages:
                return self.pages[pathname]["content"]
            return html.H1("Page d'erreur")
