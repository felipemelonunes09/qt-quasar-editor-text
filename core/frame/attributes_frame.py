from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel, QSizePolicy

class AttributesFrame(QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName(AttributesFrame.__name__)
        self.setStyleSheet(f"background-color: red")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        
        self.frame_layout = QVBoxLayout(self)
        label1 = QLabel("Label dentro do Frame 1")
        self.frame_layout.addWidget(label1)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
