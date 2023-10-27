from Classes.Common import *



class ColorPickerDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Color Picker")
        self.setModal(True)

        self.color = QtGui.QColor(0, 0, 0)  # Default color (black)

        self.slider_r = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_g = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_b = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_a = QtWidgets.QSlider(QtCore.Qt.Horizontal)

        self.slider_r.setRange(0, 255)
        self.slider_g.setRange(0, 255)
        self.slider_b.setRange(0, 255)
        self.slider_a.setRange(0, 255)

        self.slider_a.setValue(255)

        self.slider_r.valueChanged.connect(self.update_color)
        self.slider_g.valueChanged.connect(self.update_color)
        self.slider_b.valueChanged.connect(self.update_color)
        self.slider_a.valueChanged.connect(self.update_color)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("Red"), 0, 0)
        layout.addWidget(self.slider_r, 0, 1)
        layout.addWidget(QtWidgets.QLabel("Green"), 1, 0)
        layout.addWidget(self.slider_g, 1, 1)
        layout.addWidget(QtWidgets.QLabel("Blue"), 2, 0)
        layout.addWidget(self.slider_b, 2, 1)
        layout.addWidget(QtWidgets.QLabel("Alpha"), 3, 0)
        layout.addWidget(self.slider_a, 3, 1)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(layout)

        self.label_color = QtWidgets.QLabel()
        self.label_color.setMinimumHeight(120)  # Set a minimum height

        vbox.addWidget(self.label_color)

        # Line edit for hex color code
        self.lineedit_hex = QtWidgets.QLineEdit()
        self.lineedit_hex.setReadOnly(True)
        self.lineedit_hex.setText(self.get_color())

        # Button to close dialog
        self.close_button = QtWidgets.QPushButton("Accept")
        self.close_button.clicked.connect(self.accept)

        vbox.addWidget(QtWidgets.QLabel("RGBA Value:"))
        vbox.addWidget(self.lineedit_hex)
        vbox.addWidget(self.close_button)

        self.setLayout(vbox)


    def update_color(self):
        red = self.slider_r.value()
        green = self.slider_g.value()
        blue = self.slider_b.value()
        alpha = self.slider_a.value()
        self.color = QtGui.QColor(red, green, blue, alpha)
        self.update_color_preview()
        self.lineedit_hex.setText(self.get_color())


    def update_color_preview(self):
        pixmap = QtGui.QPixmap(self.label_color.size())
        pixmap.fill(self.color)
        painter = QtGui.QPainter(pixmap)
        painter.fillRect(pixmap.rect(), self.color)
        painter.end()
        self.label_color.setPixmap(pixmap)


    def resizeEvent(self, event):
        self.update_color_preview()


    def get_color(self):
        return 'rgba({}, {}, {}, {})'.format(self.color.red(), self.color.green(), self.color.blue(), self.color.alpha())