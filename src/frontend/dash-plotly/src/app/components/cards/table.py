from dash import html, dcc
import dash_bootstrap_components as dbc
from components.modal.modal_full import ModalFull


class TableCard:
    def __init__(self) -> None:
        pass

    def render(self, icon, title, content, id):
        return html.Div(id='', className='solution_card', children=[
            html.Div(id='', className='hover_color_bubble', children=[]),
            html.Span(id='', className='d-flex', children=[
                html.Div(id='', className='so_top_icon', children=[
                    html.Span(id='', className='material-symbols-outlined icon', children=[icon])
                ]),
                html.Div(id='', className='solu_title', children=[
                    html.H3(id='', className='fs-4 ms-2', children=title)
                ]),
            ]),
            html.Div(id='', className='solu_description', children=[
                content,
                dbc.Button(id='show-full-'+id, className='btn btn-secondary', children=[
                    "Voir +"
                ],n_clicks=0)
            ]),
            ModalFull().render()
        ])
