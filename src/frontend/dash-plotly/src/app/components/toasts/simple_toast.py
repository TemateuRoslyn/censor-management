import dash_bootstrap_components as dbc
from dash import html

class SimpleToast:
    def __init__(self) -> None:
        pass

    def render(self,msg,title,time=3000,cstyle=None,ico=None):
        return dbc.Toast(
            [
                html.P(msg)
            ],
            header=title,
            duration=time,
            class_name=cstyle,
            icon=ico
        )