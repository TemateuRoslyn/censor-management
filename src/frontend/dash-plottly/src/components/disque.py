from dash import html, dcc
import plotly.graph_objects as go
import dash_mantine_components as dmc


def create_disque(id: str, values: [], labels: [], title: str):
    """Le composant qui doit afficher les camembergs sur l'acceuil"""
    return dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Group(
                    children=[
                        dmc.Text(
                            title,
                            weight=500,
                        ),
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
                                labels=labels,
                                values=values,
                                hole=0.1,
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
                    id=id,
                )
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"width": "100%"},
    )
