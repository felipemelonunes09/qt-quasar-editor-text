import sys
import config
from PySide6.QtCore import Slot, Signal, QFile, QDir
from PySide6.QtWidgets import QApplication, QVBoxLayout, QSplitter, QWidget, QMainWindow
from PySide6.QtGui import QShortcut, QKeySequence
from core.frame.attributes_frame import AttributesFrame
from core.frame.initial_frame import InitialFrame
from core.Editor import Editor
from core.MenuManager import MenuManager
from core.frame.area_editor_frame import AreaEditorFrame    
from theme.ThemeManager import ThemeManager


class MainWindow(QMainWindow): 
    file_saved = Signal(QFile)
    def __init__(self):
        super().__init__()
        self.__central_widget = QWidget(self)
        self.__editor = Editor()
        self.__splitter = QSplitter(self)
        self.__theme_manager = ThemeManager(config.pallete_path, config.theme)
        self.__attributes_frame = AttributesFrame(self.__splitter)
        self.__initial_frame = InitialFrame(self.__splitter)
        self.__editor_area = AreaEditorFrame(self.__splitter)
        self.__layout = QVBoxLayout(self.__central_widget)
        self.__menu = MenuManager(self)
        self.setup_initial()
        
    def setup_initial(self):
        self.__attributes_frame.load_file.connect(self.__on_file_load)
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
        self.__splitter.addWidget(self.__editor_area)
        self.__splitter.setSizes(config.splitter_size)
        self.__splitter.hide()
        self.__save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.__save_shortcut.activated.connect(self.__save_file)
        self.__editor_area.file_edited.connect(self.__on_file_edited)
        self.file_saved.connect(self.__editor_area.update_file_saved)
        self.setCentralWidget(self.__central_widget)
        
    @Slot(QFile)
    def __on_file_load(self, file: QFile) -> None:
        print(file.fileName())
        self.__editor_area.get_current_editor().set_file(file)
    @Slot()
    def __save_file(self, *a, **K) -> None:
        content, file = self.__editor_area.get_current_editor().get_current()
        self.__editor.save_file(file, content)
        self.__on_file_saved(file)
        self.file_saved.emit(file)
        
    
    @Slot()
    def __open_file(self, *a, **k) -> None:
        file = self.__editor.open_file_dialog() 
        if file:
            self.__initial_frame.hide()
            self.__attributes_frame.hide()
            self.__splitter.show()
            self.__editor_area.get_current_editor().set_file(file)     
    @Slot()
    def __create_file(self, *a, **k) -> None:
        self.__initial_frame.hide()
        self.__attributes_frame.hide()
        self.__editor_area.get_current_editor().show()
        self.__editor_area.get_current_editor().set_blank_file()
        self.__splitter.show()
        
    @Slot()
    def __open_project(self, *a, **k) -> None:
        dir_path = self.__editor.open_dir_dialog()
        self.__initial_frame.hide()
        self.__attributes_frame.show()
        self.__editor_area.get_current_editor().show()
        self.__editor_area.get_current_editor().idle()
        self.__attributes_frame.set_working_dir(dir_path)
        self.__splitter.show()
    
    @Slot()
    def __on_file_edited(self, file: QFile) -> None:
        self.__attributes_frame.change_item_color(file, "lightgreen")

    @Slot()
    def __on_file_saved(self, file: QFile) -> None:
        self.__attributes_frame.change_item_color(file, "white")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Quasar Editor")
    window.resize(1024, 768)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()