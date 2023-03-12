# -*- coding: utf-8 -*-


class Constants():
    """All program constants are gathered.

    PV_VERSION: string -> plot view version as shown by git tag.
    WIN_RESIZABLE: boolean -> prevents the user from resizing the root window.
    WIN_SIZE_POS: string -> window size (width x height) and position relative
                              to top left corner.
    FONT_SIZE: integer -> size of font to be used for all widget texts.
    PLOT_WIDTH: float -> width (in) of matplotlib figure.
    PLOT_HEIGHT: float -> height (in) of matplotlib figure.
    MAX_STR_CREATE_CURVE: int -> number of characters. Depends on window width, font and font size.

    """

    def __init__(self):

        # APPLICATION
        # ============
        self.PV_VERSION = '1.9'
        # Window size should be OK for most cases. Window positioned at top left corner.
        self.WIN_SIZE_POS = '1280x780+0+0'
        # Minimum window size is required to allow all widgets to be displayed on RH panel.
        self.WIN_MIN_WIDTH = 800
        self.WIN_MIN_HEIGHT = 610

        # Number of decimals for rounding operation
        self.ROUND = 5

        # GUI APPEARANCE
        # ==============
        # For all PV widgets
        self.FONT_SIZE = 9

        # Size of matplotlib figure holding the plot.
        # The size of the figure needs to large to fill all the space on large screen.
        self.PLOT_WIDTH = 20
        self.PLOT_HEIGHT = 12

        # Parameters for widgets on RH tool panel.
        # Padding for all containers to uniformize the look
        # self.CONTAINER_PADX = 10
        # self.CONTAINER_PADY = 6.5
        # Padding for all widgets inside a container
        # self.WIDGET_PADX = 2.5
        # self.WIDGET_PADY = 2.5

        self.MAX_STR_CREATE_CURVE = 39
