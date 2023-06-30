import plotly.graph_objects as go
from dash import html, dcc


class CamembergComponent:
    def __init__(self):
        self.labels = [
            "Capteur Thermique",
            "Accelerometre",
        ]
        self.values = [2, 5]

    def render(self, title: str, id: str):
        return html.Div(
            html.Div(
                [
                    html.Div(html.H6(title)),
                    html.Div(
                        dcc.Graph(
                            figure=go.Figure(
                                data=[
                                    go.Pie(
                                        labels=self.labels,
                                        values=self.values,
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
                            id=id,
                        )
                    ),
                ],
                className="card-style mb-3",
            ),
            className="col-lg-6 col-md-6 col-sm-12 col-sx-12",
        )
