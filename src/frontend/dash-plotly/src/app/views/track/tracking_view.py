from dash import html, dcc
import dash_bootstrap_components as dbc
from components.header.header_component import HeaderComponent
from components.title_page import TitlePageComponent
from components.modal.modal_backdrop import ModalBackdrop
from components.modal.modal_behaviour import ModalBehaviour
import plotly.graph_objects as go
import plotly.express as px
import requests



class TrackingView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()
        self.modal = ModalBackdrop()

    def render(self):
        insert = requests.get("http://127.0.0.1:8000/tracking/insert?city=Paris&state=France&lat=48.866667&lon=2.333333")
        datas = requests.get("http://127.0.0.1:8000/tracking/next").json()


        # print(datas.get('lat'))
        fig = go.Figure(
            data=go.Scattermapbox(
            mode="markers+lines",
            lat=datas.get('lat'),
            lon=datas.get('lon'),
            marker={'size':10},
            connectgaps=True,
            selectedpoints=[0],
            selected={
                'marker':{
                    'color':'green',
                    'size':15,
                }
            },
            )
        )


        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            mapbox={
                'style':'open-street-map',
                'zoom':16,
                'center':{'lon': 2.334100321220237, 'lat': 48.867453414742315},
                'bounds':{'west':0, 'east':10, 'south':0, 'north':50}
            }
        )

        return html.Div(
            [
                self.header.render(),
                html.Section(
                    [
                            html.Div(
                        [
                            html.Div(id='factice', className='',),
                            dcc.Interval(
                                id="track-interval",
                                disabled=False,
                                n_intervals=0,
                                interval=6000,
                                max_intervals=-1
                            ),
                            html.Span(id='', className='d-flex justify-content-around ', children=[
                                # html.Button(id='style-id', className='btn btn-secondary m-2 p-2', children=[
                                #     html.Span(id='', className='', children=[
                                #         html.Span(id='', className='material-symbols-outlined icon', children=['map'])
                                #         ,html.Label(id='', className='fs-4', children="Style"),
                                #     ]),
                                # ],n_clicks=0),
                                html.Button(id='zoom-id', className='btn btn-secondary m-2 p-2', children=[
                                    html.Span(id='', className='', children=[
                                        html.Span(id='', className='material-symbols-outlined icon', children=['zoom_in'])
                                        ,html.Label(id='', className='fs-4', children="Zoom"),
                                    ]),
                                    dbc.Toast(
                                        id="zoom-toast",
                                        dismissable=True,
                                        is_open=False,
                                        header="Regler le niveau du zoom",
                                        children=[
                                            dbc.Input(id="zoom-size", type='range', value=16, max=20, min=1, className="form-range bg-tranparent border-0")
                                        ],
                                        className="position-absolute top-0 start-25 bg-body"
                                    )
                                    
                                ],n_clicks=0),
                                html.Button(id='special-id', className='btn btn-secondary m-2 p-2', children=[
                                        html.Span(id='', className='material-symbols-outlined icon', children=['add_location'])
                                        ,html.Label(id='', className='fs-4', children="Point Special"),
                                        ModalBehaviour().render(
                                            modalheadermsg="Rentrez les coordonnees de la zones !",
                                            modalbody=[
                                                html.Div(id='', className='row mb-2', children=[
                                                    html.Div(id='', className='col-lg-6', children=[
                                                       dbc.InputGroup(
                                                        [dbc.InputGroupText('Pays :'), dbc.Input(id='pays',placeholder='France')]
                                                       ) 
                                                    ]),
                                                    html.Div(id='', className='col-lg-6', children=[
                                                       dbc.InputGroup(
                                                        [dbc.InputGroupText('Latitude :'), dbc.Input(id='lat',placeholder='48.8588897')]
                                                       ) 
                                                    ]),
                                                ]),
                                                html.Div(id='', className='row', children=[
                                                    html.Div(id='', className='col-lg-6', children=[
                                                        dbc.InputGroup(
                                                            [dbc.InputGroupText('Ville :'), dbc.Input(id='ville',placeholder='Paris')]
                                                        ) 
                                                    ]),
                                                    html.Div(id='', className='col-lg-6', children=[
                                                        dbc.InputGroup(
                                                            [dbc.InputGroupText('Longitude :'), dbc.Input(id='lon',placeholder='2.320041')]
                                                        ) 
                                                    ]),
                                                ]),
                                            ])
                                ],n_clicks=0),
                                # html.Button(id='layouts-id', className='btn btn-secondary m-2 p-2', children=[
                                #         html.Span(id='', className='material-symbols-outlined icon', children=['dashboard'])
                                #         ,html.Label(id='', className='fs-4', children="Layouts"),
                                        
                                # ],n_clicks=0)
                            ]),
                            dcc.Graph(
                                id="maps-render",
                                figure=fig,
                                className="shadow p-3 mb-5 bg-body rounded"
                            ),
                        ],
                        className="container-fluid",
                        )
                    ],
                    className="section m-5",
                ),
            ]
        )
