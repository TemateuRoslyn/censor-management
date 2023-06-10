from callbacks.render_callback import RenderCallback
from callbacks.toogle_sidebar_callback import ToogleSidebarCallback
from callbacks.login_callback import LoginCallback


class MainCallback:
    def __init__(self, app) -> None:
        RenderCallback(app).register()
        ToogleSidebarCallback(app).register()
        # LoginCallback(app).register()
