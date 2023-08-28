import dash
from dash import html
import dash_mantine_components as dmc

from libs.shell import create_breadcrumbs

dash.register_page(__name__, path="/about", title="A propos de nous | Data Logger")


def title(title):
    return dmc.Text(title, align="center", style={"fontSize": 30})


def head(text):
    return dmc.Text(text, align="center", my=10, mx=0)


layout = html.Div(
    [
        dmc.Container(
            size="lg",
            mt=5,
            children=[
                create_breadcrumbs(
                    steep_1="App",
                    steep_2="A propos de nous",
                    link_steep_1="/",
                    link_steep_2="/about",
                ),
                title(
                    "Data Logger.",
                ),
                head(
                    "Nous conçevons des dashboards specifiques à votre demande. Des Dashboards pour la production. "
                ),
                head("Code - Build - Test - Release. "),
            ],
        )
    ]
)
