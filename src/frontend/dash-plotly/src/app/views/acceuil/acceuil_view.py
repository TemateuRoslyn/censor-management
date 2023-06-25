from dash import html

from components.header import HeaderComponent
from components.title_page import TitlePageComponent

from views.acceuil.components.capteur_component import CapteurComponent
from views.acceuil.components.sparkline_component import SparkLineComponent


class AcceuilView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.capteur = CapteurComponent()
        self.sparkline = SparkLineComponent()

    def render(self):
        return html.Div(
            [
                self.header.render(),
                html.Section(
                    [
                        html.Div(
                            [
                                self.title_page.render(
                                    "Acceuil",
                                    description="Un appercu global de tous les capteurs disponibles",
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
