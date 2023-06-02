from dash import html
from components.button.button_component import ButtonComponent
from config import user


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
                                                    "close",
                                                    className="material-symbols-outlined m-0",
                                                    id="menu-close-btn",
                                                ),
                                                type="btn btn-secondary p-1",
                                                id="menu-toggle",
                                            ),
                                            className="",
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
                                                                        user.get('name')
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
            className="header p-1 pb-2 border-bottom border-primary border-1 bg-dark",
        )
