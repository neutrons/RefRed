# third party imports
from qtpy.QtWidgets import QGroupBox, QHBoxLayout, QCheckBox, QPushButton


class DeadTimeEntryPoint(QGroupBox):
    def __init__(self, title='Dead Time Correction'):
        super().__init__(title)
        self.initUI()

    def initUI(self):
        # Set the stylesheet for the group box to have a border
        self.setStyleSheet(
            "QGroupBox {"
            "  border: 1px solid gray;"
            "  border-radius: 5px;"
            "  margin-top: 1ex;"  # space above the group box
            "} "
            "QGroupBox::title {"
            "  subcontrol-origin: margin;"
            "  subcontrol-position: top center;"  # align the title to the center
            "  padding: 0 3px;"
            "}"
        )

        self.applyCheckBox = QCheckBox('Apply', self)
        self.applyCheckBox.stateChanged.connect(self.toggleSettingsButton)
        self.settingsButton = QPushButton('Settings', self)
        self.settingsButton.setEnabled(self.applyCheckBox.isChecked())  # enabled if we use the correction

        # Create a horizontal layout for the checkbox and settings button
        hbox = QHBoxLayout()
        hbox.addWidget(self.applyCheckBox)
        hbox.addWidget(self.settingsButton)
        hbox.addStretch(1)  # This adds a stretchable space after the button (optional)

        # Set the layout for the group box
        self.setLayout(hbox)

    def toggleSettingsButton(self, state):
        # Enable the settings button if the checkbox is checked, disable otherwise
        self.settingsButton.setEnabled(state)
