from dash import Input, Output
import math as m

class Interval:
    def __init__(self, app) -> None:
        self.app = app
    def intervalCallback(self):
        @self.app.callback(
            Output(component_id="graph-interval", component_property="interval"),
            [
                Input(component_id="interval", component_property="value"),
            ]
        )
        def switchInterval(value):
            return (m.floor(float(value))*100)