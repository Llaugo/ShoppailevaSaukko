from kivy.uix.image import Image


STONE_ART_SIZE = (10, 10)


class NavigationStone(Image):
    """A non-solid room marker dropped by the Gratitude card."""

    artSize = STONE_ART_SIZE

    def __init__(self, **kwargs):
        kwargs.setdefault("source", "images/stone.png")
        kwargs.setdefault("size_hint", (None, None))
        kwargs.setdefault("fit_mode", "contain")
        super().__init__(**kwargs)
