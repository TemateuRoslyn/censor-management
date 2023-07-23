from dash import html, dcc
from components.header.header_component import HeaderComponent
from components.title_page.title_page_component import TitlePageComponent
from components.input_group.input_group import InputGroup
from components.dropdown.dropdown import Dropdown
from components.date_range.date_range import DateRange
from components.input.input_component import InputComponent
from components.button.button_component import ButtonComponent
from datetime import datetime, date
import dash_mantine_components as dmc
from dash_iconify import DashIconify


class SauvegardeView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.input_group = InputGroup()
        self.dropdown = Dropdown()
        self.date_range = DateRange()
        self.input = InputComponent()
        self.button = ButtonComponent()

    def render(self):
        return html.Div(
            [
                self.header.render(),
                html.Section(
                    html.Div(
                        [
                            self.title_page.render(
                                "Historisation des données",
                            ),
                            html.Div(
                                html.P(
                                    "Renseignez tous les champs du formulaires et puis telechargez le fichier ",
                                    className="text-muted",
                                ),
                                className="row mt-3",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        # dmc.Select(
                                        #     data=["Capteur 1", "Capteur 2"],
                                        #     searchable=True,
                                        #     style={"width": "100%"},
                                        #     id="svg_capteur",
                                        #     label="Choisir un capteur",
                                        #     value="Capteur 1",
                                        # ),
                                        dmc.MultiSelect(
                                            label="Choisir les capteurs",
                                            placeholder="Selectionnez un capteur",
                                            id="svg_capteur",
                                            value=["Capteur 0", "Capteur 1"],
                                            data=[
                                                {"value": "c1", "label": "Capteur 1"},
                                                {"value": "c2", "label": "Capteur 2"},
                                                {"value": "c0", "label": "Capteur 0"},
                                            ],
                                            style={"width": "100%", "marginBottom": 10},
                                        ),
                                        className="col-md-6",
                                    ),
                                    html.Div(
                                        dmc.TextInput(
                                            label="La taille des donnees à téléchager ",
                                            style={"width": "100%"},
                                            # error="Entrez un nombre positif",
                                            id="svg_size",
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
                                        [
                                            dmc.DatePicker(
                                                id="svg_date_begin",
                                                label="Date de début",
                                                minDate=date(2020, 8, 5),
                                                value=datetime.now().date(),
                                                style={"width": "100%"},
                                            ),
                                        ],
                                        className="col-md-6",
                                    ),
                                    html.Div(
                                        [
                                            dmc.DatePicker(
                                                id="svg_date_end",
                                                label="Date de fin",
                                                minDate=date(2020, 8, 5),
                                                value=datetime.now().date(),
                                                style={"width": "100%"},
                                            ),
                                        ],
                                        className="col-md-6",
                                    ),
                                ],
                                className="row mt-3",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        html.Div(
                                            [
                                                html.Div(
                                                    dmc.Button(
                                                        "Télécharger en CSV",
                                                        leftIcon=DashIconify(
                                                            icon="fluent:database-plug-connected-20-filled",
                                                        ),
                                                        id="svg_download",
                                                        variant="outline",
                                                    ),
                                                    className="col-md-4",
                                                ),
                                                html.Div(
                                                    dmc.Button(
                                                        "Télécharger en TXT",
                                                        leftIcon=DashIconify(
                                                            icon="fluent:database-plug-connected-20-filled",
                                                        ),
                                                        id="svg_download",
                                                        variant="outline",
                                                    ),
                                                    className="col-md-4",
                                                ),
                                                html.Div(
                                                    dmc.Button(
                                                        "Télécharger en JSON",
                                                        leftIcon=DashIconify(
                                                            icon="fluent:database-plug-connected-20-filled",
                                                        ),
                                                        id="svg_download",
                                                        variant="outline",
                                                    ),
                                                    className="col-md-4",
                                                ),
                                                dcc.Download(id="download_data"),
                                            ],
                                            className="row",
                                        ),
                                        className="col-md-6",
                                    ),
                                ],
                                className="row mt-3",
                            ),
                        ],
                        className="container-fluid",
                    ),
                    className="section",
                ),
            ],
        )
