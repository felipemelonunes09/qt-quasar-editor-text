from PySide6.QtWidgets import QWidget
import json

class ThemeManager:
    def __init__(self, theme_file: str) -> None:
        with open(theme_file, "r") as file:
            self.theme = json.load(file)
    
    def apply_theme(self, theme_name: str, window: QWidget):
        theme = self.theme.get(theme_name, {})
        stylesheet = f"""
            #InitialFrame {{
                background-color: { theme['bg-primary-1'] };
            }}      
            #InitialButton QWidget {{
                background-color: { theme['bg-secondary-1'] };
                font-weight: bold;
            }}
            #AttributesFrame {{
                background-color: { theme['bg-primary-2'] };
            }}
            #EditorFrame {{
                background-color: { theme['bg-primary-1'] };
            }}
            #EditorFrame QPlainTextEdit {{ background-color: { theme['bg-primary-1'] }; }}
            #FileBar {{  background-color: { theme["bg-primary-2"] };}}
            #FileTab {{ 
                border: 1px solid { theme["bg-secondary-1"] }; 
                padding-left: 15px;
                padding-right: 15px;
            }}
            #FileTabLabel QLabel {{
                color: red;
            }}
            #CurrentFileTab {{
                background-color: { theme['bg-primary-1'] };
                border-top: 4px solid #334EAC;
                border-left: 1px solid { theme["bg-secondary-1"] }; 
                border-right: 1px solide { theme["bg-secondary-1"] };  
            }}
            #FileTab QPushButton {{
                border: none;
                background-color: transparent;
            }}
            #CurrentFileTab QPushButton {{
                border: none;
                background-color: transparent;
            }}
            #CurrentFileTab QPushButton:pressed {{
                color: #414747;
            }}
            #FileTab QPushButton:pressed {{
                color: #414747;
            }}
            #FileTab:hover {{
                background-color: { theme["bg-secondary-2"] }; 
            }}
            QTreeWidget {{
                background-color: { theme['bg-primary-2'] };
                border: none;
            }}
        """
        window.setStyleSheet(stylesheet)