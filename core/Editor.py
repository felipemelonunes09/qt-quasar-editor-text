from PySide6.QtWidgets import QFileDialog
from core.file_objects import File
from core.file_handlers import FileWriter

class Editor():
    
    def __init__(self) -> None:
        pass
    
    def open_file_dialog(self) -> File | None:
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File")
        if file_path:
            return File(file_path.split("/")[-1], file_path)
    
    def open_dir_dialog(self) -> str | None:
        dir_path = QFileDialog.getExistingDirectory(None, "Open your project")
        if dir_path:
            return dir_path
    
    def save_file(self, file: File, content: str) -> None:
        if not file.get_path():
            file.set_path(QFileDialog.getSaveFileName(None, "Save File")[0])
        file_writer = FileWriter(file=file, content=content)
        file_writer.write()
