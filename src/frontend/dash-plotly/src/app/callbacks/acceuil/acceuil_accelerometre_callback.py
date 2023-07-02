from services.APIRequest import APIRequest
from dash import Input, Output, State
import plotly.graph_objs as go
from datetime import datetime, timedelta
from views.acceuil.components.sparkline_component import SparkLineComponent

UPDATE_INTERVAL = 1


class AcceuilAccelerometreCallcak:
    def __init__(self, app) -> None:
        self.app = app
        self.request = APIRequest()
        self.acc_1_Y1 = []
        self.acc_2_Y1 = []
        self.X = []
        self.acc = SparkLineComponent()

    def render_figure(self, x, y, name=None):
        return go.Figure(
            {
                "data": [
                    {
                        "x": x,
                        "y": y,
                        "mode": "lines+markers",
                        "name": name,
                        "line": {"color": "#f4d44d"},
                    }
                ],
                "layout": {
                    "xaxis": dict(showline=False, showgrid=False, zeroline=False),
                    "yaxis": dict(showgrid=False, showline=False, zeroline=False),
                    "autosize": True,
                    "showlegend": True,
                    "paper_bgcolor": "rgba(0,0,0,0)",
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    "font": {"color": "white"},
                    "height": 300,
                    "uirevision": True,
                    "margin": dict(l=0, r=0, t=4, b=4, pad=4),
                    "uirevision": True,
                },
            }
        )

    def register_acc_1(self):
        @self.app.callback(
            Output("acc_1", "figure"),
            [
                Input("acc_1_interval", "n_intervals"),
                Input("acc_1_modal_mul", "value"),
            ],
        )
        def update_capteur(n, mul: int):
            if mul == "":
                mul = 1

            datas = self.request.get("/acc2/next")
            self.X = [
                datetime.now() + timedelta(seconds=i * UPDATE_INTERVAL)
                for i in range(n + 1)
            ]

            if datas is not None:
                value = datas["time "]
                self.acc_1_Y1.append(int(float(mul) * value))

                return self.render_figure(
                    y=self.acc_1_Y1[-100:], x=self.X, name="Accélérometre"
                )

            return

    def register_acc_2(self):
        @self.app.callback(
            Output("acc_2", "figure"),
            [
                Input("acc_2_interval", "n_intervals"),
                Input("acc_2_modal_mul", "value"),
            ],
        )
        def update_capteur(n, mul: int):
            if mul == "":
                mul = 1

            datas = self.request.get("/acc2/next")
            self.X = [
                datetime.now() + timedelta(seconds=i * UPDATE_INTERVAL)
                for i in range(n + 1)
            ]

            if datas is not None:
                value = datas["time "]
                self.acc_2_Y1.append(int(float(mul) * value))

                return self.render_figure(
                    y=self.acc_2_Y1[-100:], x=self.X, name="Accélérometre"
                )

            return

    def register_acc_1_modal(self):
        @self.app.callback(
            Output("acc_1_modal", "opened"),
            Input("acc_1_modal_btn", "n_clicks"),
            Input("acc_1_modal_close", "n_clicks"),
            State("acc_1_modal", "opened"),
            prevent_initial_call=True,
        )
        def toogle_modal_acc(n_clicks, closed, opened):
            return not opened

    def register_acc_2_modal(self):
        @self.app.callback(
            Output("acc_2_modal", "opened"),
            Input("acc_2_modal_btn", "n_clicks"),
            Input("acc_2_modal_close", "n_clicks"),
            State("acc_2_modal", "opened"),
            prevent_initial_call=True,
        )
        def toogle_modal_acc(n_clicks, closed, opened):
            return not opened
