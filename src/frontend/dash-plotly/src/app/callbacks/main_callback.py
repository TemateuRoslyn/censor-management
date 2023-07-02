from callbacks.layout_callbacks.render_callback import RenderCallback
from callbacks.layout_callbacks.toogle_sidebar_callback import ToogleSidebarCallback
from callbacks.acceuil.acceuil_state_callback import AcceuilStateCallback
from callbacks.acceuil.acceuil_camemberg_callback import AcceuilCamembergCallback
from callbacks.accounts.login_callback import LoginCallback
from callbacks.accounts.register_control import RegisterControlCallback
from callbacks.graphs.switching_graphs import Switch
from callbacks.interval.interval import Interval
from callbacks.sauvegardes.sauvegardes_callback import SauvegardesCallback
from callbacks.acceuil.acceuil_capteur_callback import AcceuilCapteurCallback
from callbacks.acceuil.acceuil_accelerometre_callback import AcceuilAccelerometreCallcak


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
        Interval(app).capteur_1_interval()
        Interval(app).capteur_gps_interval()
        Interval(app).capteur_acc_1_interval()
        Interval(app).capteur_acc_2_interval()
        SauvegardesCallback(app).register()
        AcceuilStateCallback(app).register()
        AcceuilCapteurCallback(app).register_capteur_1()
        AcceuilCapteurCallback(app).register_capteur_gps()
        AcceuilCapteurCallback(app).register_modal_capteur_1()
        AcceuilCapteurCallback(app).register_modal_capteur_gps()

        AcceuilAccelerometreCallcak(app).register_acc_1()
        AcceuilAccelerometreCallcak(app).register_acc_2()
        AcceuilAccelerometreCallcak(app).register_acc_1_modal()
        AcceuilAccelerometreCallcak(app).register_acc_2_modal()
