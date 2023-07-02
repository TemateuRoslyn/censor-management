import dash_mantine_components as dmc
from dash_iconify import DashIconify


class ModalCapteur:
    def __init__(self) -> None:
        pass

    def render(self, title: str, id: str):
        return dmc.Modal(
            title=title,
            id=id,
            centered=True,
            zIndex=10000,
            children=[
                dmc.TextInput(
                    label="Entrez la fréquence de récupération des données (en secondes)",
                    type="number",
                    id=id + "_freq",
                    value=1,
                ),
                dmc.TextInput(
                    label="Multiplicateur",
                    type="number",
                    id=id + "_mul",
                    value=1,
                ),
                dmc.Button(
                    "Valider",
                    leftIcon=DashIconify(
                        icon="fluent:database-plug-connected-20-filled"
                    ),
                    variant="outline",
                    mt=5,
                    id=id + "_close",
                ),
            ],
        )
