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
            ],
        )
        def switchInterval(value):
            return m.floor(float(value)) * 100

    def intervalStepCallback(self):
        @self.app.callback(
            Output(component_id="interval-step", component_property="children"),
            [
                Input(component_id="interval", component_property="value"),
            ],
        )
        def switchInterval1(value):
            return "{0}%".format(m.floor(float(value)))

    def intervalQuantityCallback(self):
        @self.app.callback(
            Output(component_id="quantity-step", component_property="children"),
            [
                Input(component_id="quantity", component_property="value"),
            ],
        )
        def switchInterval2(value):
            return "{0}%".format(m.floor(float(value)))

    def capteur_1_interval(self):
        @self.app.callback(
            Output("capteur_1_interval", "interval"),
            Input("capteur_1_modal_freq", "value"),
        )
        def switch_capteur_1_interval(value: float):
            if value == "":
                return 1
            return m.floor(float(value)) * 1000

    def capteur_gps_interval(self):
        @self.app.callback(
            Output("capteur_gps_interval", "interval"),
            Input("capteur_gps_modal_freq", "value"),
        )
        def switch_capteur_gps_interval(value: float):
            if value == "":
                return 1
            return m.floor(float(value)) * 1000

    def capteur_acc_1_interval(self):
        @self.app.callback(
            Output("acc_1_interval", "interval"),
            Input("acc_1_modal_freq", "value"),
        )
        def switch_capteur_gps_interval(value: float):
            if value == "":
                return 1
            return m.floor(float(value)) * 1000

    def capteur_acc_2_interval(self):
        @self.app.callback(
            Output("acc_2_interval", "interval"),
            Input("acc_2_modal_freq", "value"),
        )
        def switch_capteur_gps_interval(value: float):
            if value == "":
                return 1
            return m.floor(float(value)) * 1000
