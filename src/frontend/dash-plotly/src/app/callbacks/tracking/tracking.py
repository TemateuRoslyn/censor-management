from dash import Input, Output, State, dcc, no_update
import dash_bootstrap_components as dbc
import requests
import math
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
                Input(component_id="zoom-size", component_property="value"),
                Input(component_id="maps-render", component_property="figure"),
            ]
        )
        def update(n_intervals, zoom, figure):
            insert = requests.get("http://127.0.0.1:8000/tracking/insert?city=Paris&state=France&lat=48.866667&lon=2.333333")
            datas = requests.get("http://127.0.0.1:8000/tracking/next").json()

            # print("zoom = {0}".format(math.floor(float(zoom))))
            # fig = figure.get('data')[0]
            figure.get('data')[0].update(lat=datas.get('lat'),lon=datas.get('lon'))
            figure.get('layout').get('mapbox').update({'zoom':math.floor(float(zoom))})
            # print(figure.get('layout').get('mapbox'),"\n\n")
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
                                                            dbc.Button(id="open-street-map",children="Selectioner", className="btn btn-secondary mt-2", n_clicks=0)
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
                                                            dbc.Button(id="carto-positron",children="Selectioner", className="btn btn-secondary mt-2", n_clicks=10000)
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
                                                            dbc.Button(id="carto-darkmatter",children="Selectioner", className="btn btn-secondary mt-2", n_clicks=20000)
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
                                                            dbc.Button(id="stamen-terrain",children="Selectioner", className="btn btn-secondary mt-2", n_clicks=40000)
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
                                                            dbc.Button(id="stamen-toner",children="Selectioner", className="btn btn-secondary mt-2", n_clicks=50000)
                                                        ],
                                                        title='Stamen Toner'
                                                    ),
                                                ]
                                            )
                                        ]
                                    , isopen=True)
        
    def updateZoomCallback(self):
        @self.app.callback(
            Output(component_id="zoom-toast", component_property="is_open"),
            [
                Input(component_id="zoom-id", component_property="n_clicks"),
            ]
        )
        def update(nclicks):
            print(nclicks)
            if not (nclicks % 2 == 0):
                return True
            return no_update

    def showBehaviourCallback(self):
        @self.app.callback(
            Output(component_id="modal-behaviour", component_property="is_open"),
            [
                Input(component_id="special-id", component_property="n_clicks"),
                Input(component_id="pays", component_property="value"),
                Input(component_id="lat", component_property="value"),
                Input(component_id="ville", component_property="value"),
                Input(component_id="lon", component_property="value"),
                Input(component_id="close-backdrop", component_property="n_clicks"),
            ],
            [State(component_id="modal-behaviour", component_property="is_open")]
        )
        def showBehaviour(n1, pays, lat, ville, lon, n2, is_open):
            if n2 > 0:
                if pays is not None and lat is not None and ville is not None and lon is not None:
                    if len(pays) > 2 and len(ville) > 2 and len(lat) > 4 and len(lon) > 4:
                        insert = requests.get("http://127.0.0.1:8000/tracking/insert?city={0}&state={1}&lat={2}&lon={3}".format(ville, pays, lat, lon))
                        # print(insert)
                        return False
            if n1 > 0:
                return True
            return False
        
    def showLayoutsBehaviourCallback(self):
        @self.app.callback(
            Output(component_id="modal-behaviour", component_property="is_open"),
            [
                Input(component_id="layouts-id", component_property="n_clicks"),
                Input(component_id="pays", component_property="value"),
                Input(component_id="lat", component_property="value"),
                Input(component_id="ville", component_property="value"),
                Input(component_id="lon", component_property="value"),
                Input(component_id="close-backdrop", component_property="n_clicks"),
            ],
            [State(component_id="modal-behaviour", component_property="is_open")]
        )
        def showLayoutBehaviour():
            pass
           
    def loadAllCallbacks(self):
        self.updateTrackCallback()
        self.showModalCallback()
        self.updateZoomCallback()
        self.showBehaviourCallback()