import dash
import dash_mantine_components as dmc

from dash_extensions import Lottie

dash.register_page(
    __name__,
    path="/404",
    title="404 | Data Logger",
)

layout = dmc.Stack(
    align="center",
    children=[
        Lottie(
            options=dict(
                loop=True,
                autoplay=True,
            ),
            isClickToPauseDisabled=True,
            url="https://lottie.host/b3444a5c-99e6-43bf-8d1d-fbd4c42ba229/xOi93FHEHH.json",
            width="40%",
        ),
        dmc.Text(
            [
                "Oups, on dirait que vous êtes perdu.  ",
                dmc.Anchor(
                    "Aller sur notre documentation",
                    underline=False,
                    href="https://github.com/Rushclin",
                ),
                ".",
            ]
        ),
        dmc.Anchor(
            "Retourner à l'acceuil ->",
            href="/",
            underline=False,
        ),
    ],
)
