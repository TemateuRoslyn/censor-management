from callbacks.layout_callbacks.render_callback import RenderCallback
from callbacks.layout_callbacks.toogle_sidebar_callback import ToogleSidebarCallback
from callbacks.acceuil.acceuil_callback import AcceuilCallback
from callbacks.acceuil.acceuil_state_callback import AcceuilStateCallback
from callbacks.acceuil.acceuil_camemberg_callback import AcceuilCamembergCallback


class MainCallback:
    def __init__(self, app) -> None:
        RenderCallback(app).register()
        ToogleSidebarCallback(app).register()
        AcceuilCallback(app).register()
        AcceuilStateCallback(app).register()
        AcceuilCamembergCallback(app).register()
