from kivy.app import App


def tr(key: str):
    """Translate a key through the running Kivy application."""

    return App.get_running_app().tr(key)
