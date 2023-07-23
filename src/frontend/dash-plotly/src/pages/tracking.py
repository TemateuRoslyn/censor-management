from dash import dash, html
import dash
import dash_mantine_components as dmc

from libs.shell import create_breadcrumbs

dash.register_page(
    __name__,
    path="/tracking",
    title="Tracking | Sencor Management",
)

layout = html.Div(
    [
        dmc.Container(
            size="lg",
            mt=5,
            children=[
                create_breadcrumbs(
                    steep_1="App",
                    steep_2="Tracker",
                    link_steep_1="/",
                    link_steep_2="/tracking",
                )
            ],
        )
    ]
)
