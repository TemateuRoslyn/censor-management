import dash
from dash import html
import dash_mantine_components as dmc

from libs.shell import create_breadcrumbs, create_aside
from libs.utils import render_sauvegarde_form, title

dash.register_page(
    __name__,
    path="/sauvegardes",
    title="Sauvegardes | Data Logger",
)

layout = html.Div(
    [
        dmc.Container(
            size="lg",
            mt=5,
            children=[
                create_breadcrumbs(
                    steep_1="App",
                    steep_2="Sauvegardes",
                    link_steep_1="/",
                    link_steep_2="/sauvegardes",
                ),
                title("Sauvegardes des données"),
                render_sauvegarde_form(),
            ],
        ),
        create_aside(
            description="La sauvegarde de toutes les données \n Selectionnez un intervalle et telechagez les données de cet intervalle",
            title="Sauvegardes.",
        ),
    ]
)
