from dash import html

from components.header import HeaderComponent
from components.title_page import TitlePageComponent

from views.acceuil.components.capteur_component import CapteurComponent
from views.acceuil.components.sparkline_component import SparkLineComponent
from views.acceuil.components.health_card import HealthCard
from views.acceuil.components.camemberg_component import CamembergComponent
from views.acceuil.components.modal.modal_component import ModalCapteur


class AcceuilView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.capteur = CapteurComponent()
        self.accelerometre = SparkLineComponent()
        self.health = HealthCard()
        self.camemberg_1 = CamembergComponent()
        self.modal = ModalCapteur()

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
                                            self.health.render(
                                                icon="settings_panorama",
                                                etat="Etat inconnue",
                                                title="Capteur 1",
                                                id="id_capt1_health",
                                            ),
                                            className="col-md-3 col-xl-3 col-lg-4 col-sm-6",
                                        ),
                                        html.Div(
                                            self.health.render(
                                                icon="trending_up",
                                                etat="Etat inconnue",
                                                title="Accéleromètre 1",
                                                id="id_acc1_health",
                                            ),
                                            className="col-md-3 col-xl-3 col-lg-4 col-sm-6",
                                        ),
                                        html.Div(
                                            self.health.render(
                                                icon="database",
                                                etat="Inconnue",
                                                title="Accéleromètre 2",
                                                id="id_acc2_health",
                                            ),
                                            className="col-md-3 col-xl-3 col-lg-4 col-sm-6",
                                        ),
                                        html.Div(
                                            self.health.render(
                                                icon="share_location",
                                                etat="Inconnue",
                                                title="Capteur GPS",
                                                id="id_capt_gps_health",
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
