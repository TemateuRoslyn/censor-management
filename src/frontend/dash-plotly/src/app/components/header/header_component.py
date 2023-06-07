from dash import html
from components.button.button_component import ButtonComponent


class HeaderComponent:
    def __init__(self) -> None:
        self.profile_image = html.Img(
            src="./assets/imgs/profile.png",
            style={
                "height": 50,
                "paddingLeft": 10,
                "paddingBottom": 10,
                "paddingTop": 10,
                "borderRadius": 50,
            },
        )
        self.button = ButtonComponent()

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
                                            self.button.render(
                                                html.Span(
                                                    "menu",
                                                    className="material-symbols-outlined",
                                                ),
                                                type="primary-btn",
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
