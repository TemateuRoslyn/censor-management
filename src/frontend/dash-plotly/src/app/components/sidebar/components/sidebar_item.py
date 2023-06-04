from dash import html


class SidebarItem:
    def __init__(self) -> None:
        pass

    def render(self, title, href, icon):
        return html.Li(
            html.A(
                [
                    html.Span(
                        icon,
                        className="material-symbols-outlined icon",
                    ),
                    html.Span(title, className="text"),
                ],
                href=href,
            ),
            className="nav-item",
        )
