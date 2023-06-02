from dash import html, dcc


class TitlePageComponent:
    def __init__(self) -> None:
        pass

    def render(self, title: str, description=""):
        return html.Div(
            html.Div(
                [
                    html.Div(
                        html.Div(
                            html.H2(title),
                            className="title mb-30",
                        ),
                        className="col-md-6",
                    ),
                    html.Div(
                        html.Div(
                            html.Nav(
                                html.Ol(
                                    html.Li(
                                        dcc.Link(description, href=""),
                                        className="breadcrumb-item fs-5",
                                    ),
                                    className="breadcrumb",
                                )
                            ),
                            className="breadcrumb-wrapper text-end",
                        ),
                        className="col-md-6",
                    ),
                ],
                className="row align-items-center",
            ),
            className="title-wrapper pt-30",
        )
