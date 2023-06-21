# from dash import html
# # import dash_bootstrap_components as dbc
# import dash_bootstrap_components as dbc

# class ModalComponent:
#     def __init__(self) -> None:
#         pass

#     def render(self):
#         return html.Div(
#             [
#                 dbc.Button("Open modal", id="open-dismiss"),
#                 dbc.Modal(
#                     [
#                         dbc.ModalHeader(
#                             dbc.ModalTitle("Dismissing"), close_button=False
#                         ),
#                         dbc.ModalBody(
#                             "This modal has no close button and can't be dismissed by "
#                             "pressing ESC. Try clicking on the backdrop or the below "
#                             "close button."
#                         ),
#                         dbc.ModalFooter(dbc.Button("Close", id="close-dismiss")),
#                     ],
#                     id="modal-dismiss",
#                     keyboard=False,
#                     backdrop="static",
#                 ),
#             ],
#         )
