from callbacks.layout_callbacks.render_callback import RenderCallback
from callbacks.layout_callbacks.toogle_sidebar_callback import ToogleSidebarCallback
from callbacks.accounts.register_control import RegisterControlCallback
from callbacks.accounts.login_callback import LoginCallback
from callbacks.graphs.switching_graphs import Switch

class MainCallback:
    def __init__(self, app) -> None:
        RenderCallback(app).register()
        ToogleSidebarCallback(app).register()
        RegisterControlCallback(app).render_callbacks()
        LoginCallback(app).render_callbacks()
        Switch(app).switchCallback()
        # ToogleSidebarCallback(app).register_sidebar_callbacks()
