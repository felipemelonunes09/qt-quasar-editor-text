import yaml

class Config():
    def __init__(self, config_file="config.yaml") -> None:
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)
    
    def get_screen_config(self) -> dict:
        return self.config['screen']
    
    def get_theme_config(self) -> dict:
        return self.config['style']
    
config = Config()
screen = config.get_screen_config()
theme = config.get_theme_config()

######## ########### #######
######## Main Layout #######
######## ########### #######

splitter_size   = [ screen['splitter_size'].get('left', 50), screen['splitter_size'].get('right', 400) ]

######## ########### #######
########    Style    #######
######## ########### #######

style = config.get_theme_config()
theme = style.get("theme")
pallete_path = style.get("pallete-path")
