from dash import Input, Output, html, dcc

from views.acceuil.acceuil_view import AcceuilView
from views.statistiques.statistiques_view import StatistiqueView
from views.about.about_view import AboutView
from views.login.login_view import LoginView
from views.accounts.sign_up import SignUpView
from views.graphes.graphes_view import GrapheView
from views.notifications.notifications_view import NotificationsView
from views.data.data import DataView
from views.transformations.transformations_view import TransformationsView
from views.track.tracking_view import TrackingView
from views.track.tracking_view import TrackingView
from views.track.tracking_view import TrackingView
from views.track.tracking_view import TrackingView
from components.sidebar import SidebarComponent
from views.sauvegardes.sauvegardes_view import SauvegardeView
from views.sauvegardes.sauvegardes_view import SauvegardeView


class RenderCallback:
    def __init__(self, app) -> None:
        self.app = app
        self.acceuil = AcceuilView()
        self.statistique = StatistiqueView()
        self.about = AboutView()
        self.login = LoginView()
        self.sign_up = SignUpView()
        self.graphes = GrapheView()
        self.notifications = NotificationsView()
        self.datas = DataView()
        self.transformations = TransformationsView()
        self.sidebar = SidebarComponent()
        self.sauvegardes = SauvegardeView()
        self.track = TrackingView()

        self.pages = {
            "/sign-up": {"content": self.sign_up.render()},
            "/accueil": {"content": self.acceuil.render()},
            "/tracking": {"content": self.track.render()},
            # "/statistiques": {"content": self.statistique.render()},
            "/about": {"content": self.about.render()},
            "/notifications": {"content": self.notifications.render()},
            # "/transformations": {"content": self.transformations.render()},
            # "/graphes": {"content": self.graphes.render()},
            "/datas": {"content": self.datas.render()},
            "/": {"content": self.login.render()},
            "/sauvegardes": {"content": self.sauvegardes.render()},
        }

    def register(self):
        @self.app.callback(
            Output("main-wrapper", "children"),
            [
                Input("url", "pathname"),
            ],
            prevent_update=True,
        )
        def render_pages(pathname: str):
            if pathname in self.pages:
                if pathname.__eq__("/") or pathname.__eq__("/sign-up"):
                    return self.pages[pathname]["content"]
                else:
                    return html.Div(
                        children=[
                            self.sidebar.render(),
                            self.pages[pathname]["content"],
                        ]
                    )
            return html.Div(
                [
                    html.H1("404", className="display-1"),
                    html.H4("Page Not Found !", className="display-5"),
                    html.P(
                        "Cette page n'existe pas, vous pouve vous retrouver en cliquant sur le lien ci-dessous",
                    ),
                    dcc.Link(
                        "Retour à l'accueil",
                        href="accueil",
                        className="btn btn-outline-dark",
                    ),
                ],
                className="jumbotron justify-center",
            )
