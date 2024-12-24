from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QSplitter,QSizePolicy, QHBoxLayout, QBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtCore import Slot, Qt
from core.file_handlers import File
from core.frame.editor_frame import EditorFrame    
from core.util.common import Direction
from typing import Self

    
class AreaEditorFrame(QFrame):
    class AreaNode():
        def __init__(self, leaves: list, orientation: int, frame: EditorFrame = None, parent: Self=None) -> None:
            self.leaves: list[Self] = leaves
            self.orientation = orientation
            self.frame: QFrame = frame
            self.parent: Self = parent
            
        def set_parent(self, parent: Self) -> None:
            self.parent = parent
        
        def set_frame(self, frame: EditorFrame) -> None:
            self.frame = frame
            
        def get_frame(self) -> EditorFrame | None:
            return self.frame
        
        def get_parent(self) -> Self:
            return self.parent
        
        def get(self) -> tuple[list[Self], int, int]: 
            return (self.leaves, len(self.leaves), self.orientation)    
    
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.__editor_list: list[EditorFrame] = list()
        self.__current_editor: EditorFrame = None
        self.__area_tree = AreaEditorFrame.AreaNode(leaves=[AreaEditorFrame.AreaNode(leaves=[], orientation=1)], orientation=0)
        self.__area_tree.leaves[0].set_parent(self.__area_tree)
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
            frame = area.get_frame() 
            if not frame: 
                frame = self.__create_editor() 
                area.set_frame(frame)
            setattr(frame, "__area_node__", area)
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
            child.set_parent(area)
    
    def __on_split(self, direction: Direction, file: File, editor: QFrame):
        __area_node__: AreaEditorFrame.AreaNode = getattr(editor, "__area_node__")
        if __area_node__:
            parent = __area_node__.get_parent()
            if parent:
                frame = __area_node__.get_frame()
                new_frame = self.__create_editor()
                new_frame.set_file(file)
                __area_node__.orientation = 0
                if direction == Direction.LEFT:
                    __area_node__.leaves.append(AreaEditorFrame.AreaNode(leaves=[], orientation=0, frame=new_frame, parent=__area_node__))
                    __area_node__.leaves.append(AreaEditorFrame.AreaNode(leaves=[], orientation=0, frame=frame, parent=__area_node__))
                if direction == Direction.RIGHT:
                    __area_node__.leaves.append(AreaEditorFrame.AreaNode(leaves=[], orientation=0, frame=frame, parent=__area_node__))
                    __area_node__.leaves.append(AreaEditorFrame.AreaNode(leaves=[], orientation=0, frame=new_frame, parent=__area_node__))
                if direction == Direction.TOP:
                    __area_node__.orientation = 1
                    __area_node__.leaves.append(AreaEditorFrame.AreaNode(leaves=[], orientation=0, frame=new_frame, parent=__area_node__))
                    __area_node__.leaves.append(AreaEditorFrame.AreaNode(leaves=[], orientation=0, frame=frame, parent=__area_node__))
                if direction == Direction.BOTTOM:
                    __area_node__.orientation = 1
                    __area_node__.leaves.append(AreaEditorFrame.AreaNode(leaves=[], orientation=0, frame=frame, parent=__area_node__))
                    __area_node__.leaves.append(AreaEditorFrame.AreaNode(leaves=[], orientation=0, frame=new_frame, parent=__area_node__))
            self.build_area()