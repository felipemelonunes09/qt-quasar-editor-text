from PySide6.QtWidgets import QFrame, QPlainTextEdit, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent, QDropEvent, QMouseEvent, QTextCursor, QTextCharFormat, QBrush, QColor
from core.shared.widgets.FileBar import FileBar
from core.file_handlers import FileLoader
from core.file_objects import File
from PySide6.QtCore import Signal, Slot, Qt
from PySide6.QtGui import QKeyEvent

class EditorFrame(QFrame):
    clicked = Signal(QFrame)
    class CustomPlainTextEdit(QPlainTextEdit):
        key_pressed = Signal() 
        cliked = Signal()
        def __init__(self, parent):
            super().__init__(parent)
            self.setAcceptDrops(True)
        
        def keyPressEvent(self, event: QKeyEvent):
            self.key_pressed.emit()
            if event.key() == Qt.Key_Tab:
                self.insertPlainText(' '*4)
            super().keyPressEvent(event)
        def mousePressEvent(self, e: QMouseEvent) -> None:
            self.cliked.emit()
            return super().mousePressEvent(e)
        
        def dragEnterEvent(self, e: QDragEnterEvent) -> None:
            self.setObjectName("QPlainTextEditDragEnterCenter")
            self.style().polish(self)
            e.acceptProposedAction()
        
        def dragMoveEvent(self, e: QDragMoveEvent) -> None:
            print(e.position())
            print(self.size())
            return super().dragMoveEvent(e)
        
        def dropEvent(self, e: QDropEvent) -> None:
            e.acceptProposedAction()
            self.setObjectName(None)
            self.style().polish(self)
            print("dropped here")
            
        def dragLeaveEvent(self, e: QDragLeaveEvent) -> None:
            self.setObjectName(None)
            self.style().polish(self)
            return super().dragLeaveEvent(e)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("EditorFrame")
        self.filebar = FileBar(self)
        #self.filebar.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.filebar.closing_current.connect(self.__on_current_close)
        self.filebar.tab_click.connect(self.__on_tab_change)
        self.text_edit = EditorFrame.CustomPlainTextEdit(self)
        #self.text_edit.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.text_edit.setContentsMargins(0, 0, 0, 0)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_edit.key_pressed.connect(self.__on_text_changed)
        self.text_edit.cliked.connect(lambda: self.clicked.emit(self))
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  
        layout.setSpacing(0) 
        layout.addWidget(self.filebar)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
        self.highlight_word("-var")
        
    def idle(self):
        ...

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
        self.filebar.add_file(file, current=True)
        file_loader = FileLoader(file)
        self.text_edit.setPlainText(file_loader.load())
        
    def set_blank_file(self) -> None:
        self.filebar.add_file(File("Unknow", None), current=True)
        self.text_edit.setPlainText("")
        
    def get_current(self) -> tuple[str, File | None]:
        return self.text_edit.toPlainText(), self.filebar.get_current_file()
    
    def mousePressEvent(self, event) -> None:
        self.clicked.emit(self)
        return super().mousePressEvent(event)
    
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