from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        #configuração do layout basico
        self.central_widget = QWidget()
        self.Vlayout = QVBoxLayout()
        self.central_widget.setLayout(self.Vlayout)
        self.setCentralWidget(self.central_widget)

        #definir Titulo do aplicativo
        self.setWindowTitle('Calculator')


    def adjustfixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def AddWidgetToVlayout(self, widget: QWidget):
        self.Vlayout.addWidget(widget)
    
    def makeMensageBox(self):
        return QMessageBox(self)

