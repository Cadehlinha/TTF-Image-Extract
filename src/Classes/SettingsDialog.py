from Classes.Common import *



class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")

        layout = QtWidgets.QVBoxLayout()

        # Character List
        character_label = QtWidgets.QLabel("Character List:")
        self.character_edit = QtWidgets.QLineEdit()
        layout.addWidget(character_label)
        layout.addWidget(self.character_edit)

        # Font Size
        size_label = QtWidgets.QLabel("Font Size:")
        self.size_spinbox = QtWidgets.QSpinBox()
        layout.addWidget(size_label)
        layout.addWidget(self.size_spinbox)

        # Background Color
        bg_color_label = QtWidgets.QLabel("Background Color:")
        self.bg_color_button = QtWidgets.QPushButton()
        self.bg_color_button.clicked.connect(self.pick_bg_color)
        layout.addWidget(bg_color_label)
        layout.addWidget(self.bg_color_button)

        # Font Color
        font_color_label = QtWidgets.QLabel("Font Color:")
        self.font_color_button = QtWidgets.QPushButton()
        self.font_color_button.clicked.connect(self.pick_font_color)
        layout.addWidget(font_color_label)
        layout.addWidget(self.font_color_button)

        # Save and Cancel Buttons
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)


    def pick_bg_color(self):
        dialog = ColorPickerDialog(self)
        dialog.accepted.connect(lambda: self.handle_color_accepted(self.bg_color_button))
        dialog.exec_()


    def pick_font_color(self):
        dialog = ColorPickerDialog(self)
        dialog.accepted.connect(lambda: self.handle_color_accepted(self.font_color_button))
        dialog.exec_()


    @QtCore.pyqtSlot()
    def handle_color_accepted(self, button):
        dialog = self.sender()
        button.setStyleSheet(f"background-color: {dialog.get_color()};")
        #print(dialog.get_color())