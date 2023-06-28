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
    def intervalStepCallback(self):
        @self.app.callback(
            Output(component_id="interval-step", component_property="children"),
            [
                Input(component_id="interval", component_property="value"),
            ]
        )
        def switchInterval1(value):
            return ("{0}%".format(m.floor(float(value))))
    def intervalQuantityCallback(self):
        @self.app.callback(
            Output(component_id="quantity-step", component_property="children"),
            [
                Input(component_id="quantity", component_property="value"),
            ]
        )
        def switchInterval2(value):
            return ("{0}%".format(m.floor(float(value))))