from dash import Input, Output, dcc
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import plotly.graph_objects as go
from components.modal.modal_backdrop import ModalBackdrop

class TrackerCallback:
    def __init__(self, app):
        self.app = app
    def updateTrackCallback(self):
        @self.app.callback(
            Output(component_id="maps-render", component_property="figure"),
            [
                Input(component_id="track-interval", component_property="n_intervals"),
                Input(component_id="maps-render", component_property="figure"),
            ]
        )
        def update(n_intervals, figure):
            insert = requests.get("http://127.0.0.1:8000/tracking/insert?city=Paris&state=France&lat=48.866667&lon=2.333333")
            datas = requests.get("http://127.0.0.1:8000/tracking/next").json()

            # print(figure.get('data')[0],"\n\n\n\n")
            # fig = figure.get('data')[0]
            figure.get('data')[0].update(lat=datas.get('lat'),lon=datas.get('lon'))
            # print(fig)
            return figure
    
    def showModalCallback(self):
        @self.app.callback(
            Output(component_id="factice", component_property="children"),
            [
                Input(component_id="style-id", component_property="n_clicks"),
            ]
        )
        def showModal(n_clicks):
            print(n_clicks)
            if n_clicks > 0:
                return ModalBackdrop().render("Choisir le type de carte !",
                                        [
                                            dbc.Accordion(
                                                [
                                                    dbc.AccordionItem(
                                                        [
                                                            dcc.Graph(
                                                                figure=go.Figure(
                                                                    data=go.Scattermapbox()
                                                                ).update_layout(
                                                                    margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                                                    mapbox={
                                                                        'style':'open-street-map',
                                                                        'zoom':15,
                                                                        'center':{'lon': 2.334100321220237, 'lat': 48.867453414742315},
                                                                        'bounds':{'west':0, 'east':10, 'south':0, 'north':50}
                                                                    }
                                                                )
                                                            ),
                                                            dbc.Button(id="open-street-map",children="Selectioner", className="btn btn-secondary mt-2")
                                                        ],
                                                        title='Open Street Map'
                                                    ),
                                                    dbc.AccordionItem(
                                                        [
                                                            dcc.Graph(
                                                                figure=go.Figure(
                                                                    data=go.Scattermapbox()
                                                                ).update_layout(
                                                                    margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                                                    mapbox={
                                                                        'style':'carto-positron',
                                                                        'zoom':15,
                                                                        'center':{'lon': 2.334100321220237, 'lat': 48.867453414742315},
                                                                        'bounds':{'west':0, 'east':10, 'south':0, 'north':50}
                                                                    }
                                                                )
                                                            ),
                                                            dbc.Button(id="carto-positron",children="Selectioner", className="btn btn-secondary mt-2")
                                                        ],
                                                        title='Carto Positron'
                                                    ),
                                                    dbc.AccordionItem(
                                                        [
                                                            dcc.Graph(
                                                                figure=go.Figure(
                                                                    data=go.Scattermapbox()
                                                                ).update_layout(
                                                                    margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                                                    mapbox={
                                                                        'style':'carto-darkmatter',
                                                                        'zoom':15,
                                                                        'center':{'lon': 2.334100321220237, 'lat': 48.867453414742315},
                                                                        'bounds':{'west':0, 'east':10, 'south':0, 'north':50}
                                                                    }
                                                                )
                                                            ),
                                                            dbc.Button(id="carto-darkmatter",children="Selectioner", className="btn btn-secondary mt-2")
                                                        ],
                                                        title='Carto Darkmatter'
                                                    ),
                                                    dbc.AccordionItem(
                                                        [
                                                            dcc.Graph(
                                                                figure=go.Figure(
                                                                    data=go.Scattermapbox()
                                                                ).update_layout(
                                                                    margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                                                    mapbox={
                                                                        'style':'stamen-terrain',
                                                                        'zoom':15,
                                                                        'center':{'lon': 2.334100321220237, 'lat': 48.867453414742315},
                                                                        'bounds':{'west':0, 'east':10, 'south':0, 'north':50}
                                                                    }
                                                                )
                                                            ),
                                                            dbc.Button(id="stamen-terrain",children="Selectioner", className="btn btn-secondary mt-2")
                                                        ],
                                                        title='Stamen Terrain'
                                                    ),
                                                    dbc.AccordionItem(
                                                        [
                                                            dcc.Graph(
                                                                figure=go.Figure(
                                                                    data=go.Scattermapbox()
                                                                ).update_layout(
                                                                    margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                                                    mapbox={
                                                                        'style':'stamen-toner',
                                                                        'zoom':15,
                                                                        'center':{'lon': 2.334100321220237, 'lat': 48.867453414742315},
                                                                        'bounds':{'west':0, 'east':10, 'south':0, 'north':50}
                                                                    }
                                                                )
                                                            ),
                                                            dbc.Button(id="stamen-toner",children="Selectioner", className="btn btn-secondary mt-2")
                                                        ],
                                                        title='Stamen Toner'
                                                    ),
                                                ]
                                            )
                                        ]
                                    , isopen=True)
        
    def loadAllCallbacks(self):
        self.updateTrackCallback()
        self.showModalCallback()