from dash import html
from components.header.header_component import HeaderComponent
from components.title_page.title_page_component import TitlePageComponent
import dash_daq as daq


class StatistiqueView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.theme = {
            "dark": True,
            "detail": "#007439",
            "primary": "#00EA64",
            "secondary": "#6E6E6E",
        }

    def render(self):
        return html.Div(
            [
                self.header.render(),
                html.Section(
                    [
                        html.Div(
                            [
                                self.title_page.render("Statistiques"),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H4(
                                                    "Nombre de consultation",
                                                    className="mb-2",
                                                ),
                                                daq.LEDDisplay(
                                                    value="3.14159",
                                                    color=self.theme["secondary"],
                                                    className="w-100",
                                                ),
                                                # className="card bg-dark",
                                            ],
                                            className="col-md-3 col-sm-12",
                                        ),
                                        html.Div(
                                            [
                                                html.H4(
                                                    "Nombre de visites",
                                                    className="mb-2",
                                                ),
                                                daq.LEDDisplay(
                                                    value="3.14159",
                                                    color=self.theme["secondary"],
                                                    className="w-100",
                                                ),
                                                # className="card bg-dark",
                                            ],
                                            className="col-md-3 col-sm-12",
                                        ),
                                        html.Div(
                                            [
                                                html.H4(
                                                    "Nombre de ",
                                                    className="mb-2",
                                                ),
                                                daq.LEDDisplay(
                                                    value="3.14159",
                                                    color=self.theme["secondary"],
                                                    className="w-100",
                                                ),
                                                # className="card bg-dark",
                                            ],
                                            className="col-md-3 col-sm-12",
                                        ),
                                        html.Div(
                                            [
                                                html.H4(
                                                    "Nombre de consultation",
                                                    className="mb-2",
                                                ),
                                                daq.LEDDisplay(
                                                    value="3.14159",
                                                    color=self.theme["secondary"],
                                                    className="w-100",
                                                ),
                                                # className="card bg-dark",
                                            ],
                                            className="col-md-3 col-sm-12",
                                        ),
                                    ],
                                    className="mt-2 row",
                                ),
                                html.Div(
                                    [
                                        self.title_page.render("Santé des capteurs"),
                                        html.Div(
                                            [
                                                html.P(
                                                    "Capteur 1",
                                                    className="text-center text-small mb-2",
                                                ),
                                                daq.Thermometer(
                                                    min=95,
                                                    max=105,
                                                    value=98.6,
                                                    className="dark-theme-control",
                                                ),
                                            ],
                                            className="col-md-3 col-sm-12",
                                        ),
                                    ],
                                    className="row mt-2",
                                ),
                            ],
                            className="container-fluid",
                        ),
                    ],
                    className="section",
                ),
            ]
        )
