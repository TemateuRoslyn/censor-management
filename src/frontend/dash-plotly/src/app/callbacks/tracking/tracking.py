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