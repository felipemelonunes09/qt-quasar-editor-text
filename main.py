import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Slot
from PySide6.QtGui import QShortcut, QKeySequence
from core.frame.editor_frame import EditorFrame
from core.frame.attributes_frame import AttributesFrame
from core.frame.initial_frame import InitialFrame
from core.Editor import Editor
from theme.ThemeManager import ThemeManager

import config

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.__editor = Editor()
        self.__theme_manager = ThemeManager(config.pallete_path)
        self.__attributes_frame= AttributesFrame(self)
        self.__editor_frame = EditorFrame(self)
        self.__initial_frame = InitialFrame(self)
        self.__splitter = QSplitter(self)
        
        self.__splitter.addWidget(self.__attributes_frame)
        self.__splitter.addWidget(self.__editor_frame)
        
        self.__splitter.setSizes(config.splitter_size)
        
        self.__layout = QVBoxLayout(self)
        self.__layout.addWidget(self.__splitter)
        self.__layout.addWidget(self.__initial_frame)
        
        self.setup_initial()
    
    def setup_initial(self):
        self.__editor_frame.setContentsMargins(0, 0, 0, 0)
        self.__splitter.setContentsMargins(0, 0, 0, 0)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)
        self.__editor
        
        self.__initial_frame.open_file.connect(self.open_file)
        self.__initial_frame.open_project.connect(self.open_project)
        self.__initial_frame.create_file.connect(self.create_file)
        self.__theme_manager.apply_theme(config.theme, self)
        self.__splitter.hide()
        
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save_file)
        
    @Slot()
    def save_file(self, *a, **K) -> None:
        content, file = self.__editor_frame.get_current()
        self.__editor.save_file(file, content)
        
    @Slot()
    def open_file(self, *a, **k) -> None:
        file = self.__editor.open_file_dialog() 
        if(file):
            self.__initial_frame.hide()
            self.__attributes_frame.hide()
            self.__editor_frame.show()
            self.__splitter.show()
            self.__editor_frame.set_file(file)     
    @Slot()
    def create_file(self, *a, **k):
        self.__initial_frame.hide()
        self.__attributes_frame.hide()
        self.__editor_frame.show()
        self.__splitter.show()
        self.__editor_frame.set_blank_file()
        
    @Slot()
    def open_project(self, *a, **k):
        dir_path = self.__editor.open_dir_dialog()
        self.__initial_frame.hide()
        self.__attributes_frame.show()
        self.__editor_frame.show()
        self.__editor_frame.idle()
        self.__splitter.show()
        self.__attributes_frame.set_working_dir(dir_path)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("<-> Quasar <->")
    window.resize(1024, 768)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
