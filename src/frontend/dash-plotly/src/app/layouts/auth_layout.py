from views.login.login_view import LoginView


class AuthLayout:
    def __init__(self) -> None:
        self.login_view = LoginView()

    def render(self):
        return self.login_view.render()
