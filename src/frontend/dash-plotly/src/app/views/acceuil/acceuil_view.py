from dash import html

from components.header import HeaderComponent
from components.title_page import TitlePageComponent
from components.toasts.simple_toast import SimpleToast

from views.acceuil.components.capteur_component import CapteurComponent
from views.acceuil.components.sparkline_component import SparkLineComponent


class AcceuilView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.capteur = CapteurComponent()
        self.sparkline = SparkLineComponent()
        self.simple_toast = SimpleToast()

    def render(self):
        return html.Div(
            [
                self.simple_toast.render(
                    msg="Plonger dans un bain de donnees !",
                    title="BIENVENUE",
                    cstyle="bg-primary position-absolute ml-70 mt-70 p-50",
                    ico="primary"
                ),
                self.header.render(),
                html.Section(
                    [
                        html.Div(
                            [
                                self.title_page.render(
                                    "ACCUEIL",
                                    description="Un appercu global de tous les capteurs disponibles !",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            self.capteur.render(
                                                id="capteur-1", label="Capteur 1"
                                            ),
                                            className="col-md-4 col-xs-12 mb-2",
                                        ),
                                        html.Div(
                                            self.capteur.render(
                                                id="capteur-1", label="Capteur 2"
                                            ),
                                            className="col-md-4 col-xs-12 mb-2",
                                        ),
                                        html.Div(
                                            self.capteur.render(
                                                id="capteur-1", label="Capteur 3"
                                            ),
                                            className="col-md-4 col-xs-12 mb-2",
                                        ),
                                    ],
                                    className="row mt-3",
                                ),
                                html.Div(html.H5("Capteurs"), className="row my-5"),
                                html.Div(
                                    [
                                        html.Div(
                                            self.sparkline.render(
                                                id="sparkline-1",
                                                name="Sparkline",
                                                x=None,
                                                y=None,
                                            ),
                                            className="col-md-6 col-sm-12 col-xs-12 mb-2",
                                        ),
                                        html.Div(
                                            self.sparkline.render(
                                                id="sparkline-1",
                                                name="Sparkline",
                                                x=None,
                                                y=None,
                                            ),
                                            className="col-md-6 col-sm-12 col-xs-12 mb-2",
                                        ),
                                    ],
                                    className="row mt-3",
                                ),
                            ],
                            className="container-fluid",
                        )
                    ],
                    className="section",
                ),
            ]
        )
    def render(self):
        return html.Div([
            self.header.render(),
            html.Section([
                html.Div([
                    html.H1("Bonjour le genie Rushclin")
                ], className="container-fluid")
        ], className="section")]
        )
