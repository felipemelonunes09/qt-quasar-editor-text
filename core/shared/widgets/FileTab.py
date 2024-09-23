from typing import Callable
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from core.file_objects import File
from PySide6.QtWidgets import QFrame, QWidget, QHBoxLayout, QLabel, QPushButton

class FileTab(QFrame):
    def __init__(self, parent: QWidget, file: File, clickcallback: Callable) -> None:
        super().__init__(parent)
        self.__layout = QHBoxLayout(self)
        self.label = QLabel(file.get_name())
        self.x_button = QPushButton("X")
        self.__file = file
        self.__layout.addWidget(self.label)
        self.__layout.addWidget(self.x_button)
        self.__clickcallback=clickcallback
        
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.__clickcallback(self.__file)
            self.setObjectName("CurrentFileTab")
            self.style().polish(self)
        return super().mousePressEvent(event)