from PySide6.QtWidgets import QWidget
import json

class ThemeManager:
    def __init__(self, theme_file: str) -> None:
        with open(theme_file, "r") as file:
            self.theme = json.load(file)
    
    def apply_theme(self, theme_name: str, window: QWidget):
        theme = self.theme.get(theme_name, {})
        stylesheet = f"""
        
        QLabel {{
            background-color: red;
        }}
        
        """
        print(stylesheet)
        window.setStyleSheet(stylesheet)