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

            else:
                return [
                    sidebar_class.replace(" active", ""),
                    main_class.replace(" active", ""),
                    "close",
                ]

    # def register_sidebar_callbacks(self):
    #     @self.app.callback(
    #         Output('active-nav-item', 'className'),
    #         Input('', '')
    #     )
