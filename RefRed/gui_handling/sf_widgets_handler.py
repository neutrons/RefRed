class SfWidgetsHandler(object):
    '''
    button can take the following values
    'calculated'
    'auto'
    'manual'
    '''
    button = 'calculated'

    def __init__(self, parent=None, button='calculated'):
        self.parent = parent
        self.button = button

        self.set_widgets()

    def set_widgets(self):
        first_angle_visible_for = ['calculated', 'auto']
        if self.button in first_angle_visible_for:
            enable_group = True
        else:
            enable_group = False

        self.parent.ui.first_angle_groupbox.setEnabled(enable_group)
