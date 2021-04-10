# -*- coding: utf-8 -*-

"""PlotView reads a data file and plots the data curve using matplotlib.

    Code hosted at: https://github.com/fa201/PlotView
    PlotView is summarized as PV in variable names.
    It is the controller part in the Model View Controller pattern.
"""


from PlotView_GUI import Gui
from PlotView_model import Model


class Application:
    """ Define the controller."""
    def __init__(self):
        """ Instantiate the controller.

            Variables:
            - model: Model -> 1 instance to link to the PlotView_model file.
            - gui: GUI -> 1 instance to link to the PlotView_GUI file.
        """

        # The App instance is passed to the GUI instance to link both for call-backs.
        self.gui = Gui(self)
        self.model = Model(self)

    def create_curve(self, path):
        print('In controller - File path : ', path)
        self.model.create_curve(path)


if __name__ == '__main__':
    app = Application()
    # Launch the GUI mainloop which should always be the last instruction!
    app.gui.mainloop()
