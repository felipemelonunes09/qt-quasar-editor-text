from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QFrame
from core.shared.widgets.FileTab import FileTab
from PySide6.QtCore import Signal, Slot, QFile

class FileBar(QFrame):
    closing_current = Signal(QFile)
    tab_click       = Signal(QFile)
    bar_empty       = Signal()
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("FileBar")
        self.setFixedHeight(40)
        self.__tabs: dict[str, FileTab] = dict()
        self.__list: dict[str, QFile] = dict()
        self.__layout = QHBoxLayout(self)
        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.__layout.setSpacing(0)
        self.__layout.addStretch()
        self.__current_file: QFile = None
        self.__size: int = 0
        self.setLayout(self.__layout)
        self.update()
        
    def get_current_file(self) -> QFile:
        return self.__current_file
        
    def add_file(self, file: QFile, current=False) -> None:
        self.__remove_current_from_all()
        if not file.fileName() in self.__list: 
            tab = self.__create_tab(file)
            self.__tabs[file.fileName()] = tab
            self.__list[file.fileName()] = file
            self.__layout.addWidget(tab)
            self.__current_file = file if current else None
            tab.set_active() if current else tab.set_disable()
            self.__size += 1
        else:
            print("file is already on the list")
            ## create routine to set the current eddited path
            file = self.__list.get(file.fileName(), None)
            self.__tabs[file.fileName()].set_active()
            if current and file:
                self.__current_file = file
            
    def remove_file(self, file: QFile) -> None:
        if file.fileName() in self.__list:
            self.__tabs[file.fileName()].deleteLater() 
            self.__list[file.fileName()] = None
            del self.__tabs[file.fileName()]
            del self.__list[file.fileName()]
            self.__size -= 1
            if self.__size == 0:
                self.bar_empty.emit()
    
    def set_current_file_edited(self):
        if self.__current_file:
            print(f"(+) file {self.__current_file.fileName()} is edited")
            self.__current_file.set_edited(True)
            self.__tabs[self.__current_file.get_path()].set_edited()
    
    @Slot(QFile)
    def on_file_saved(self, file: QFile):
        file = self.__list.get(file.fileName(), None)
        if file:
            tab = self.__tabs.get(file.fileName(), None)
            if tab:
                tab.set_saved()
    
    def __remove_current_from_all(self):
        for tab_id in self.__tabs:
            self.__tabs[tab_id].set_disable()
    
    def __on_tab_close(self, file: QFile):
        self.remove_file(file)
        if self.__current_file:
            if file.fileName() == self.__current_file.fileName():
                next_id = next(iter(self.__list), None)
                next_file = self.__list.get(next_id, None)
                self.closing_current.emit(next_file)
                self.__current_file = self.__list.get(next_file)
        else:
            self.closing_current.emit(None)
            
    def __on_tab_click(self, file: QFile):
        self.tab_click.emit(file)
        self.__remove_current_from_all()
    
    def __create_tab(self, file: QFile) -> FileTab:
        tab = FileTab(self, file, clickcallback=self.__on_tab_click)
        tab.x_button.clicked.connect(lambda: self.__on_tab_close(file.readAll().data().decode("utf-8")))
        return tab
