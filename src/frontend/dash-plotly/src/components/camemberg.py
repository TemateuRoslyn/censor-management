from dash import dcc, html
import dash_daq as daq
import dash_mantine_components as dmc
import plotly.graph_objects as go


def create_camemberg():
    """Le composant qui doit afficher les camembergs sur l'acceuil"""
    return dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Group(
                    children=[
                        dmc.Text("Graphe 1", weight=500),
                    ],
                    position="apart",
                ),
                withBorder=True,
                inheritPadding=True,
                py="xs",
            ),
            html.Div(
                dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Pie(
                                labels=[
                                    "Capteur Thermique",
                                    "Accelerometre",
                                ],
                                values=[10, 20],
                                hole=0.3,
                            )
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
                    id="graphe_1",
                )
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"width": "100%"},
    )
