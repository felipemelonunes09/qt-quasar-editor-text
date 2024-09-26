
from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout
from core.shared.widgets.FileBrowser import FileBrowserWidget
from PySide6.QtCore import Slot, Qt, Signal
from core.file_objects import File
import os


class AttributesFrame(QFrame):
    load_file = Signal(File)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("AttributesFrame")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.frame_layout = QVBoxLayout(self)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(0)
        self.file_browser = FileBrowserWidget()
        self.file_browser.file_tree.itemClicked.connect(self.atrribute_cliked)
        self.frame_layout.addWidget(self.file_browser)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def set_working_dir(self, path: str) -> None:
        self.file_browser.set_current_path(path)
        
    @Slot()
    def atrribute_cliked(self, item) -> None:
        data = item.data(0, Qt.UserRole)
        if data:
            path, filename = data
            path = os.path.join(path, filename)
            file = File(filename, path)
            self.load_file.emit(file)