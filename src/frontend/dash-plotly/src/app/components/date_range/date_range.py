from dash import html, dcc


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
                html.Div(
                    dcc.DatePickerRange(
                        id=id,
                        start_date_placeholder_text="Date de début",
                        end_date_placeholder_text="Date de fin",
                        # className="dash-date-picker-range",
                    ),
                    # className="bg-danger",
                ),
            ],
        )
