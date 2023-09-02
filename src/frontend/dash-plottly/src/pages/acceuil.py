import dash
from dash import html
import dash_mantine_components as dmc

from libs.shell import create_breadcrumbs, create_aside
from libs.utils import (
    render_analogic_inputs,
    render_camemberg_graph,
    render_capteurs_graph,
    render_accelerometre_graph,
    render_disk,
    subTitle,
)


dash.register_page(
    __name__,
    "/",
    title="Acceuil | Data Logger",
    description="Application de suppervision et de contrôle de production.",
)

style = {
    "border": f"1px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
    "textAlign": "center",
}


layout = html.Div(
    [
        dmc.Container(
            size="lg",
            mt=5,
            children=[
                create_breadcrumbs(
                    steep_1="App",
                    steep_2="Acceuil",
                    link_steep_1="/",
                    link_steep_2="/",
                ),
                render_analogic_inputs(),
                subTitle(subtile="Espace disque"),
                render_disk(),
                # render_camemberg_graph(),
                render_capteurs_graph(),
                render_accelerometre_graph(),
            ],
        ),
        create_aside(
            "Ici, vous trouverez les graphes essentiels pour l'application, \n Notament les: "
        ),
    ],
)
