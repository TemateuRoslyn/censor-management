from dash import html
from components.header.header_component import HeaderComponent
from components.title_page import TitlePageComponent
from components.input.input_component import InputComponent
from components.divider.divider_component import DividerComponent
from components.button.button_component import ButtonComponent
<<<<<<< HEAD
from components.cards.table import TableCard
from components.table.table import Table
import pandas as pd
=======
>>>>>>> fcbd46f (parent c88a30575362290d564b94468eef6a5cd76becb1)


class DataView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.input = InputComponent()
        self.divider = DividerComponent()
        self.button = ButtonComponent()

    def render(self):
<<<<<<< HEAD
        us_cities = pd.read_csv("us-cities-top-1k.csv")
        # print(us_cities['City'][0])
=======
>>>>>>> fcbd46f (parent c88a30575362290d564b94468eef6a5cd76becb1)
        return html.Div(
            [
                self.header.render(),
                html.Section(
                    [
                        html.Div(
                            [
<<<<<<< HEAD
                                html.Div(
                                    [
                                        html.Div(id='', className='col-lg-12 col-md-12 col-sm-12', children=[
                                            html.Div(id='', className='our_solution_category', children=[
                                                html.Div(id='', className='solution_cards_box', children=[
                                                    TableCard().render('table', "Donnees GPS", Table().renderGps(us_cities),id="1"),
                                                    TableCard().render('table', "title", Table().renderGps(us_cities),id="2"),
                                                ]),
                                                html.Div(id='', className='solution_cards_box sol_card_top_3', children=[
                                                    TableCard().render('table',"title", Table().renderGps(us_cities),id="3"),
                                                    TableCard().render('table',"title", Table().renderGps(us_cities),id="4"),
                                                ])
                                            ])
                                        ])
                                    ],
                                    className="row",
                                )
                            ],
                            className="section_our_solution m-5",
                        )
                    ],
                    className="section m-5",
=======
                                self.title_page.render(
                                    "Parametrages",
                                    description="Parametrer les composants. Capteur, Accelerometres, et autres...",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H5(
                                                    "Parametrer les capteurs",
                                                    className="text-sm my-2",
                                                ),
                                                html.Div(
                                                    self.input.render(
                                                        label="Texte",
                                                        id="input-1",
                                                        type="number",
                                                    ),
                                                    className="mb-2",
                                                ),
                                                html.Div(
                                                    self.input.render(
                                                        label="Axis",
                                                        id="input-1",
                                                        type="text",
                                                    ),
                                                    className="mb-2",
                                                ),
                                                html.Div(
                                                    self.button.render(
                                                        title="Valider",
                                                        id="button-1",
                                                        type="primary-btn w-50",
                                                    ),
                                                    className="mb-3 text-end",
                                                ),
                                            ],
                                            className="col-md-6 col-sm-12 bg-white rounded",
                                        )
                                    ],
                                    className="row",
                                ),
                            ],
                            className="container-fluid",
                        )
                    ],
                    className="section",
>>>>>>> fcbd46f (parent c88a30575362290d564b94468eef6a5cd76becb1)
                ),
            ]
        )
