from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QFile, QIODevice

class Editor():
    
    @staticmethod
    def open_file_dialog() -> QFile | None:
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File")
        if file_path:
            return QFile(file_path)
    
    @staticmethod
    def open_dir_dialog() -> str | None:
        dir_path = QFileDialog.getExistingDirectory(None, "Open your project")
        if dir_path:
            return dir_path
    
    @staticmethod
    def save_file(file: QFile, content: str) -> None:
        if file.open(QIODevice.WriteOnly | QIODevice.Text):
            file.write(content.encode("utf-8"))
            file.close()

    @staticmethod
    def read_file(file: QFile) -> str:
        if file.open(QIODevice.ReadOnly | QIODevice.Text):
            content = file.readAll().data().decode("utf-8")
            file.close()
            return content
