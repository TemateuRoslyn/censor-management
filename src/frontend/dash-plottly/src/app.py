import dash
from dash import Dash

from libs.shell import mount_app

scripts = [
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/dayjs.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/locale/ru.min.js",
    "https://www.googletagmanager.com/gtag/js?id=G-4PJELX1C4W",
    "https://media.ethicalads.io/media/client/ethicalads.min.js",
]

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    use_pages=True,
    external_scripts=scripts,
    title="Sencor Management.",
)

app.layout = mount_app(
    dash.page_registry.values(),
)

server = app.server
if __name__ == "__main__":
    app.run_server(
        debug=True,
        port=8085,
    )
