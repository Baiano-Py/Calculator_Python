from PySide6.QtWidgets import QLineEdit, QLabel, QWidget
from PySide6.QtCore import Qt
from files.variables_ import BIG_FONT_SIZE, MEDIUM_FONT_SIZE, SMALL_FONT_SIZE, TEXT_MARGIN

class Display(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {MEDIUM_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[TEXT_MARGIN for _ in range(4)])
        self.setMinimumWidth(300)
        self.setMinimumHeight(10) 

