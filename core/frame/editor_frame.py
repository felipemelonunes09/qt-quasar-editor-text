from PySide6.QtWidgets import QFrame, QPlainTextEdit, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QTextCursor, QTextCharFormat, QBrush, QColor
from core.shared.widgets.FileBar import FileBar
from core.file_handlers import FileLoader
from core.file_objects import File
from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QKeyEvent

class CustomPlainTextEdit(QPlainTextEdit):
    keyPressed = Signal() 
    def keyPressEvent(self, event: QKeyEvent):
        self.keyPressed.emit()
        super().keyPressEvent(event)

class EditorFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("EditorFrame")
        self.filebar = FileBar(self)
        self.filebar.closing_current.connect(self.__on_current_close)
        self.filebar.tab_click.connect(self.__on_tab_change)
        self.text_edit = CustomPlainTextEdit(self)
        self.text_edit.setContentsMargins(0, 0, 0, 0)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_edit.keyPressed.connect(self.__on_text_changed)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  
        layout.setSpacing(0) 
        layout.addWidget(self.filebar)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
        self.highlight_word("-var")
        
    def idle(self):
        self.text_edit.setDisabled(True)

    def highlight_word(self, word):
        cursor = self.text_edit.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat()) 
        highlight_format = QTextCharFormat()
        highlight_format.setForeground(QBrush(QColor("red"))) 
        cursor.setPosition(0)
        while not cursor.isNull() and not cursor.atEnd():
            cursor = self.text_edit.document().find(word, cursor)
            if not cursor.isNull():
                cursor.mergeCharFormat(highlight_format)
                
    def set_file(self, file: File) -> None:
        self.text_edit.setDisabled(False)
        self.filebar.add_file(file, current=True)
        file_loader = FileLoader(file)
        self.text_edit.setPlainText(file_loader.load())
        
    def set_blank_file(self) -> None:
        self.text_edit.setDisabled(False)
        self.filebar.add_file(File("Unknow", None), current=True)
        self.text_edit.setPlainText("")
        
    def get_current(self) -> tuple[str, File | None]:
        return self.text_edit.toPlainText(), self.filebar.get_current_file()
    
    
    @Slot()
    def __on_text_changed(self, *args, **kwargs):
        #self.highlight_word()
        self.filebar.set_current_file_edited()
        
    @Slot(File)
    def __on_current_close(self, next_file: File | None):
        if (next_file):
            file_loader = FileLoader(next_file)
            self.text_edit.setPlainText(file_loader.load())
        else:
            self.text_edit.setPlainText("")
            
    @Slot(File)
    def __on_tab_change(self, file):
        self.set_file(file)