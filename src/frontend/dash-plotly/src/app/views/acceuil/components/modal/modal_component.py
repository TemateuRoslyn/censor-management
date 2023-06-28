from dash import html

# import dash_boottrap_components as dbc

# import dash_bootstrap_components as dbc


class ModalComponent:
    def __init__(self) -> None:
        pass

    def render(self):
        return html.Div(
            html.Div(
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Message de la modale"),
                            ],
                            className="modal-header",
                        )
                    ],
                    className="modal-content",
                ),
                className="modal-dialog",
            ),
            className="modal fade",
            id="modal",
        )
