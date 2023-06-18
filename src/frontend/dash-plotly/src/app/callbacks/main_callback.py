from callbacks.layout_callbacks.render_callback import RenderCallback
from callbacks.layout_callbacks.toogle_sidebar_callback import ToogleSidebarCallback
from callbacks.accounts.register_control import RegisterControlCallback

class MainCallback:
    def __init__(self, app) -> None:
        RenderCallback(app).register()
        ToogleSidebarCallback(app).register()
        RegisterControlCallback(app).render_callbacks()
        # ToogleSidebarCallback(app).register_sidebar_callbacks()
