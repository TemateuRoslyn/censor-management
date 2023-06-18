from dash import dcc

class GraphFigure:
    def __init__(self) -> None:
        pass

    def render(self):
        return dcc.Graph(
            figure={
                'data':[
                    {'x':[1,2,3],'y':[4,1,2], 'type':'bar','name':'SF'},
                    {'x':[2,4,6],'y':[13,19,28], 'type':'bar','name':'MontReal'}
                ],
                'layout':{
                    'title':'A graph'
                }
            }
        )