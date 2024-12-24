from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Signal
from core.shared.widgets.InitialButton import InitialButton
import config

    
class InitialFrame(QFrame):
    
    open_file       = Signal()
    open_project    = Signal()
    create_file     = Signal()
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("InitialFrame") 
        self.__layout = QVBoxLayout(self)
        self.__btn_layout = QHBoxLayout()
        btn_open_file = InitialButton(img_path=config.icon_path_rocket_lunch, text="Open File", signal=self.open_file)
        btn_open_file.setFixedSize(220, 240)
        btn_open_file.image_label.setContentsMargins(0, 0, 0, 30)
        btn_open_file.text_label.setContentsMargins(0, 0, 0, 50)
        btn_create_file = InitialButton(img_path=config.icon_path_file_edit, text="New File", signal=self.create_file)
        btn_create_file.setFixedSize(220, 240)
        btn_create_file.image_label.setContentsMargins(0, 0, 0, 30)
        btn_create_file.text_label.setContentsMargins(0, 0, 0, 50)
        btn_open_project = InitialButton(img_path=config.icon_path_folder_tree, text="Open Project", signal=self.open_project)
        btn_open_project.setFixedSize(220, 240)
        btn_open_project.image_label.setContentsMargins(0, 0, 0, 30)
        btn_open_project.text_label.setContentsMargins(0, 0, 0, 50)
        self.frame_layout = QHBoxLayout(self)
        self.__btn_layout.addWidget(btn_open_file)
        self.__btn_layout.addWidget(btn_create_file)
        self.__btn_layout.addWidget(btn_open_project)
        
        self.__layout.addLayout(self.__btn_layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
