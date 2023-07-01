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


        print(datas.get('lat'))
        fig = go.Figure(
            data=go.Scattermapbox(
            mode="markers+lines",
            lat=datas.get('lat'),
            lon=datas.get('lon'),
            marker={'size':20},
            )
        )


        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            mapbox={
                'style':'open-street-map',
                'zoom':5,
                'center':{'lon':2.320041, 'lat':48.8588897}
            }
        )
        # fig.show()
        # fig = px.scatter_mapbox(
        #     data_frame=datas,
        #     lat="lat",
        #     lon="lon",
        #     hover_name="city",
        #     hover_data=["state"],
        #     zoom=15,
        #     height=350,
        #     title="Tracker"
        # )
        # fig.update_layout(mapbox_style="open-street-map")
        # fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        # # fig.update_layout(mapbox_bounds={"west": 0, "east": 10, "south": 0, "north": 51})

        # fig.update_layout(
        #     autosize=True,
        #     hovermode='closest'
        # )
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
                                max_intervals=0
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
