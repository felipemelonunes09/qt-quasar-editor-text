from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QSplitter,QSizePolicy, QHBoxLayout, QBoxLayout, QTextEdit
from PySide6.QtCore import Qt
from core.frame.editor_frame import EditorFrame

class AreaNode():
    def __init__(self, leaves: list, orientation: int) -> None:
        self.leaves: list[AreaNode] = leaves
        self.orientation = orientation
    def get(self) -> tuple[list[object], int, int]: 
        return (self.leaves, len(self.leaves), self.orientation)       

class AreaEditorFrame(QFrame):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        self.__area_tree = AreaNode(leaves=[
            AreaNode(leaves=[], orientation=0),
            AreaNode(leaves=[
                AreaNode(leaves=[], orientation=0),
                AreaNode(leaves=[], orientation=0)
            ], orientation=1)    
        ], orientation=0)
        self.setLayout(self.__build_area(self.__area_tree, self))
    def __build_area(self, area: AreaNode, parent: QWidget) -> QBoxLayout:
        leaves, height, orientation = area.get()
        layout = QVBoxLayout(parent) if orientation == 1 else QHBoxLayout(parent)
        layout.setContentsMargins(0,0,0,0)
        if height == 0:
            frame = EditorFrame(parent)
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
             