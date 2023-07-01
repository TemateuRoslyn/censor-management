from dash import html
from components.divider.divider_component import DividerComponent
from components.sidebar.components.sidebar_item import SidebarItem


class SidebarComponent:
    def __init__(self) -> None:
        self.divider = DividerComponent()
        self.item = SidebarItem()

    def render(self):
        return html.Aside(
            [
                html.Div(html.H4("Dashboard"), className="navbar-logo"),
                html.Div(
                    [
                        html.Ul(
                            [
                                self.item.render(
                                    icon="home", href="accueil", title="Accueil"
                                ),
                                self.divider.render(),
                                self.item.render(
                                    icon="map",
                                    href="tracking",
                                    title="Tracker",
                                ),
                                # self.item.render(
                                #     icon="auto_graph",
                                #     href="graphes",
                                #     title="Graphes",
                                # ),
                                self.divider.render(),
                                self.item.render(
                                    icon="analytics",
                                    href="datas",
                                    title="donnees",
                                ),
                                # self.item.render(
                                #     icon="transform",
                                #     href="transformations",
                                #     title="Transformations",
                                # ),
                                self.divider.render(),
                                self.item.render(
                                    icon="notifications",
                                    href="notifications",
                                    title="Notifications",
                                ),
                                self.divider.render(),
                                self.item.render(
                                    icon="partner_exchange",
                                    href="about",
                                    title="A Propos de nous",
                                ),
                                html.Div(
                                    [
                                        html.H3("SOFTMAES"),
                                        html.P("Code. Build. Test. Release."),
                                    ],
                                    className="promo-box",
                                ),
                            ]
                        )
                    ],
                    className="sidebar-nav",
                ),
            ],
            className="sidebar-nav-wrapper",
            id="sidebar-nav-wrapper",
        )
