from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QFile, QIODevice

class Editor():
    
    def __init__(self) -> None:
        pass
    
    def open_file_dialog(self) -> QFile | None:
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File")
        if file_path:
            return QFile(file_path)
    
    def open_dir_dialog(self) -> str | None:
        dir_path = QFileDialog.getExistingDirectory(None, "Open your project")
        if dir_path:
            return dir_path
    
    def save_file(self, file: QFile, content: str) -> None:
        if file.open(QIODevice.WriteOnly | QIODevice.Text):
            file.write(content.encode("utf-8"))
            file.close()
