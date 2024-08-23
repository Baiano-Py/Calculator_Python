from pathlib import Path

ROOT_DIR = Path(__file__).parent
WINDOW_ICON_PATH = ROOT_DIR / 'icon.png'

file_pasta = Path(__file__).parent
caminho_history = file_pasta / 'history.json'


PRIMARY_COLOR = '#1e81b0'
DARKER_PRIMARY_COLOR = '#16658a'
DARKEST_PRIMARY_COLOR = '#115270'
#sizing

BIG_FONT_SIZE = 40
MEDIUM_FONT_SIZE = 24
SMALL_FONT_SIZE = 18
TEXT_MARGIN = 15

#botão tema
button_theme ="""
background-color: #0E1418;
color: #057DCE;
font-size: 18px;
border: 1px solid #666;
border-radius: 5px;
"""

info_theme ="""
background-color: #0E1418;
color: #057DCE;
font-size: 20px;
border: 4px solid #666;
border-radius: 5px;
"""