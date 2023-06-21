from dash import html, dcc
import pandas as pd
import plotly.express as px
from components.input import InputComponent
from components.button import ButtonComponent
from components.dropdown.dropdown import Dropdown
from components.input_group.input_group import InputGroup
from config import graph as g

class GraphFigure:
    def __init__(self,df=None) -> None:
        self.df = df
        self.input = InputComponent()
        self.login_button = ButtonComponent()
        self.dropdown = Dropdown()
        self.inputg = InputGroup()

    def render(self,xlabel,ylabel,color):
        return html.Div(id='', className='', children=[
            html.Div(id='graph-render', className='', children=[
                dcc.Graph(
                    figure=px.scatter(self.df, x=xlabel, y=ylabel, color=color),
                    id="figure-graph-render",
                    animate=True,
                )
            ]),
            # html.Div(id='graph-param', className='p-0', children=[
                html.Form(id='', disable_n_clicks=True, className=' m-0 mb-5', children=[
                    html.Div(id='', className='row', children=[
                        html.Div(id='', className='col-lg-3', children=[
                            self.dropdown.render(id='graph-type',icons=g.get('icons'),options=g.get('label'), droplabel='Changer le graphique')
                        ]),
                        html.Div(id='', className='col-lg-3', children=[
                            self.dropdown.render(id='graph-axes-x',options=[xlabel, ylabel, color], droplabel='Changer les donnees en abssisse')
                        ]),
                        html.Div(id='', className='col-lg-3', children=[
                            self.dropdown.render(id='graph-axes-y',options=[ylabel, xlabel, color], droplabel='Changer les donnees en ordonnees')
                        ]),
                        html.Div(id='', className='col-lg-3', children=[
                            self.dropdown.render(id='graph-color',options=[color, xlabel, ylabel], droplabel='Changer le pattern de coloration')
                        ]),
                        # html.Div(id='', className='col-lg-3', children=[
                        #     self.inputg.render(id='',label='sfsefdeff', value='1')
                        # ])
                    ])
                ])
            # ])
        ])