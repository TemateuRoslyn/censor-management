from callbacks.layout_callbacks.render_callback import RenderCallback
from callbacks.layout_callbacks.toogle_sidebar_callback import ToogleSidebarCallback
from callbacks.acceuil.acceuil_callback import AcceuilCallback
from callbacks.acceuil.acceuil_state_callback import AcceuilStateCallback
from callbacks.acceuil.acceuil_camemberg_callback import AcceuilCamembergCallback
from callbacks.accounts.login_callback import LoginCallback
from callbacks.accounts.register_control import RegisterControlCallback
from callbacks.interval.interval import Interval
from callbacks.graphs.switching_graphs import Switch


class MainCallback:
    def __init__(self, app) -> None:
        RenderCallback(app).register()
        ToogleSidebarCallback(app).register()
        RegisterControlCallback(app).render_callbacks()
        LoginCallback(app).render_callbacks()
        Switch(app).switchCallback()
        Interval(app).intervalCallback()
        Interval(app).intervalStepCallback()
        Interval(app).intervalQuantityCallback()
        AcceuilCallback(app).register()
        AcceuilStateCallback(app).register()
        AcceuilCamembergCallback(app).register()
        # ToogleSidebarCallback(app).register_sidebar_callbacks()
