from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QWidget, QHBoxLayout, QLabel, QPushButton

class FileTab(QFrame):
    def __init__(self, parent: QWidget, name: str) -> None:
        super().__init__(parent)
        self.__layout = QHBoxLayout(self)
        self.label = QLabel(name)
        self.x_button = QPushButton("X")
        self.__layout.addWidget(self.label)
        self.__layout.addWidget(self.x_button)