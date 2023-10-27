from Classes.Common import *



class CharacterExtractorGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.font_path = None
        self.desired_characters = "!@#$%^&*()0123456789          ABCDEFGHIJKLMNOPQRSTUVWXYZ              abcdefghijklmnopqrstuvwxyz"
        self.point_size = 64
        self.background_color = "rgba(0, 0, 0, 0)"  # Hex color code with alpha channel
        self.font_color = "rgba(0, 0, 0, 255)"

        self.init_ui()


    def init_ui(self):
        self.setWindowTitle("Character Extractor")
        self.create_menu()
        self.setFixedSize(500, 500)

        layout = QtWidgets.QVBoxLayout()

        # Create a scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create a widget to hold the extracted character images
        content_widget = QtWidgets.QWidget()
        scroll_area.setWidget(content_widget)

        # Create a grid layout for the content widget
        self.content_layout = QtWidgets.QGridLayout()
        content_widget.setLayout(self.content_layout)

        # Add the scroll area to the main layout
        layout.addWidget(scroll_area)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.show()


    def create_menu(self):
        menubar = self.menuBar()
        # File Menu
        file_menu = menubar.addMenu("File")
        # Open Font Action
        open_action = QtWidgets.QAction("Open Font", self)
        open_action.triggered.connect(self.font_dialog)
        file_menu.addAction(open_action)
        # Batch Export Action
        batch_export_action = QtWidgets.QAction("Batch Export", self)
        batch_export_action.triggered.connect(self.batch_export_dialog)
        file_menu.addAction(batch_export_action)
        # Exit Action
        exit_action = QtWidgets.QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit Menu
        options_menu = menubar.addMenu("Edit")
        # Preferences Action
        settings_action = QtWidgets.QAction("Preferences", self)
        settings_action.triggered.connect(self.settings_dialog)
        options_menu.addAction(settings_action)


    def clear_grid(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()


    def fill_grid(self):
        # Create an instance of the CharacterExtractor class
        extractor = CharacterExtractor(self.font_path, self.desired_characters,
                                       self.point_size, self.background_color, self.font_color)

        # Extract characters and add them to the GUI
        num_columns = 10  # Number of columns for the grid layout
        for i, char in enumerate(self.desired_characters):
            image = extractor.extract_characters(char)

            # Convert the PIL image to QPixmap
            qimage = QtGui.QImage(extractor.final_image.tobytes("raw", "RGBA"), extractor.final_image.size[0],
                            extractor.final_image.size[1], QtGui.QImage.Format_RGBA8888)
            pixmap = QtGui.QPixmap.fromImage(qimage)

            # Create a QLabel to display the image
            label = QtWidgets.QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(QtCore.Qt.AlignCenter)

            # Create a separate instance of QMenu for each label
            context_menu = QtWidgets.QMenu(self)

            if char != " ":
                action1 = QtWidgets.QAction(f"Save '{char}' as PNG", self)
                action1.triggered.connect(lambda checked, char=extractor.final_image: self.action_press(char))
                context_menu.addAction(action1)
                label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

            # Connect the context menu to a lambda function to capture the label instance
            label.customContextMenuRequested.connect(
                lambda pos, label=label, context_menu=context_menu: self.context_menu(pos, label, context_menu)
            )

            # Calculate the row and column for the current label
            row = i // num_columns
            col = i % num_columns

            # Add the label to the content layout at the specified row and column
            self.content_layout.addWidget(label, row, col)


    def context_menu(self, position, label, context_menu):
        # Get the global position of the click event and spawn
        global_position = label.mapToGlobal(position)
        context_menu.exec_(global_position)


    def action_press(self, char):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix("png")
        file_path, _ = file_dialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png)")

        if file_path:
            if not file_path.endswith(".png"):  # Check if the file path has an extension
                file_path += ".png"  # Append the default extension if necessary
            char.save(file_path)


    def font_dialog(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file_path, _ = file_dialog.getOpenFileName(self, "Open Font", "", "Font Files (*.ttf)")

        if file_path:
            self.font_path = file_path
            self.clear_grid()
            self.fill_grid()


    def batch_export_dialog(self):
        if self.font_path == None:
            QtWidgets.QMessageBox.critical(self, "Error", f"Nothing to export! No font loaded")
            return

        directory_dialog = QtWidgets.QFileDialog()
        directory_dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        directory_path = directory_dialog.getExistingDirectory(self, "Select Directory for Batch Export")

        if directory_path:
            extractor = CharacterExtractor(self.font_path, self.desired_characters,
                                           self.point_size, self.background_color, self.font_color)

            for i, char in enumerate(self.desired_characters):
                image = extractor.extract_characters(char)
                file_path = os.path.join(directory_path, f"image_{i}.png")

                try:
                    if char != " ":
                        image.save(file_path, "PNG")
                except Exception as e:
                    #print(f"An error occurred while saving '{char}': {str(e)}")
                    pass

            QtWidgets.QMessageBox.information(self, "Batch Export", "Batch export completed successfully.")


    def settings_dialog(self):
        dialog = SettingsWindow(self)
        dialog.character_edit.setText(self.desired_characters)
        dialog.size_spinbox.setValue(self.point_size)
        dialog.bg_color_button.setStyleSheet(f"background-color: {self.background_color};")
        dialog.font_color_button.setStyleSheet(f"background-color: {self.font_color};")

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.desired_characters = dialog.character_edit.text()
            self.point_size = dialog.size_spinbox.value()

            # really annoying way to do this, but it works.
            # trying to use the .name() object of the color() class will
            # refuse to return the alpha channel which means it won't support
            # transparency. I want transparency to be an option though, so...
            # fuck it, we ball >:3
            background_obj = dialog.bg_color_button.palette().button().color()
            font_obj = dialog.font_color_button.palette().button().color()
            self.background_color = f"rgba({background_obj.red()}, {background_obj.green()}, {background_obj.blue()}, {background_obj.alpha()})"
            self.font_color = f"rgba({font_obj.red()}, {font_obj.green()}, {font_obj.blue()}, {font_obj.alpha()})"
            
            # do Try: Except: just so it wont break if settings are changed
            # before the font is loaded
            try:
                self.clear_grid()
                self.fill_grid()
            except:
                pass



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CharacterExtractorGUI()
    sys.exit(app.exec_())