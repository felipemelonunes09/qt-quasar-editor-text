from typing import Callable
from PySide6.QtCore import Qt, QFile, QFileInfo
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QFrame, QWidget, QHBoxLayout, QLabel, QPushButton

class FileTab(QFrame):
    def __init__(self, parent: QWidget, file: QFile, clickcallback: Callable) -> None:
        super().__init__(parent)
        self.__layout = QHBoxLayout(self)
        self.label = QLabel(QFileInfo(file).fileName())
        self.x_button = QPushButton("X")
        self.__file = file
        self.__layout.addWidget(self.label)
        self.__layout.addWidget(self.x_button)
        self.__clickcallback=clickcallback
        
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.__clickcallback(self.__file)
            self.set_active()
            self.style().polish(self)
        return super().mousePressEvent(event)
    
    def set_active(self) -> None:
        self.setObjectName("CurrentFileTab")
        self.label.setStyleSheet("color: white;")
        self.style().polish(self)
    
    def set_disable(self) -> None:
        self.setObjectName("FileTab")
        self.label.setStyleSheet("color: gray;")
        self.style().polish(self)
    
    def set_edited(self) -> None:
        self.label.setStyleSheet("color: lightgreen")
        
    def set_saved(self) -> None:
        self.label.setStyleSheet("color: white")