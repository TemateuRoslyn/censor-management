from dash import html, dcc
from components.header.header_component import HeaderComponent
from components.title_page.title_page_component import TitlePageComponent
from components.input_group.input_group import InputGroup
from components.dropdown.dropdown import Dropdown
from components.date_range.date_range import DateRange


class SauvegardeView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.input_group = InputGroup()
        self.dropdown = Dropdown()
        self.date_range = DateRange()

    def render(self):
        return html.Div(
            [
                self.header.render(),
                html.Section(
                    html.Div(
                        [
                            self.title_page.render(
                                "Historisation des capteurs",
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
                                        self.dropdown.render(
                                            droplabel="Hello",
                                            title="Choisir un capteur",
                                            id="Hello",
                                            options=["hello", "h"],
                                        ),
                                        className="col-md-6",
                                    ),
                                    html.Div(
                                        self.date_range.render(
                                            id="he",
                                            label="Date de début et date de fin",
                                        ),
                                        className="col-md-6",
                                    ),
                                ],
                                className="row mt-2",
                            ),
                        ],
                        className="container-fluid",
                    ),
                    className="section",
                ),
            ],
        )
