from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QKeyEvent
from PySide6.QtCore import Qt, Signal
from files.utils import isEmpty, isNumOrDot
from files.variables_ import BIG_FONT_SIZE, MEDIUM_FONT_SIZE, SMALL_FONT_SIZE, TEXT_MARGIN

class Display(QLineEdit):
    enterPress = Signal()
    delPress = Signal()
    clearPress = Signal()
    historyPress = Signal()  
    inputPress = Signal(str)
    operatorPress = Signal(str)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {MEDIUM_FONT_SIZE}px;')
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[TEXT_MARGIN for _ in range(4)])
        self.setMinimumWidth(300)
        self.setMinimumHeight(10) 

    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return, KEYS.Key_Equal]
        isDel = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isEsq = key in [KEYS.Key_Escape, KEYS.Key_C]
        ishistory = key in [KEYS.Key_H]
        isoperator = key in [KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_Asterisk]


        if isEnter:
            self.enterPress.emit()
            return event.ignore()            
        
        if isDel:
            self.delPress.emit()
            return event.ignore()
        
        if isEsq:
            self.clearPress.emit()
            return event.ignore()
        
        if ishistory:
            self.historyPress.emit()
            return event.ignore()
        
        if isoperator:
            self.operatorPress.emit(text)
            return event.ignore()           

        if isEmpty(text):
            return event.ignore()
        
        if isNumOrDot(text):
            self.inputPress.emit(text)
            return event.ignore()
