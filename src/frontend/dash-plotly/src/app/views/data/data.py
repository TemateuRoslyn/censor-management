from dash import html
from components.header.header_component import HeaderComponent
from components.title_page import TitlePageComponent
from components.input.input_component import InputComponent
from components.divider.divider_component import DividerComponent
from components.button.button_component import ButtonComponent
from components.cards.table import TableCard
from components.table.table import Table
import pandas as pd


class DataView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.input = InputComponent()
        self.divider = DividerComponent()
        self.button = ButtonComponent()

    def render(self):
        us_cities = pd.read_csv("us-cities-top-1k.csv")
        # print(us_cities['City'][0])
        return html.Div(
            [
                self.header.render(),
                html.Section(
                    [
                        html.Div(
                            [
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
                ),
            ]
        )
