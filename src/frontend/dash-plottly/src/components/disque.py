from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import dash_mantine_components as dmc
from services.request import get_request, post_request


def create_disque(id: str, values: [], labels: [], title: str):
    """Le composant qui doit afficher les camembergs sur l'acceuil"""
    return dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Group(
                    children=[
                        dmc.Text(title, weight=500),
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
                        data=[go.Pie(labels=labels, values=values, hole=0.1)],
                        layout={
                            "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
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


""" Implementaion des callbacks """


def run_callback(output_id: str):
    @callback(
        [Output(output_id, "children")],
        Input("liste_disque", "value"),
    )
    def update_disque(disque):
        """Je recupere d'abord tous les disques branché"""
        api_url_usb_find_all = get_request("http://localhost:5003/api/usb/find_all")

        if api_url_usb_find_all is not None:
            print("api_url_usb_find_all ====>", api_url_usb_find_all)
            usb_present = api_url_usb_find_all["usb_present"]
            usb_mount_paths = api_url_usb_find_all["usb_mount_paths"]

            """Utiliser cette variable pour afficher un toast"""
            message = api_url_usb_find_all["message"]

            """Je recupère à present l'espace sur les differents disque"""
            if usb_present:
                create_disque_graph = []
                for mount_path in usb_mount_paths:
                    print("mount_path ====>", mount_path)

                    response = post_request(
                        "http://localhost:5003/api/usb/usage",
                        data={"mount_dir": mount_path},
                    )
                    values = response["values"]

                    create_disque_graph.insert(
                        html.Div(
                            create_disque(
                                id=mount_path,
                                labels=["Espace libre", "Espace occupé"],
                                title=mount_path,
                                values=[
                                    values["total"] - values["used"],
                                    values["used"],
                                ],
                            )
                        )
                    )
                return create_disque_graph
            else:
                return [html.Div("Aucun disque présent")]

        else:
            return [html.Div("Aucun disque présent")]


run_callback(output_id="liste_disque")
