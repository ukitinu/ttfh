"""
Collection of interfaces common to graphics objects
"""


class Tickable:
    """ Interface for objects that can be updated (tick) """

    def tick(self) -> None:
        """ Updates the panel """
        pass


class Panel(Tickable):
    """ Interface for objects that can be drawn and updated on the window """

    def draw(self) -> None:
        """ Draws the panel """
        pass

    def tick(self) -> None:
        """ Updates the panel """
        pass
