from dash import Input, Output
from config import renderGraph, renderDF

class Switch:
    def __init__(self, app) -> None:
        self.app = app
    def switchCallback(self):
        @self.app.callback(
            Output(component_id="figure-graph-render", component_property="figure"),
            [
                Input(component_id="graph-type", component_property="value"),
                Input(component_id="graph-axes-x", component_property="value"),
                Input(component_id="graph-axes-y", component_property="value"),
                Input(component_id="graph-color", component_property="value"),
            ]
        )
        def switching(selected:str,xasis:str,yaxis:str,color:str):
            return renderGraph(selected, x=xasis, y=yaxis, color=color, df=renderDF())