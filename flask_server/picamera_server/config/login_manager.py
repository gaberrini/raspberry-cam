from flask_login import LoginManager


def init_login_manager(manager: LoginManager) -> LoginManager:
    manager.login_view = "users.user_login"
    return manager
