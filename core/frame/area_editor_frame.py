from PySide6.QtGui import QDropEvent
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QSplitter,QSizePolicy, QHBoxLayout, QBoxLayout, QTextEdit
from PySide6.QtCore import Qt
from core.file_handlers import File
from core.frame.editor_frame import EditorFrame    
    
class AreaEditorFrame(QFrame):
    class AreaNode():
        def __init__(self, leaves: list, orientation: int) -> None:
            self.leaves: list[AreaEditorFrame.AreaNode] = leaves
            self.orientation = orientation
        def get(self) -> tuple[list[object], int, int]: 
            return (self.leaves, len(self.leaves), self.orientation)    
    
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.__editor_list: list[EditorFrame] = list()
        self.__current_editor: EditorFrame = None
        self.__area_tree = AreaEditorFrame.AreaNode(leaves=[], orientation=0)
        self.__area_widget: QFrame = None
        self.__area_layout: QBoxLayout = None
        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(0,0,0,0)
        self.__layout.setSpacing(0)
        self.setLayout(self.__layout)
        self.build_area()
        
    def build_area(self) -> None:
        if self.__area_widget:
            self.__area_widget.deleteLater()
        self.__area_widget = QFrame(self) 
        self.__area_layout = self.__build_area(self.__area_tree, self.__area_widget)
        self.__area_widget.setLayout(self.__area_layout)
        self.__layout.addWidget(self.__area_widget)
        
    def get_current_editor(self) -> EditorFrame:
        return self.__current_editor
    
    def set_current_editor(self, editor: EditorFrame) -> None:
        self.__current_editor = editor  
        
    def update_file_saved(self, file: File):
        for editor in self.__editor_list:
            editor.filebar.on_file_saved(file)    
        
    def __create_editor(self) -> EditorFrame:
        new_editor = EditorFrame(self)
        new_editor.splitted.connect(self.__on_split)
        self.__editor_list.append(new_editor)
        self.set_current_editor(new_editor)
        new_editor.clicked.connect(lambda editor: self.set_current_editor(editor)) 
        return new_editor
        
    def __build_area(self, area: AreaNode, parent: QWidget) -> QBoxLayout:
        leaves, height, orientation = area.get()
        layout = QVBoxLayout(parent) if orientation == 1 else QHBoxLayout(parent)
        layout.setContentsMargins(0,0,0,0)
        if height == 0:
            frame = self.__create_editor()
            layout.addWidget(frame)
            return layout
        spliter = QSplitter(Qt.Vertical) if orientation == 1 else QSplitter(Qt.Horizontal)
        layout.addWidget(spliter)
        for child in leaves:
            frame = QFrame(parent)
            frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            child_layout = self.__build_area(child, frame)
            frame.setLayout(child_layout)
            spliter.addWidget(frame)
            
    def __on_split(self, direction: int, file: File):
        print("Splitting here clear" + str(direction))