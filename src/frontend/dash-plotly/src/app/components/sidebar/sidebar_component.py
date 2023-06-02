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
                                    icon="home", href="accueil", title="Acceuil"
                                ),
                                self.divider.render(),
                                self.item.render(
                                    icon="insert_chart",
                                    href="statistiques",
                                    title="Statistiques",
                                ),
                                self.item.render(
                                    icon="auto_graph",
                                    href="graphes",
                                    title="Graphes",
                                ),
                                self.divider.render(),
                                self.item.render(
                                    icon="settings",
                                    href="parametrages",
                                    title="Paramétrages",
                                ),
                                self.item.render(
                                    icon="transform",
                                    href="transformations",
                                    title="Transformations",
                                ),
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
                                self.divider.render(),
                                html.Div(
                                    [
                                        html.H3("SOFTMAES"),
                                        html.P("Code. Build. Test. Release."),
                                    ],
                                    className="promo-box",
                                ),
                            ],
                            id="nav-sidebar",
                        )
                    ],
                    className="sidebar-nav",
                ),
            ],
            className="sidebar-nav-wrapper bg-dark",
            id="sidebar-nav-wrapper",
        )
