from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel

class EditorFrame(QFrame):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.frame_layout = QVBoxLayout(self)
        self.setStyleSheet(f"background-color: blue")
        label1 = QLabel("Label dentro do Frame 2")
        self.frame_layout.addWidget(label1)