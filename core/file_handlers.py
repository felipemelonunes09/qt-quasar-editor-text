
from typing import Union
from core.file_objects import File

class FileLoader():
    def __init__(self, file: File) -> None:
        self.__file = file

    def load(self) -> str:
        with open(self.__file.get_path(), 'r') as file:
            return file.read()
        
class FileWriter():
    def __init__(self, file: File, content: Union[FileLoader, str]) -> None:
        self.__file = file
        self.__content = content
        
    def write(self):
        if  isinstance(self.__content, FileLoader):
            content = self.__content.load()
        else:
            content = self.__content
        with open(self.__file.get_path(), 'w') as file:     
            file.write(content)
            
            