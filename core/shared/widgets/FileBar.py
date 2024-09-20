from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy
from core.file_objects import File
from PySide6.QtCore import Signal

class FileBar(QFrame):
    closing_current = Signal(File)
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("FileBar")
        self.setFixedHeight(40)
        self.__list: set[File] = set()
        self.__tabs: dict[QFrame] = dict()
        self.__layout = QHBoxLayout(self)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)
        self.__layout.addStretch()
        self.__current_file: File = None
        self.setLayout(self.__layout)
        self.update()
        
    def get_current_file(self) -> File:
        return self.__current_file
        
    def addFile(self, file: File, current=False) -> None:
        if not file in self.__list:
            tab = self.__create_tab(file)
            self.__tabs[file] = tab
            self.__layout.addWidget(tab)
            self.__list.add(file)
            self.__current_file = file if current else None
            tab.setObjectName("CurrentFileTab") if current else tab.setObjectName("FileTab")

    def removeFile(self, file: File) -> None:
        if file in self.__list:
            self.__tabs[file].deleteLater() 
            del self.__tabs[file]
            self.__list.remove(file)
    
    def set_current_file_edited(self):
        if self.__current_file:
            self.__current_file.set_edited(True)
            self.__tabs[self.__current_file].setStyleSheet("QLabel { color: lightgreen; }")
    
    def __on_tab_close(self, file: File):
        self.removeFile(file)
        if file == self.__current_file:
            next_file = next(iter(self.__list), None)
            self.closing_current.emit(next_file)
            self.__current_file = next_file
    
    def __create_tab(self, file: File) -> QFrame:
        tab = QFrame()
        tab_layout = QHBoxLayout()
        label = QLabel(file.get_name())
        x_button = QPushButton("X")
        x_button.clicked.connect(lambda: self.__on_tab_close(file))
        tab_layout.addWidget(label)
        tab_layout.addWidget(x_button)
        tab.setLayout(tab_layout)
        return tab
