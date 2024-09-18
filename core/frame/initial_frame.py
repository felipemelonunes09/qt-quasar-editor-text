from PySide6.QtWidgets import QFrame, QWidget, QHBoxLayout, QPushButton, QSizePolicy, QLabel
from core.shared.widgets.InitialButton import InitialButton

import config

    
class InitialFrame(QFrame):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1E2025;
            }
            
            QWidget#InitialButton {
                background-color: #29343D;
            }
            
        """)
        
        btn_open_file = InitialButton(img_path="./assets/img/icon/rocket-lunch.png", text="Open File")
        btn_open_file.setFixedSize(220, 240)
        btn_open_file.image_label.setContentsMargins(0, 0, 0, 30)
        btn_open_file.text_label.setContentsMargins(0, 0, 0, 50)
        btn_create_file = InitialButton(img_path="./assets/img/icon/file-edit-2.png", text="New File")
        btn_create_file.setFixedSize(220, 240)
        btn_create_file.image_label.setContentsMargins(0, 0, 0, 30)
        btn_create_file.text_label.setContentsMargins(0, 0, 0, 50)
        btn_open_project = InitialButton(img_path="./assets/img/icon/folder-tree-2.png", text="Open Project")
        btn_open_project.setFixedSize(220, 240)
        btn_open_project.image_label.setContentsMargins(0, 0, 0, 30)
        btn_open_project.text_label.setContentsMargins(0, 0, 0, 50)
        self.frame_layout = QHBoxLayout(self)
        self.frame_layout.addWidget(btn_open_file)
        self.frame_layout.addWidget(btn_create_file)
        self.frame_layout.addWidget(btn_open_project)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)