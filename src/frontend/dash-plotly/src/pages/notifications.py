import dash
from dash import html
import dash_mantine_components as dmc

from libs.shell import create_breadcrumbs
from libs.utils import title

dash.register_page(
    __name__, path="/notifications", title="Notifications | Censor Management"
)

layout = html.Div(
    [
        dmc.Container(
            size="lg",
            mt=5,
            children=[
                create_breadcrumbs(
                    steep_1="App",
                    steep_2="Notifications",
                    link_steep_1="/",
                    link_steep_2="/notifications",
                ),
                title("Notifications sur votre activité"),
                dmc.Alert(
                    "Vous avez modifié le temps de chargement du module d'affichage du capteur",
                    title="Modification",
                    color="violet",
                    mb=5,
                    mt=20,
                ),
                dmc.Alert(
                    "Vous avez modifié le temps de chargement du module d'affichage du capteur",
                    title="Edition",
                    color="red",
                ),
            ],
        )
    ]
)
