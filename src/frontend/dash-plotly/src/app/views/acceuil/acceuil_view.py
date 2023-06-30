from dash import html, dcc
import plotly.graph_objects as go
import numpy as np

from components.header import HeaderComponent
from components.title_page import TitlePageComponent

from views.acceuil.components.capteur_component import CapteurComponent
from views.acceuil.components.sparkline_component import SparkLineComponent
from views.acceuil.components.health_card import HealthCard
from views.acceuil.components.camemberg_component import CamembergComponent


class AcceuilView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.capteur = CapteurComponent()
        self.sparkline = SparkLineComponent()
        self.health = HealthCard()
        self.camemberg_1 = CamembergComponent()
        self.x0 = np.random.randn(500)
        self.x1 = np.random.randn(500) + 1
        self.histogramme = go.Figure(
            layout={
                "margin": {
                    "l": 50,
                    "r": 50,
                    "t": 50,
                    "b": 50,
                },
                "hovermode": False,
                "showlegend": False,
            },
        )
        self.histogramme.add_trace(
            go.Histogram(
                x=self.x0,
                histnorm="percent",
                name="Capteur 1",
                xbins=dict(start=0, end=11.0, size=1.0),
                marker_color="#EB89B5",
                opacity=0.75,
            )
        )
        self.histogramme.add_trace(
            go.Histogram(
                x=self.x1,
                histnorm="percent",
                name="Capteur 2",
                xbins=dict(start=0, end=11.0, size=1.0),
                marker_color="#330C73",
                opacity=0.75,
            )
        )
        self.histogramme.update_layout(
            xaxis_title_text="Période",
            yaxis_title_text="Valeur",
            bargap=0.2,
            bargroupgap=0.1,
        )

    def render(self):
        return html.Div(
            [
                self.header.render(),
                html.Section(
                    [
                        html.Div(
                            [html.H1("Bonjour le genie Rushclin")],
                            [
                                self.title_page.render(
                                    "Dashboard",
                                    description="",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            self.health.render(
                                                icon="trending_up",
                                                etat="Etat inconnue",
                                                title="Santé des capteurs",
                                                id="id_capt_health",
                                            ),
                                            className="col-md-3 col-xl-3 col-lg-4 col-sm-6",
                                        ),
                                        html.Div(
                                            self.health.render(
                                                icon="trending_up",
                                                etat="Etat inconnue",
                                                title="Accélerometres",
                                                id="id_acc_health",
                                            ),
                                            className="col-md-3 col-xl-3 col-lg-4 col-sm-6",
                                        ),
                                        html.Div(
                                            self.health.render(
                                                icon="database",
                                                etat="Inconnue",
                                                title="Capteurs thermiques",
                                                id="id_ther_health",
                                            ),
                                            className="col-md-3 col-xl-3 col-lg-4 col-sm-6",
                                        ),
                                        html.Div(
                                            self.health.render(
                                                icon="account_tree",
                                                etat="Inconnue",
                                                title="Capteurs de pression",
                                                id="id_pres_health",
                                            ),
                                            className="col-md-3 col-xl-3 col-lg-4 col-sm-6",
                                        ),
                                    ],
                                    className="row mt-3",
                                ),
                                html.Div(
                                    [
                                        self.camemberg_1.render(
                                            title="Type de Capteurs",
                                            id="types_capteurs",
                                        ),
                                        self.camemberg_1.render(
                                            title="Capteurs les plus actifs",
                                            id="capteurs_actifs",
                                        ),
                                        html.Div(
                                            html.Div(
                                                [
                                                    html.Div(
                                                        html.H6(
                                                            "Santé des capteurs sous forme de graphe"
                                                        )
                                                    ),
                                                    html.Div(
                                                        dcc.Graph(
                                                            figure=self.histogramme,
                                                        )
                                                    ),
                                                ],
                                                className="card-style mb-3",
                                            ),
                                            className="col-lg-12 col-md-12 col-sm-12 col-sx-12",
                                        ),
                                    ],
                                    className="row mt-3",
                                ),
                                html.Div(className="row mt-3"),
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
