from callbacks.layout_callbacks.render_callback import RenderCallback
from callbacks.layout_callbacks.toogle_sidebar_callback import ToogleSidebarCallback
from callbacks.acceuil.acceuil_callback import AcceuilCallback
from callbacks.acceuil.acceuil_state_callback import AcceuilStateCallback
from callbacks.acceuil.acceuil_camemberg_callback import AcceuilCamembergCallback
from callbacks.accounts.login_callback import LoginCallback
from callbacks.accounts.register_control import RegisterControlCallback
from callbacks.graphs.switching_graphs import Switch
from callbacks.interval.interval import Interval
from callbacks.tracking.tracking import TrackerCallback
from callbacks.modal.modal_callbacks import ModalCallback


class MainCallback:
    def __init__(self, app) -> None:
        RenderCallback(app).register()
        ToogleSidebarCallback(app).register()
        RegisterControlCallback(app).render_callbacks()
        LoginCallback(app).render_callbacks()
        # Switch(app).switchCallback()
        # Interval(app).intervalCallback()
        # Interval(app).intervalStepCallback()
        # Interval(app).intervalQuantityCallback()
        TrackerCallback(app).loadAllCallbacks()
        ModalCallback(app).closeModalCallback()
        # ToogleSidebarCallback(app).register_sidebar_callbacks()
        RegisterControlCallback(app).render_callbacks()
        LoginCallback(app).render_callbacks()
        # Switch(app).switchCallback()
        # Interval(app).intervalCallback()
        # Interval(app).intervalStepCallback()
        # Interval(app).intervalQuantityCallback()
        TrackerCallback(app).loadAllCallbacks()
        ModalCallback(app).closeModalCallback()
        # ToogleSidebarCallback(app).register_sidebar_callbacks()
