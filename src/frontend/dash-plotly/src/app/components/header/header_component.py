from dash import html


class HeaderComponent:
    def __init__(self) -> None:
        self.profile_image = html.Img(
            src="./assets/imgs/profile.png",
            style={
                "height": 50,
                "padding-left": 10,
                "padding-bottom": 10,
                "padding-top": 10,
                "border-radius": 50,
            },
        )

    def render(self):
        return html.Header(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    html.Div(
                                        html.Div(
                                            html.Button(
                                                html.Span(
                                                    "menu",
                                                    className="material-symbols-outlined icon",
                                                ),
                                                className="main-btn primary-btn btn-hover",
                                                id="menu-toggle",
                                            ),
                                            className="menu-toggle-btn mr-20",
                                        ),
                                        className="header-left d-flex align-items-center",
                                    ),
                                    className="col-lg-5 col-md-5 col-6",
                                ),
                                html.Div(
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Button(
                                                        html.Div(
                                                            html.Div(
                                                                [
                                                                    html.H6(
                                                                        "Rushclin 02"
                                                                    ),
                                                                    self.profile_image,
                                                                ],
                                                                className="info",
                                                            ),
                                                            className="profile-info",
                                                        ),
                                                        className="dropdown-toggle bg-transparent border-0",
                                                        type="button",
                                                        id="profile",
                                                    ),
                                                    # html.Ul(
                                                    #     [html.Li(html.A("Profile"))],
                                                    #     className="dropdown-menu dropdown-menu-end",
                                                    # ),
                                                ],
                                                className="profile-box ml-15",
                                            )
                                        ],
                                        className="header-right",
                                    ),
                                    className="col-lg-7 col-md-7 col-6",
                                ),
                            ],
                            className="row",
                        ),
                    ],
                    className="container-fluid",
                )
            ],
            className="header",
        )
