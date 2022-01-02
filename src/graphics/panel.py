class Panel:
    """ Interface for objects that can be drawn on the window """

    def draw(self) -> None:
        """ Draws the panel """
        pass

    def tick(self) -> None:
        """ Updates the panel """
        pass
