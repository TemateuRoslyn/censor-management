from dash import html


class NotificationsComponent:
    def __init__(self) -> None:
        pass

    def render(self, titre: str, content: str):
        return html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            html.Span(titre[0:1]),
                            className="image bg-danger",
                        ),
                        html.Span(
                            [
                                html.H6(titre),
                                html.P(
                                    content,
                                    className="text-sm lead",
                                ),
                            ],
                            className="content",
                        ),
                    ],
                    className="notification",
                ),
            ],
            className="single-notification",
        )
