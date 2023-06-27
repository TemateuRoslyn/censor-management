from dash import html


class HealthCard:
    def __init__(self) -> None:
        pass

    def render(self, icon: str, title: str, etat: str, id: str):
        return html.Div(
            [
                html.Div(
                    html.Span(
                        icon,
                        className="material-symbols-outlined",
                    ),
                    className="icon purple",
                ),
                html.Div(
                    [
                        html.H6(title, className="mb-1 ", id=id + "_title"),
                        html.H3("", className="text-bold", id=id + "_valeur"),
                        html.Small(
                            etat,
                            id=id + "_etat",
                            className="text-success text-small",
                        ),
                    ],
                    className="content mx-2",
                ),
            ],
            className="icon-card md-4",
        )
