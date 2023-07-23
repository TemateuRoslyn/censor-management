from dash import html
from components.header import HeaderComponent
from components.title_page import TitlePageComponent
import dash_mantine_components as dmc
from dash_iconify import DashIconify


class ParametreView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.list_entree_analogiques = [
            "Entrée analogique 01",
            "Entrée analogique 02",
            "Entrée analogique 03",
            "Entrée analogique 04",
            "Entrée analogique 05",
            "Entrée analogique 06",
            "Entrée analogique 07",
        ]
        self.type_capteurs = [
            "Accéléromètre",
            "Microphone",
        ]

        self.list_unite = [
            "G",
            "Metre carré / seconde",
            "Inches / seconde carré",
        ]

    def render(self):
        return html.Div(
            [
                self.header.render(),
                html.Section(
                    [
                        html.Div(
                            [
                                self.title_page.render(
                                    "Paramétrage",
                                ),
                                html.Div(
                                    html.P(
                                        "Renseignez tous les champs du formulaires pour le parmétrage du capteur selectionné.",
                                        className="text-muted",
                                    ),
                                    className="row mt-3",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            dmc.Select(
                                                data=self.list_entree_analogiques,
                                                searchable=False,
                                                style={"width": "100%"},
                                                id="",
                                                label="Selectionnez l'entrée analigique :",
                                                value=self.list_entree_analogiques[0],
                                            ),
                                            className="col-md-6",
                                        ),
                                        html.Div(
                                            dmc.TextInput(
                                                label="Entrez la sensitivité :",
                                                style={"width": "100%"},
                                                # error="Valeur invalide",
                                                id="",
                                                type="number",
                                            ),
                                            className="col-md-6",
                                        ),
                                    ],
                                    className="row mt-2",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            dmc.Select(
                                                data=self.list_unite,
                                                searchable=False,
                                                style={"width": "100%"},
                                                id="",
                                                label="Selectionnez l'unité de la sensitivité :",
                                                value=self.list_unite[0],
                                            ),
                                            className="col-md-6",
                                        ),
                                        html.Div(
                                            dmc.Select(
                                                data=self.type_capteurs,
                                                searchable=False,
                                                style={"width": "100%"},
                                                id="",
                                                label="Type du capteur :",
                                                value=self.type_capteurs[0],
                                            ),
                                            className="col-md-6",
                                        ),
                                    ],
                                    className="row mt-2",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            dmc.TextInput(
                                                label="Entrez le nom du capteur :",
                                                style={"width": "100%"},
                                                # error="Valeur invalide",
                                                id="",
                                                type="text",
                                            ),
                                            className="col-md-6",
                                        ),
                                        html.Div(
                                            dmc.Select(
                                                data=self.list_unite,
                                                searchable=False,
                                                style={"width": "100%"},
                                                id="",
                                                label="Unité :",
                                                value=self.list_unite[0],
                                            ),
                                            className="col-md-6",
                                        ),
                                    ],
                                    className="row mt-3",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dmc.Button(
                                                    "Valider",
                                                    variant="outline",
                                                    leftIcon=DashIconify(
                                                        icon="fluent:settings-32-regular"
                                                    ),
                                                ),
                                            ],
                                            className="col-md-6",
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
