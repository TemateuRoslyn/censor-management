from dash import Output, Input, State, html, dcc
import plotly.graph_objects as go
import numpy as np


class AcceuilCamembergCallback:
    def __init__(self, app) -> None:
        self.app = app
        self.labels = [
            "Capteur 3",
            "Capteur 5",
        ]
        self.values = [2, 5]

    def register(self):
        @self.app.callback(
            [Output("types_capteurs", "figure"), Output("capteurs_actifs", "figure")],
            Input("interval-component", "n_intervals"),
        )
        def register_callback(n_intervals):
            return [
                go.Figure(
                    data=[
                        go.Pie(
                            labels=[
                                "Capteurs",
                                "Accelerometre",
                            ],
                            values=np.arange(1, 4, 1),
                            hole=0.3,
                        ),
                    ],
                    layout={
                        "margin": {
                            "l": 50,
                            "r": 50,
                            "t": 50,
                            "b": 50,
                        },
                        "plot_bgcolor": "rgba(0, 0, 0, 0)",
                    },
                ),
                go.Figure(
                    data=[
                        go.Pie(
                            labels=["Accelerometre Nord", "Comparateur", "Capteur Sud"],
                            values=np.arange(1, 5, 1),
                            hole=0.3,
                        ),
                    ],
                    layout={
                        "margin": {
                            "l": 50,
                            "r": 50,
                            "t": 50,
                            "b": 50,
                        },
                        "plot_bgcolor": "rgba(0, 0, 0, 0)",
                    },
                ),
            ]
