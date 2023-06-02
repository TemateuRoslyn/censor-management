from dash import Input, Output
from config import renderGraph, renderDF
import requests
import pandas as pd

class Switch:
    def __init__(self, app) -> None:
        self.app = app
    def switchCallback(self):
        @self.app.callback(
            Output(component_id="figure-graph-render", component_property="figure"),
            [
                Input(component_id="graph-interval", component_property="n_intervals"),
                Input(component_id="graph-type", component_property="value"),
                Input(component_id="graph-axes-x", component_property="value"),
                Input(component_id="graph-axes-y", component_property="value"),
                Input(component_id="graph-color", component_property="value"),
                Input(component_id="quantity", component_property="value"),
            ]
        )
        def switching(n_intervals,selected:str,xasis:str,yaxis:str,color:str,cycle:int):
            insert = requests.get("http://127.0.0.1:8000/accelerometre/insert")
            datas = requests.get("http://127.0.0.1:8000/accelerometre/next?cycle={0}".format(cycle))
            if datas.status_code == requests.codes.ok:
                json_datas = datas.json()
                df = pd.DataFrame(data=json_datas)
                return renderGraph(selected, x=xasis, y=yaxis, color=color, df=df)