from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

from PySide6.QtGui import QPixmap

class InitialButton(QWidget):
    def __init__(self, img_path, text: str):
        super().__init__()
        self.setObjectName("#InitialButton")
        self.background_label = QLabel()
        self.background_label.setObjectName("head-initial-button")
        self.setStyleSheet("background-color: #29343D;")
        self.image_label = QLabel()
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio,  Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("font-weight: bold;")
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.addWidget(self.background_label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.text_label)
        self.setLayout(layout)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.background_label.setStyleSheet(""" 
                border-top: 5px solid white; 
        """)  

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.background_label.setStyleSheet(""" 
                border-top: 0px;
        """)  
