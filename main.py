import sys
from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QApplication, QVBoxLayout, QSplitter, QWidget, QMainWindow
from PySide6.QtGui import QShortcut, QKeySequence
from core.frame.editor_frame import EditorFrame
from core.frame.attributes_frame import AttributesFrame
from core.frame.initial_frame import InitialFrame
from theme.ThemeManager import ThemeManager
from core.Editor import Editor
from core.file_objects import File
from core.MenuManager import MenuManager
from core.frame.area_editor_frame import AreaEditorFrame
    
import config

class MainWindow(QMainWindow): 
    file_saved = Signal(File)
    def __init__(self):
        super().__init__()
        self.__central_widget = QWidget(self)
        self.__editor = Editor()
        self.__theme_manager = ThemeManager(config.pallete_path)
        self.__attributes_frame= AttributesFrame(self)
        self.__current_editor = EditorFrame(self)
        self.__editor_frames: list[EditorFrame] = [self.__current_editor]
        self.__initial_frame = InitialFrame(self)
        self.__splitter = QSplitter(self)
        self.__layout = QVBoxLayout(self.__central_widget)
        self.__menu = MenuManager(self)
        self.setup_initial()
        
    def setup_initial(self):
        self.__current_editor.setContentsMargins(0, 0, 0, 0)
        self.__attributes_frame.load_file.connect(self.__current_editor.set_file)
        self.__splitter.setContentsMargins(0, 0, 0, 0)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)
        self.__layout.addWidget(self.__splitter)
        self.__layout.addWidget(self.__initial_frame)
        self.__initial_frame.open_file.connect(self.__open_file)
        self.__initial_frame.open_project.connect(self.__open_project)
        self.__initial_frame.create_file.connect(self.__create_file)
        self.__theme_manager.apply_theme(config.theme, self)
        self.__splitter.addWidget(self.__attributes_frame)
        self.__splitter.addWidget(self.__current_editor)
        self.__splitter.setSizes(config.splitter_size)
        self.__splitter.hide()
        self.__save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.__save_shortcut.activated.connect(self.__save_file)
        self.__menu.split.connect(self.__split_editor)
        self.file_saved.connect(self.__current_editor.filebar.on_file_saved)
        self.setCentralWidget(self.__central_widget)
        
    @Slot()
    def __save_file(self, *a, **K) -> None:
        content, file = self.__current_editor.get_current()
        self.__editor.save_file(file, content)
        self.file_saved.emit(file)
        
    @Slot()
    def __open_file(self, *a, **k) -> None:
        file = self.__editor.open_file_dialog() 
        if file:
            self.__initial_frame.hide()
            self.__attributes_frame.hide()
            self.__current_editor.show()
            self.__splitter.show()
            self.__current_editor.set_file(file)     
            
    @Slot()
    def __create_file(self, *a, **k) -> None:
        self.__initial_frame.hide()
        self.__attributes_frame.hide()
        self.__current_editor.show()
        self.__splitter.show()
        self.__current_editor.set_blank_file()
        
    @Slot()
    def __open_project(self, *a, **k) -> None:
        dir_path = self.__editor.open_dir_dialog()
        self.__initial_frame.hide()
        self.__attributes_frame.show()
        self.__current_editor.show()
        self.__current_editor.idle()
        self.__splitter.show()
        self.__attributes_frame.set_working_dir(dir_path)
        
    @Slot(EditorFrame)
    def __on_editor_change(self, editor: EditorFrame):
        print("changed")
        self.__current_editor = editor
        
    def __split_editor(self) -> None:
        if not self.__splitter.isHidden():
            new_editor = self.__create_editor()
            self.__editor_frames.append(new_editor)
            self.__current_editor = new_editor
            self.__splitter.addWidget(new_editor)
    
    def __create_editor(self) -> EditorFrame:
        new_editor = EditorFrame(self)
        new_editor.setContentsMargins(0,0,0,0)
        new_editor.clicked.connect(self.__on_editor_change)   
        return new_editor     
    
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("<-> Quasar <->")
    window.resize(1024, 768)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()