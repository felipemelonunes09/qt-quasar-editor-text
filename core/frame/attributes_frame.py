
from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QLabel
from core.frame.editor_frame import EditorFrame
from core.shared.widgets.FileBrowser import FileBrowserWidget
from PySide6.QtCore import Slot, Qt, Signal, QFile
import os

class AttributesFrame(QFrame):
    load_file = Signal(QFile)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("AttributesFrame")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.file_browser = FileBrowserWidget()
        self.file_browser.itemClicked.connect(self.atrribute_cliked)
        self.path_label = QLabel("")
        self.path_label.setContentsMargins(0,0,0,10)
        self.__layout = QVBoxLayout(self)
        self.__layout.setContentsMargins(20, 20, 0, 0)
        self.__layout.setSpacing(0)
        self.__layout.addWidget(self.path_label)
        self.__layout.addWidget(self.file_browser)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def set_working_dir(self, path: str) -> None:
        self.path_label.setText(f"<b>{(path if path else os.getcwd()).split("/")[-1].upper()}</b>")
        self.file_browser.set_current_path(path)
        
    @Slot()
    def atrribute_cliked(self, item) -> None:
        data = item.data(0, Qt.UserRole)
        if data:
            path, filename = data
            path = os.path.join(path, filename)
            file = QFile(path)
            self.load_file.emit(file)

    def change_item_color(self, path: str, color: str) -> None:
        print(path)
        print(self.file_browser.mapper)