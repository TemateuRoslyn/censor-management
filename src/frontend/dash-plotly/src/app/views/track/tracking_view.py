from dash import html, dcc
from components.header.header_component import HeaderComponent
from components.title_page import TitlePageComponent
import plotly.graph_objects as go
import plotly.express as px
import requests



class TrackingView:
    def __init__(self) -> None:
        self.header = HeaderComponent()
        self.title_page = TitlePageComponent()

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
                'zoom':17,
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

                            dcc.Interval(
                                id="track-interval",
                                disabled=False,
                                n_intervals=0,
                                interval=10000,
                                max_intervals=-1
                            ),
                            html.Div(
                                [
                                    dcc.Graph(
                                        id="maps-render",
                                        figure=fig,
                                    )
                                ],
                                className="row ",
                            ),
                        ],
                        className="container-fluid",
                        )
                    ],
                    className="section m-5 shadow p-3 mb-5 bg-body rounded",
                ),
            ]
        )
