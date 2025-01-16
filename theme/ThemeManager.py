from PySide6.QtWidgets import QWidget
import json

class ThemeManager:
    theme: dict[dict, str | dict]
    def __init__(self, theme_file: str, context_theme: str) -> None:
        with open(theme_file, "r") as file:
            self.theme = json.load(file)
        
        self.context_theme_name = context_theme
        ThemeManager.theme = self.theme[self.context_theme_name]
    
    def apply_theme(self, theme_name: str, window: QWidget):
        theme = self.theme.get(theme_name, self.theme[self.context_theme_name])
        stylesheet = f"""
            QMenuBar {{
                background-color: { theme['bg-secondary-1'] };
                color: { theme['text-menu-color'] };
            }}
            QMenuBar::item {{}}
            QMenuBar::item::selected {{}}
            QLabel {{
                color: { theme['text-color-primary'] };
            }}
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
            #EditorFrame #QPlainTextEditDragEnterCenter {{ background-color: rgba(255, 255, 255, 75); }}
            #EditorFrame #QPlainTextEditDragEnterLeft {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,  
                    stop: 0 gray,               
                    stop: 0.5 gray,             
                    stop: 0.5  { theme['bg-primary-1'] },              
                    stop: 1  { theme['bg-primary-1'] }                
                );
            }}
            #EditorFrame #QPlainTextEditDragEnterRight {{
                background: qlineargradient(
                    x1: 1, y1: 0, x2: 0, y2: 0,  
                    stop: 0 gray,               
                    stop: 0.5 gray,             
                    stop: 0.5  { theme['bg-primary-1'] },              
                    stop: 1  { theme['bg-primary-1'] }                
                );
            }}
            #EditorFrame #QPlainTextEditDragEnterTop {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,  
                    stop: 0 gray,               
                    stop: 0.5 gray,             
                    stop: 0.5  { theme['bg-primary-1'] },              
                    stop: 1  { theme['bg-primary-1'] }                
                );
            }}
            #EditorFrame #QPlainTextEditDragEnterBottom {{
                background: qlineargradient(
                    x1: 0, y1: 1, x2: 0, y2: 0,  
                    stop: 0 gray,               
                    stop: 0.5 gray,             
                    stop: 0.5  { theme['bg-primary-1'] },              
                    stop: 1  { theme['bg-primary-1'] }                
                );
            }}
            
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
                border-top: 2px solid #334EAC;
                border-left: 1px solid { theme["bg-secondary-1"] }; 
                border-right: 1px solid { theme["bg-secondary-1"] };  
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