from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from main_window import MainWindow
from files.variables_ import WINDOW_ICON_PATH
from display import Display
from info import Info
from files.style_theme import setupTheme
from buttons import ButtonsGrid

if __name__ == '__main__':
    # Iniciar interface + tema da interface
    app = QApplication()
    window = MainWindow()
    setupTheme(app) 

    # definindo icon
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    #info +-*
    info = Info('')
    window.AddWidgetToVlayout(info)

    # Display
    display = Display()
    window.AddWidgetToVlayout(display)

    # Grid
    buttonGrid =  ButtonsGrid(display, info, window)
    window.Vlayout.addLayout(buttonGrid)

    #ajustar e mostrar itens na tela, iniciar interface
    window.adjustfixedSize()
    window.show()
    app.exec()