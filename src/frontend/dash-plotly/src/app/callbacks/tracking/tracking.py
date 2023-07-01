from dash import Input, Output
import requests
import pandas as pd
import plotly.express as px

class TrackerCallback:
    def __init__(self, app):
        self.app = app
    def updateTrackCallback(self):
        @self.app.callback(
            Output(component_id="maps-render", component_property="figure"),
            [
                Input(component_id="track-interval", component_property="n_intervals"),
            ]
        )
        def update(n_intervals):
            insert = requests.get("http://127.0.0.1:8000/tracking/insert?city=Paris&state=France&lat=48.866667&lon=2.333333")
            datas = requests.get("http://127.0.0.1:8000/tracking/next")


            fig = px.scatter_mapbox(
                data_frame=datas.json(),
                lat="lat",
                lon="lon",
                hover_name="city",
                hover_data=["state"],
                zoom=15,
                height=350,
                title="Tracker"
            )
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            # fig.update_layout(mapbox_bounds={"west": 0, "east": 10, "south": 0, "north": 51})

            fig.update_layout(
                autosize=True,
                hovermode='closest'
            )
            return fig