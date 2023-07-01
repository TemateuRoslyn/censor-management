from dash import html, dcc


def renderIcon(icons, i):
    if icons is not None:
        return html.Span(icons[i], className="material-symbols-outlined icon")


class Dropdown:
    def __init__(self) -> object:
        pass

    def render(self, id, options, droplabel, icons=None, title=None):
        optionstab = [
            # {
            #     'label': html.Span(
            #         [
            #             html.Span(id='', className='', children=droplabel),
            #         ]
            #     ),
            #     'value':options[0]
            # },
        ]
        if options is not None:
            for i in range(len(options)):
                optionstab.append(
                    {
                        "label": html.Span(
                            [
                                html.Span(id="", className="", children=options[i]),
                                renderIcon(icons, i),
                            ]
                        ),
                        "value": options[i],
                    }
                )

        return html.Div(
            [
                html.H6(title, className="mb-2"),
                dcc.Dropdown(
                    id=id,
                    options=optionstab,
                    value=options[0],
                ),
            ]
        )
