from dash import html
from components.header.header_component import HeaderComponent
from components.title_page import TitlePageComponent


class TransformationsView:
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
                                self.title_page.render("Transformation"),
                            ],
                            className="container-fluid",
                        )
                    ],
                    className="section",
                ),
            ]
        )
