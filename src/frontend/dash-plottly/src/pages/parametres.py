import dash
from dash import html

import dash_mantine_components as dmc

from libs.shell import create_breadcrumbs
from libs.utils import title, render_parametre_form

dash.register_page(
    __name__,
    path="/parametres",
    title="Paramètres | Data Logger.",
)

layout = html.Div(
    [
        dmc.Container(
            size="lg",
            mt=5,
            children=[
                create_breadcrumbs(
                    steep_1="App",
                    steep_2="Paramètres",
                    link_steep_1="/",
                    link_steep_2="/parametres",
                ),
                title("Paramètres des capteurs"),
                render_parametre_form(),
            ],
        )
    ]
)
