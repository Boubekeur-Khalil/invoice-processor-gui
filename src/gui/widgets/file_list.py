from PyQt5.QtWidgets import QListWidget, QListWidgetItem

class FileListWidget(QListWidget):
    """A widget for displaying and selecting files for processing."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionMode(QListWidget.MultiSelection)

    def add_file(self, file_name: str):
        """Add a file to the list."""
        item = QListWidgetItem(file_name)
        self.addItem(item)

    def get_selected_files(self):
        """Return a list of selected files."""
        return [item.text() for item in self.selectedItems()]

    def clear_files(self):
        """Clear the file list."""
        self.clear()