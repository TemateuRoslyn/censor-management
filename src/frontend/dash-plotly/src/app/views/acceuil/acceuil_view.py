from dash import html

import dash_daq as daq

from components.header import HeaderComponent
from components.title_page import TitlePageComponent

from views.acceuil.components.capteur_component import CapteurComponent
from views.acceuil.components.sparkline_component import SparkLineComponent
from views.acceuil.components.camemberg_component import CamembergComponent
from views.acceuil.components.modal.modal_component import ModalCapteur
from views.acceuil.components.analogic_input import AnalogicInput


class AcceuilView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.capteur = CapteurComponent()
        self.accelerometre = SparkLineComponent()
        self.camemberg_1 = CamembergComponent()
        self.modal = ModalCapteur()
        self.analogic_input = AnalogicInput()

    def render(self):
        return html.Div(
            [
                self.header.render(),
                html.Section(
                    [
                        html.Div(
                            [
                                self.title_page.render(
                                    "Tableau de Bord",
                                    description="",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            self.analogic_input.render(
                                                etat="Actif",
                                                title="Entrée analogique 0",
                                                id="ai_0",
                                            ),
                                            className="col-md-3 col-xl-3 col-lg-4 col-sm-6",
                                        ),
                                        html.Div(
                                            self.analogic_input.render(
                                                etat="Actif",
                                                title="Entrée analogique 1",
                                                id="ai_1",
                                            ),
                                            className="col-md-3 col-xl-3 col-lg-4 col-sm-6",
                                        ),
                                        html.Div(
                                            self.analogic_input.render(
                                                etat="Actif",
                                                title="Entrée analogique 2",
                                                id="ai_2",
                                            ),
                                            className="col-md-3 col-xl-3 col-lg-4 col-sm-6",
                                        ),
                                        html.Div(
                                            self.analogic_input.render(
                                                etat="Actif",
                                                title="Entrée analogique 3",
                                                id="ai_3",
                                            ),
                                            className="col-md-3 col-xl-3 col-lg-4 col-sm-6",
                                        ),
                                    ],
                                    className="row mt-3",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            self.analogic_input.render(
                                                etat="Actif",
                                                title="Entrée analogique 4",
                                                id="ai_4",
                                            ),
                                            className="col-md-3 col-xl-3 col-lg-4 col-sm-6",
                                        ),
                                        html.Div(
                                            self.analogic_input.render(
                                                etat="Actif",
                                                title="Entrée analogique 5",
                                                id="ai_5",
                                            ),
                                            className="col-md-3 col-xl-3 col-lg-4 col-sm-6",
                                        ),
                                        html.Div(
                                            self.analogic_input.render(
                                                etat="Actif",
                                                title="Entrée analogique 6",
                                                id="ai_6",
                                            ),
                                            className="col-md-3 col-xl-3 col-lg-4 col-sm-6",
                                        ),
                                        html.Div(
                                            self.analogic_input.render(
                                                etat="Actif",
                                                title="Entrée analogique 7",
                                                id="ai_7",
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
                                    ],
                                    className="row mt-3",
                                ),
                                html.Div(
                                    html.H5("Capteurs"),
                                    className="row my-5",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            self.capteur.render(
                                                id="capteur_1", label="Capteur 1"
                                            ),
                                            className="col-md-6 col-xs-12 mb-2",
                                        ),
                                        html.Div(
                                            self.capteur.render(
                                                id="capteur_gps", label="Capteur GPS"
                                            ),
                                            className="col-md-6 col-xs-12 mb-2",
                                        ),
                                    ],
                                    className="row mt-3",
                                ),
                                html.Div(
                                    html.H5("Accéléromètres"), className="row my-5"
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            self.accelerometre.render(
                                                id="acc_1", name="Accéléromètre 1"
                                            ),
                                            className="col-md-12 col-sm-12 col-xs-12 mb-2",
                                        ),
                                        html.Div(
                                            self.accelerometre.render(
                                                id="acc_2", name="Accéléromètre 2"
                                            ),
                                            className="col-md-12 col-sm-12 col-xs-12 mb-2",
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
                self.modal.render(
                    title="Parametrer le capteur 1",
                    id="capteur_1_modal",
                ),
                self.modal.render(
                    title="Parametrer le capteur GPS",
                    id="capteur_gps_modal",
                ),
                self.modal.render(
                    title="Parametrer l'accélérometre 1",
                    id="acc_1_modal",
                ),
                self.modal.render(
                    title="Parametrer l'accélérometre 2",
                    id="acc_2_modal",
                ),
            ]
        )
