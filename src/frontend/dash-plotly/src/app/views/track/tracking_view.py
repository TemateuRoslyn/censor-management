from dash import html, dcc
import dash_bootstrap_components as dbc
from components.header.header_component import HeaderComponent
from components.title_page import TitlePageComponent
from components.modal.modal_backdrop import ModalBackdrop
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
                                interval=5000,
                                max_intervals=0
                            ),
                            html.Span(id='', className='d-flex justify-content-around ', children=[
                                html.Button(id='style-id', className='btn btn-secondary m-2 p-2', children=[
                                    html.Span(id='', className='', children=[
                                        html.Span(id='', className='material-symbols-outlined icon', children=['map'])
                                        ,html.Label(id='', className='fs-4', children="Style"),
                                    ]),
                                    
                                ],n_clicks=0),
                                html.Button(id='zoom-id', className='btn btn-secondary m-2 p-2', children=[
                                    html.Span(id='', className='', children=[
                                        html.Span(id='', className='material-symbols-outlined icon', children=['zoom_in'])
                                        ,html.Label(id='', className='fs-4', children="Zoom"),
                                    ])
                                    
                                ]),
                                html.Button(id='special-id', className='btn btn-secondary m-2 p-2', children=[
                                        html.Span(id='', className='material-symbols-outlined icon', children=['add_location'])
                                        ,html.Label(id='', className='fs-4', children="Point Special"),
                                ]),
                                html.Button(id='layouts-id', className='btn btn-secondary m-2 p-2', children=[
                                        html.Span(id='', className='material-symbols-outlined icon', children=['dashboard'])
                                        ,html.Label(id='', className='fs-4', children="Layouts"),
                                ])
                            ]),
                            dcc.Graph(
                                id="maps-render",
                                figure=fig,
                                className="shadow p-3 mb-5 bg-body rounded"
                            )
                        ],
                        className="container-fluid",
                        )
                    ],
                    className="section m-5",
                ),
            ]
        )
