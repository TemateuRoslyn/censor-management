from dash import html
from components.header.header_component import HeaderComponent
from components.title_page.title_page_component import TitlePageComponent


class StatistiqueView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()

    def render(self):
        return html.Div(
            [
                self.header.render(),
                html.Section(
                    [
                        html.Div(
                            [
                                self.title_page.render("Statistiques"),
                            ],
                            className="container-fluid",
                        ),
                    ],
                    className="section",
                ),
            ]
        )
