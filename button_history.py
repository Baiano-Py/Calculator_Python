from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import os, sys
from typing import Optional



class ButtonInterpolator(QPushButton):

    def __init__(self,
              text                    : Optional[str]    = "",
              text_font_family        : Optional[str]    = "Verdana",
              text_color              : Optional[QColor] = QColor("#FFFFFF"),
              text_size               : Optional[int]    = 14,
              text_padding            : Optional[int]    = 24,
              text_align              : Optional[str]    = "left",
              background_color        : Optional[QColor] = QColor("#2A3442"),
              background_color_hover  : Optional[QColor] = QColor("#3F495E"),
              border_color            : Optional[int]    = QColor("#88C0D0"),
              border_left             : Optional[int]    = 0,
              border_top              : Optional[int]    = 0,
              border_right            : Optional[int]    = 0,
              border_bottom           : Optional[int]    = 0,
              tooltip                 : Optional[str]    = "",
              tooltip_color           : Optional[QColor] = QColor("#FFFFFF"),
              tooltip_background      : Optional[QColor] = QColor("#2A3442"),
              icon_color              : Optional[int]    = QColor("#3B4252"),
              icon_color_hover        : Optional[int]    = QColor("#FFFFFF"),
              icon_path               : Optional[int]    = "",
              minimum_width           : Optional[int]    = 25,
              checkable               : Optional[bool]   = False,
              active                  : Optional[bool]   = False,

        ) -> None:

        QPushButton.__init__(self)

        self.setText(text)
        self.setToolTip(tooltip)
        self.setMinimumHeight(50)
        self.setMaximumHeight(50)
        self.setCheckable(checkable)
        self.setAutoExclusive(checkable)
        self.setChecked(active)


        self.text_color             = text_color
        self.text_font_family       = text_font_family
        self.text_size              = text_size
        self.text_padding           = text_padding
        self.text_align             = text_align
        self.background_color       = background_color
        self.background_color_hover = background_color_hover
        self.border_color           = border_color
        self.border_left            = border_left
        self.border_top             = border_top
        self.border_right           = border_right
        self.tooltip_color          = tooltip_color
        self.tooltip_background     = tooltip_background
        self.icon_path              = icon_path
        self.icon_color             = icon_color
        self.icon_color_hover       = icon_color_hover
        self.border_bottom          = border_bottom
        self.minimum_width          = minimum_width
        self.active                 = active

        self.progress = 0.1

        self.addStyle(
            text_font_family       = self.text_font_family,
            text_color             = self.text_color,
            text_size              = self.text_size,
            text_padding           = self.text_padding,
            text_align             = self.text_align,
            background_color       = self.background_color,
            background_color_hover = self.background_color_hover,
            border_color           = self.border_color,
            border_left            = self.border_left,
            border_top             = self.border_top,
            border_right           = self.border_right,
            border_bottom          = self.border_bottom,
            tooltip_color          = self.tooltip_color,
            tooltip_background     = self.tooltip_background,
            active                 = self.active
        )

        self.animation = QVariantAnimation()
        self.animation.setStartValue(0.1)
        self.animation.setEndValue(0.9)
        self.animation.setDuration(100)
        self.animation.valueChanged.connect(self.interpolator)

        self.timer_leave = QTimer()
        self.timer_leave.setSingleShot(True)
        self.timer_leave.timeout.connect(self.restartAnimation)

        self.timer_enter = QTimer()
        self.timer_enter.setSingleShot(True)
        self.timer_enter.timeout.connect(self.startAnimation)


    def addStyle(self,
              text_font_family        : Optional[str]    = 'Verdana',
              text_color              : Optional[QColor] = QColor("#FFFFFF"),
              text_size               : Optional[int] = 14,
              text_padding            : Optional[int] = 24,
              text_align              : Optional[str] = "left",
              background_color        : Optional[QColor] = QColor("#2E3440"),
              background_color_hover  : Optional[QColor] = QColor("#3F495E"),
              border_color            : Optional[int] = QColor("#88C0D0"),
              border_left             : Optional[int] = 0,
              border_top              : Optional[int] = 0,
              border_right            : Optional[int] = 0,
              border_bottom           : Optional[int] = 0,
              tooltip_color           : Optional[QColor] = QColor("#FFFFFF"),
              tooltip_background      : Optional[QColor] = QColor("#2A3442"),
              active                  : Optional[bool] = False
        ):

        style = f"""
        QPushButton {{
            color: rgb({text_color.red()},{text_color.green()},{text_color.blue()});
            font-size: {text_size}px;
            padding-left: {text_padding}px;
            text-align: {text_align};
            background-color: rgb({background_color.red()},{background_color.green()},{background_color.blue()});
            border: none;
        }}

        QToolTip {{
            color: rgb({tooltip_color.red()},{tooltip_color.green()},{tooltip_color.blue()});
            background-color: rgb({tooltip_background.red()},{tooltip_background.green()},{tooltip_background.blue()});
            border: none;
        }}

        QPushButton:checked {{
            background-color: rgb({background_color_hover.red()},{background_color_hover.green()},{background_color_hover.blue()});
            border-left: {border_left}px solid rgb({border_color.red()},{border_color.green()},{border_color.blue()});
            border-top: {border_top}px solid rgb({border_color.red()},{border_color.green()},{border_color.blue()});
            border-right: {border_right}px solid rgb({border_color.red()},{border_color.green()},{border_color.blue()});
            border-bottom: {border_bottom}px solid rgb({border_color.red()},{border_color.green()},{border_color.blue()});
        }}
        QPushButton:unchecked {{
            background-color: rgb({background_color.red()},{background_color.green()},{background_color.blue()});
            border: none;
        }}
        """

        self.setStyleSheet(style)
    def drawIcon(self, image, qp, rect, color):

        abs_path = os.path.abspath(os.getcwd())
        folder_path = r"windows\widgets\PushButton\icons"
        join_path = os.path.join(abs_path, folder_path)
        norm_path = os.path.normpath(os.path.join(join_path, image))


        #icon =  QPixmap(r"C:\Users\Gabriel\Desktop\JG-Digitalization\windows\widgets\PushButton\icons\notification.svg")
        icon = QPixmap(norm_path)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)

        # def drawPixmap(self, x: int, y: int, w: int, h: int, pm: Union[PySide6.QtGui.QPixmap, PySide6.QtGui.QImage, str]) -> None: ...
        qp.drawPixmap(
            (rect.width() - icon.width()) / 2,
            (rect.height() - icon.height()) / 2,
            icon
        )

        painter.end()

    def startAnimation(self):
        self.animation.setDirection(QAbstractAnimation.Forward)
        self.animation.start()

    def interpolator(self, progress):
        self.progress = progress
        self.repaint()


    def restartAnimation(self):
        self.animation.setDirection(QAbstractAnimation.Backward)
        self.animation.start()

    # QPushButton.paintEvent(self, event)
    def paintEvent(self, event):
        QPushButton.paintEvent(self, event)
        self.painter = QPainter()
        self.painter.begin(self)
        self.painter.setPen(Qt.NoPen)

        self.painter.setRenderHint(QPainter.Antialiasing)

        self.icon_rect = QRect(0,0,self.minimum_width, self.height())
        if not self.isChecked():
            self.drawIcon(self.icon_path, self.painter, self.icon_rect, QColor(
                self.icon_color.red() + (self.icon_color_hover.red() - self.icon_color.red()) * self.progress,
                self.icon_color.green() + (self.icon_color_hover.green() - self.icon_color.green()) * self.progress,
                self.icon_color.blue() + (self.icon_color_hover.blue() - self.icon_color.blue()) * self.progress
            ))
            self.painter.end()
        else:
            self.drawIcon(self.icon_path, self.painter, self.icon_rect, QColor(
                self.icon_color_hover.red(),
                self.icon_color_hover.green(),
                self.icon_color_hover.blue()
            ))
            self.painter.end()



    # QPushButton.enterEvent(self, event)
    def enterEvent(self, event):
        self.timer_leave.stop()
        self.timer_enter.start(80)

    # QPushButton.leaveEvent(self, event)
    def leaveEvent(self, event):
        self.timer_enter.stop()
        self.timer_leave.start(80)