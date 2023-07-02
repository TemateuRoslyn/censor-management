from dash import html, dcc


class NotFound:
    def __init__(self) -> None:
        pass

    def render(self):
        return html.Div(
                [
                    html.H1("404", className="display-1"),
                    html.H4("Page refrfsrfr Found !", className="display-5"),
                    html.P(
                        "Cette page n'existe pas, vous pouve vous retrouver en cliquant sur le lien ci-dessous",
                    ),
                    dcc.Link(
                        "Retour à l'accueil",
                        href="accueil",
                        className="btn btn-outline-dark",
                    ),
                ],
                className="jumbotron justify-center",
            )