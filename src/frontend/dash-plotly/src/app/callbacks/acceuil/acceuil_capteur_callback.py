from dash import Input, Output, State
from services.APIRequest import APIRequest


class AcceuilCapteurCallback:
    def __init__(self, app) -> None:
        self.app = app
        self.service = APIRequest()

    def register_capteur_1(self):
        @self.app.callback(
            Output("capteur_1", "value"),
            [
                Input("capteur_1_interval", "n_intervals"),
                Input("capteur_1_modal_mul", "value"),
            ],
            prevent_initial_call=True,
        )
        def register_callback(n_intervals: int, multiplicateur: int):
            if multiplicateur == "":
                multiplicateur = 1

            datas = self.service.get("/acc2/next")
            value: int = datas["time "]

            return int(float(multiplicateur) * value)

    def register_capteur_gps(self):
        @self.app.callback(
            Output("capteur_gps", "value"),
            [
                Input("capteur_gps_interval", "n_intervals"),
                Input("capteur_gps_modal_mul", "value"),
            ],
        )
        def register_callback(n_intervals: int, multiplicateur: int):
            if multiplicateur == "":
                multiplicateur = 1

            datas = self.service.get("/acc2/next")
            value: int = datas["time "]

            return int(float(multiplicateur) * value)

    def register_modal_capteur_1(self):
        @self.app.callback(
            Output("capteur_1_modal", "opened"),
            Input("capteur_1_modal_btn", "n_clicks"),
            Input("capteur_1_modal_close", "n_clicks"),
            State("capteur_1_modal", "opened"),
            prevent_initial_call=True,
        )
        def toogle_modal_capteur(n_clicks, closed, opened):
            return not opened

    def register_modal_capteur_gps(self):
        @self.app.callback(
            Output("capteur_gps_modal", "opened"),
            Input("capteur_gps_modal_btn", "n_clicks"),
            Input("capteur_gps_modal_close", "n_clicks"),
            State("capteur_gps_modal", "opened"),
            prevent_initial_call=True,
        )
        def toogle_modal_capteur(n_clicks, closed, opened):
            return not opened
