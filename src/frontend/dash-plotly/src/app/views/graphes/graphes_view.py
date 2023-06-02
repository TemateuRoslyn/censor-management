from dash import html, dcc
from components.header.header_component import HeaderComponent
from components.title_page import TitlePageComponent
from components.figures.graph_figures import GraphFigure
from components.input import InputComponent
from config import renderDF


class GrapheView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.graph = GraphFigure()
        self.input = InputComponent()

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

                                dcc.Interval(
                                    id="graph-interval",
                                    disabled=False,
                                    n_intervals=0,
                                    interval=2500,
                                    max_intervals=0
                                ),
                                self.title_page.render(
                                    "GRAPHIQUE",
                                    description="Une representation graphique de vos donnees !",
                                ),
                                html.Div(
                                    [
                                        html.Div(id='', className='row m-0', children=[
                                            self.input.render(
                                                id="quantity",label="Quantite de donnees",
                                                type="range", value=25,
                                                classname="col-lg-6"),
                                            self.input.render(
                                                id="interval",label="Interval de recuperation",
                                                type="range", value=25,
                                                classname="col-lg-6"),
                                        ])
                                        ,
                                        html.Div(
                                            self.graph.render(xlabel='times',ylabel='temperatures',color='humidites'),
                                            className="",
                                        ),
                                    ],
                                    className="row mt-0",
                                ),
                            ],
                            className="container-fluid",
                        ),
                            ],
                            className="container-fluid",
                        )
                    ],
                    className="section bg-dark text-white",
                ),
            ]
        )
