import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSplitter
from core.frame.editor_frame import EditorFrame
from core.frame.attributes_frame import AttributesFrame
from core.frame.initial_frame import InitialFrame
from PySide6.QtCore import Slot
from core.Editor import Editor
from theme.ThemeManager import ThemeManager

import config

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.__editor = Editor()
        self.__theme_manager = ThemeManager(config.pallete_path)
        self.__left_frame = EditorFrame(self)
        self.__right_frame = AttributesFrame(self)
        self.__initial_frame = InitialFrame(self)
        self.__splitter = QSplitter(self)
        
        self.__splitter.addWidget(self.__left_frame)
        self.__splitter.addWidget(self.__right_frame)
        
        self.__splitter.setSizes(config.splitter_size)
        
        self.__layout = QVBoxLayout(self)
        self.__layout.addWidget(self.__splitter)
        self.__layout.addWidget(self.__initial_frame)
        
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)
        
        self.setup_initial()
    
    def setup_initial(self):
        self.__initial_frame.open_file.connect(self.open_file)
        self.__initial_frame.open_project.connect(self.open_project)
        self.__initial_frame.create_file.connect(self.create_file)
        self.__theme_manager.apply_theme(config.theme, self)
        self.__splitter.hide()
        
    @Slot()
    def open_file(*a, **k):
        print("Opening file")
        
    @Slot()
    def create_file(*a, **k):
        print("creating file")
        
    @Slot()
    def open_project(*a, **k):
        print("Opening project")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Exemplo de Frame no Qt")
    window.resize(1024, 768)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
