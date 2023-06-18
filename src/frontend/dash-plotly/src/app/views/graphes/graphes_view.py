from dash import html
from components.header.header_component import HeaderComponent
from components.title_page import TitlePageComponent
from components.figures.graph_figures import GraphFigure


class GrapheView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.graph = GraphFigure()

    def render(self):
        return html.Div(
            [
                self.header.render(),
                html.Section(
                    [
                        html.Div(
                            [
                                html.Div(
                            [
                                self.title_page.render(
                                    "GRAPHIQUE",
                                    description="Une representation graphique de vos donnees !",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            self.graph.render(),
                                            className="mb-2",
                                        ),
                                    ],
                                    className="row mt-3",
                                ),
                            ],
                            className="container-fluid",
                        ),
                            ],
                            className="container-fluid",
                        )
                    ],
                    className="section",
                ),
            ]
        )
