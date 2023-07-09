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
<<<<<<< HEAD
=======
from views.track.tracking_view import TrackingView
>>>>>>> fcbd46f (parent c88a30575362290d564b94468eef6a5cd76becb1)
from components.sidebar import SidebarComponent
from views.sauvegardes.sauvegardes_view import SauvegardeView
<<<<<<< HEAD
from views.not_found.not_found import NotFound
=======
>>>>>>> ad6c424 (parent c88a30575362290d564b94468eef6a5cd76becb1)


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
            "/parametres": {"content": self.transformations.render()},
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
            return NotFound().render()
