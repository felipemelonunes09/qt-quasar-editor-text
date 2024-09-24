from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QAction
from PySide6.QtCore import QObject, Signal

class MenuManager(QObject):
    
    split = Signal()
    
    def __init__(self, parent: QMainWindow) -> None:
        self.menu_bar = parent.menuBar()
        self.setup_menus()
        super().__init__()
        
    def setup_menus(self):
        self.file_menu = self.menu_bar.addMenu("Window")
        self.file_menu.addAction(self.create_action("Split editor", self.split.emit))
    
    def create_action(self, name, callback):
        action = QAction(name, self.menu_bar)
        action.triggered.connect(callback)
        return action