from dash import html, dcc
from datetime import datetime


class DateRange:
    def __init__(self) -> None:
        pass

    def render(self, id: str, label=None):
        return html.Div(
            [
                html.H6(
                    label,
                    className="mb-2",
                ),
                dcc.DatePickerRange(
                    id=id,
                    start_date=datetime.today(),
                    end_date_placeholder_text="Selectionez une date de fin!",
                ),
            ],
            className="w-100",
        )
