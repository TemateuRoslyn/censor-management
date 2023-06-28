from dash import Output, Input, State


class ToogleSidebarCallback:
    def __init__(self, app) -> None:
        self.app = app

    def register(self):
        @self.app.callback(
            Output("sidebar-nav-wrapper", "className"),
            Output("main-wrapper", "className"),
            Output("menu-close-btn", "children"),
            Input("menu-toggle", "n_clicks"),
            [
                State("sidebar-nav-wrapper", "className"),
                State("main-wrapper", "className"),
            ],
        )
        def toogle_callback(n_clicks, sidebar_class, main_class):
            if "active" not in sidebar_class and "active" not in main_class:
                return [
                    " ".join(sidebar_class.split() + ["active"]),
                    " ".join(main_class.split() + ["active"]),
                    "menu",
                ]
            return [
                sidebar_class.replace(" active", ""),
                main_class.replace(" active", ""),
                "close",
            ]

    def register_sidebar_callbacks(self):
        @self.app.callback(
            Output("active-nav-item", "className"),
            Input("url", "pathname"),
            [
                State("nav-sidebar", "children"),
                State("active-nav-item", "className"),
            ],
        )
        def active_nav_item(pathname, nav_list, active_class):
            for i in range(len(nav_list) - 1):
                nav = nav_list[i]
                if nav["props"]["children"]["props"]["children"] is not None:
                    nav_i = nav["props"]["children"]["props"]["href"]
                    if nav_i == pathname[1:]:
                        print("Les classes sont : ", active_class, pathname)
                        if "active" not in active_class:
                            print(active_class, "Hello")
                            return " ".join(active_class.split() + ["active"])
                        return active_class.replace(" active", " ")
