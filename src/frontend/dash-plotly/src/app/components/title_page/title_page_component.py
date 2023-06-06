from dash import html


class TitlePageComponent:
    def __init__(self) -> None:
        pass

    def render(self, title: str):
        return html.Div(
            html.Div(
                [
                    html.Div(
                        html.Div(
                            html.H2(title),
                            className="title mb-30",
                        ),
                        className="col-md-6",
                    )
                ],
                className="row align-items-center",
            ),
            className="title-wrapper pt-30",
        )
