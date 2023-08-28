from dash import Output, Input, clientside_callback, html, dcc, page_container, State
from dash_iconify import DashIconify

import dash_mantine_components as dmc

from libs.utils import title, render_sensor_settings_form, render_ai_settings_form


def render_settings_tabs():
    return dmc.Tabs(
        [
            dmc.TabsList(
                grow=True,
                children=[
                    dmc.Tab(
                        "Paramétrer les capteurs",
                        value="1",
                    ),
                    dmc.Tab(
                        "Paramétrer les AI",
                        value="2",
                    ),
                ],
            ),
            dmc.TabsPanel(
                [
                    title("Paramétrer des capteurs"),
                    render_sensor_settings_form(),
                ],
                value="1",
                mt=20,
            ),
            dmc.TabsPanel(
                [
                    title("Paramétrer les entrées analogiques"),
                    render_ai_settings_form(),
                ],
                value="2",
                mt=20,
            ),
        ],
        value="1",
    )


def create_breadcrumbs(
    steep_1: str, link_steep_1: None, steep_2: str, link_steep_2: None
):
    """Creation des breadcrumbs pour afficher le chemin jusqu'à l'acceuil"""
    return dmc.Breadcrumbs(
        separator="→",
        children=[
            dmc.Anchor(steep_1, href=link_steep_1, underline=False),
            dmc.Anchor(steep_2, href=link_steep_2, underline=False),
        ],
        mb=20,
    )


def create_home_link(label):
    return dmc.Anchor(
        label,
        size="xl",
        href="/",
        underline=False,
    )


def create_header_link(icon, href, size=22, color="indigo"):
    return dmc.Anchor(
        dmc.ThemeIcon(
            DashIconify(
                icon=icon,
                width=size,
            ),
            variant="outline",
            radius=30,
            size=36,
            color=color,
        ),
        href=href,
        target="_blank",
    )


def create_header(nav_data):
    """HEADER FOR APP"""

    return dmc.Header(
        height=70,
        fixed=True,
        px=25,
        children=[
            dmc.Stack(
                justify="center",
                style={"height": 70},
                children=dmc.Grid(
                    children=[
                        dmc.Col(
                            [
                                dmc.MediaQuery(
                                    create_home_link("Data Logger."),
                                    smallerThan="lg",
                                    styles={"display": "none"},
                                ),
                                dmc.MediaQuery(
                                    create_home_link("Data Logger."),
                                    largerThan="lg",
                                    styles={"display": "none"},
                                ),
                            ],
                            span="content",
                            pt=12,
                        ),
                        dmc.Col(
                            span="auto",
                            children=dmc.Group(
                                position="right",
                                spacing="xl",
                                children=[
                                    create_header_link(
                                        "radix-icons:github-logo",
                                        "https://github.com/Rushclin/",
                                    ),
                                    create_header_link(
                                        "material-symbols:mail-outline",
                                        "mailto:takamrushclin@gmail.com",
                                    ),
                                    create_header_link(
                                        "mdi:telephone-in-talk-outline",
                                        "tel:+237690139627",
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="radix-icons:blending-mode", width=22
                                        ),
                                        variant="outline",
                                        radius=30,
                                        size=36,
                                        color="yellow",
                                        id="color-scheme-toggle",
                                    ),
                                    dmc.MediaQuery(
                                        dmc.ActionIcon(
                                            DashIconify(
                                                icon="radix-icons:hamburger-menu",
                                                width=18,
                                            ),
                                            id="drawer-hamburger-button",
                                            variant="outline",
                                            size=36,
                                        ),
                                        largerThan="lg",
                                        styles={"display": "none"},
                                    ),
                                ],
                            ),
                        ),
                    ]
                ),
            )
        ],
    )


def create_nav_item(
    path: str,
    title: str,
    icon="home",
):
    return html.Li(
        [
            dcc.Link(
                [
                    html.Span(
                        icon,
                        className="material-symbols-outlined icon",
                    ),
                    html.Span(
                        title,
                        className="text",
                    ),
                ],
                href=path,
                className="nav-link",
            ),
        ],
        className="nav-item",
    )


def create_main_nav_link(icon, label, href):
    return dmc.Anchor(
        dmc.Group(
            [
                DashIconify(
                    icon=icon,
                    width=23,
                    color=dmc.theme.DEFAULT_COLORS["indigo"][5],
                ),
                dmc.Text(label, size="sm"),
            ]
        ),
        href=href,
        variant="text",
        mb=5,
        style={"fontSize": "20px"},
    )


