import dash
from dash import html
import dash_mantine_components as dmc

from libs.shell import create_breadcrumbs, create_aside
from libs.utils import create_table, subTitle, render_disk, title
from libs.datas import data_frame_enregistrement

dash.register_page(
    __name__,
    "/systeme",
    title="Système | Data Logger",
    description="Application de suppervision et de contrôle de production.",
)

layout = html.Div(
    [
        dmc.Container(
            size="lg",
            mt=5,
            children=[
                create_breadcrumbs(
                    steep_1="App",
                    steep_2="Système",
                    link_steep_1="/",
                    link_steep_2="/systeme",
                ),
                title(title="Système, USB, disque et bugs"),
                subTitle(subtile="Listing des enregistrements"),
                create_table(df=data_frame_enregistrement),
                dmc.Divider(my=20, size=0),
                subTitle(subtile="Espace disque"),
                render_disk(),
                dmc.Divider(my=20, size=0),
                subTitle(subtile="Défaut et bugs"),
                dmc.Divider(my=20, size=0),
            ],
        ),
        create_aside(
            "Liste des enregistrements, \n Espace disque, \n Espace disponible sur la clef, \n Liste des defauts/bugs",
            title="Système.",
        ),
    ]
)