def create_side_nav_content(nav_data):
    main_links = dmc.Stack(
        mt=20,
        children=[
            html.Ul(
                html.Li(
                    create_nav_item(
                        path="/",
                        title="Accueil",
                    ),
                    className="nav-item",
                )
            ),
            dmc.Divider(),
            html.Ul(
                html.Li(
                    create_nav_item(path="/tracking", title="Tracker", icon="map"),
                    className="nav-item",
                )
            ),
            dmc.Divider(),
            html.Ul(
                [
                    html.Li(
                        create_nav_item(
                            path="/parametres", title="Paramètres", icon="settings"
                        ),
                        className="nav-item",
                        style={"marginBottom": 20},
                    ),
                    html.Li(
                        create_nav_item(
                            path="/sauvegardes", title="Sauvegardes", icon="save"
                        ),
                        className="nav-item",
                        style={"marginBottom": 20},
                    ),
                    html.Li(
                        create_nav_item(
                            path="/systeme", title="Système", icon="sensor_door"
                        ),
                        className="nav-item",
                    ),
                ]
            ),
            dmc.Divider(),
            html.Ul(
                html.Li(
                    create_nav_item(
                        path="/notifications",
                        title="Notifications",
                        icon="notifications",
                    ),
                    className="nav-item",
                ),
            ),
            dmc.Divider(),
            html.Ul(
                html.Li(
                    create_nav_item(
                        path="/about", title="A propos de nous", icon="partner_exchange"
                    ),
                    className="nav-item",
                ),
            ),
        ],
        style={"marging": 0},
    )
    return dmc.Stack(
        spacing=0,
        children=[
            main_links,
        ],
        px=25,
    )


def create_side_navbar(nav_data):
    """SIDEBAR FOR THE APP"""

    return dmc.Navbar(
        fixed=True,
        id="components-navbar",
        position={"top": 70},
        width={"base": 300},
        children=[
            dmc.ScrollArea(
                offsetScrollbars=True,
                type="scroll",
                children=create_side_nav_content(nav_data),
            )
        ],
    )


def create_navbar_drawer(nav_data):
    return dmc.Drawer(
        id="components-navbar-drawer",
        overlayOpacity=0.55,
        overlayBlur=3,
        zIndex=9,
        size=300,
        children=[
            dmc.ScrollArea(
                offsetScrollbars=True,
                type="scroll",
                style={"height": "100vh"},
                pt=20,
                children=create_side_nav_content(nav_data),
            )
        ],
    )


def create_aside(description: str, title="Une description de la section"):
    return dmc.Aside(
        position={"top": 140, "right": 0},
        fixed=True,
        id="toc-navbar",
        width={"base": 300},
        zIndex=10,
        children=[
            dmc.Text(
                title,
                align="center",
                my=10,
                weight="bold",
            ),
            dmc.Text(
                description,
                align="center",
                my=10,
                mx=0,
            ),
        ],
        withBorder=True,
    )


def mount_app(nav_data):
    return dmc.MantineProvider(
        dmc.MantineProvider(
            theme={
                "fontFamily": "'Poppins', sans-serif",
                "primaryColor": "indigo",
                "components": {
                    "Button": {"styles": {"root": {"fontWeight": 400}}},
                    "Alert": {"styles": {"title": {"fontWeight": 500}}},
                    "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
                },
            },
            children=[
                dcc.Store(
                    id="theme-store",
                    storage_type="local",
                ),
                dcc.Location(id="url", refresh="callback-nav"),
                dmc.NotificationsProvider(
                    [
                        create_header(nav_data),
                        create_side_navbar(nav_data),
                        create_navbar_drawer(nav_data),
                        html.Div(
                            dmc.Container(
                                size="lg",
                                pt=90,
                                children=page_container,
                            ),
                            id="wrapper",
                        ),
                    ]
                ),
            ],
        ),
        theme={"colorScheme": "light"},
        id="theme-provider",
        withGlobalStyles=True,
        withNormalizeCSS=True,
    )


clientside_callback(
    """ function(data) { return data } """,
    Output("theme-provider", "theme"),
    Input("theme-store", "data"),
)

clientside_callback(
    """function(n_clicks, data) {
        if (data) {
            if (n_clicks) {
                const scheme = data["colorScheme"] == "dark" ? "light" : "dark"
                return { colorScheme: scheme } 
            }
            return dash_clientside.no_update
        } else {
            return { colorScheme: "light" }
        }
    }""",
    Output("theme-store", "data"),
    Input("color-scheme-toggle", "n_clicks"),
    State("theme-store", "data"),
)

clientside_callback(
    """
    function(children) { 
        ethicalads.load();
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return null
    }
    """,
    Output("select-component", "value"),
    Input("_pages_content", "children"),
)

clientside_callback(
    """
    function(value) {
        if (value) {
            return value
        }
    }
    """,
    Output("url", "pathname"),
    Input("select-component", "value"),
)

clientside_callback(
    """function(n_clicks) { return true }""",
    Output("components-navbar-drawer", "opened"),
    Input("drawer-hamburger-button", "n_clicks"),
    prevent_initial_call=True,
)
