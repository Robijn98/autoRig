from PyQt5 import QtCore, QtWidgets
from junkYard.collapsibleBoxClass_pyQt5 import CollapsibleBox
from PyQt5.QtWidgets import (
    QScrollArea,
    QVBoxLayout,
    QMainWindow,
    QApplication,
    QWidget,
    QPushButton
)

class CollapsibleBox(QWidget):
    def __init__(self, title="", color = "", parent=None):
        super(CollapsibleBox, self).__init__(parent)

        self.toggle_button = QtWidgets.QToolButton(
            text=title, checkable=True, checked=False
        )
        self.toggle_button.setFixedSize(500,50)

        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setStyleSheet(f"color: black; background-color: rgb{color};")
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)

        self.toggle_button.pressed.connect(self.on_pressed)

        self.toggle_animation = QtCore.QParallelAnimationGroup(self)

        self.content_area = QScrollArea(
            maximumHeight=0, minimumHeight=0)
        self.content_area.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.content_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        lay = QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.toggle_button)
        lay.addWidget(self.content_area)

        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"minimumHeight")
        )
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self, b"maximumHeight")
        )
        self.toggle_animation.addAnimation(
            QtCore.QPropertyAnimation(self.content_area, b"maximumHeight")
        )

    def on_pressed(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            QtCore.Qt.DownArrow if not checked else QtCore.Qt.RightArrow
        )
        self.toggle_animation.setDirection(
            QtCore.QAbstractAnimation.Forward
            if not checked
            else QtCore.QAbstractAnimation.Backward
        )
        self.toggle_animation.start()

    def setContentLayout(self, layout):
        lay = self.content_area.layout()
        del lay
        self.content_area.setLayout(layout)
        collapsed_height = (
            self.sizeHint().height() - self.content_area.maximumHeight()
        )
        content_height = layout.sizeHint().height()
        for i in range(self.toggle_animation.animationCount()):
            animation = self.toggle_animation.animationAt(i)
            animation.setDuration(500)
            animation.setStartValue(collapsed_height)
            animation.setEndValue(collapsed_height + content_height)

        content_animation = self.toggle_animation.animationAt(
            self.toggle_animation.animationCount() - 1
        )
        content_animation.setDuration(500)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)


def create_collapsableBox(tabName='', color=(), buttons=[], functions=[]):
    box = CollapsibleBox(tabName, color)
    main_layout.addWidget(box)
    lay = QVBoxLayout()
    multiplier = 0.8

    for num, j in enumerate(buttons):
        pushButton = QPushButton("{}".format(j))
        mul_color = tuple(min(int(channel * multiplier), 255) for channel in color)
        pushButton.setStyleSheet(f"color: black; background-color: rgb{mul_color};")
        pushButton.clicked.connect(functions[num])  # Use clicked signal instead of pressed

        multiplier += 0.2
        lay.addWidget(pushButton)

    box.setContentLayout(lay)

def custom_print(printMessage=''):
    print(printMessage)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    w = QMainWindow()
    w.setCentralWidget(QWidget())
    main_layout = QVBoxLayout(w.centralWidget())

    tab_list = ['Skeleton Tools','Body Rig Tools', 'Face Rig Tools',
                'Skinning Tools', 'Connection Tools', 'Parent Tools']

    rainBow = [
        (255, 182, 193),
        (255, 204, 153),
        (255, 255, 153),
        (144, 238, 144),
        (173, 216, 230),
        (221, 160, 221),
        (255, 228, 225),
        (255, 218, 185),
        (255, 235, 205),
        (250, 250, 210),
        (152, 251, 152),
        (175, 238, 238),
        (240, 128, 128),
        (255, 182, 193),
        (173, 216, 230),
        (240, 230, 140),
        (255, 160, 122)
    ]


    create_collapsableBox(tab_list[0], rainBow[0], ['testButton', 'anotherButton'], [lambda: custom_print('hallelujah'), lambda: custom_print('and with two')])
    create_collapsableBox(tab_list[1], rainBow[1], ['testButton', 'anotherButton'], [lambda: custom_print('hallelujah'), lambda: custom_print('and with two')])




    main_layout.addStretch()
    w.resize(500, 500)
    w.show()
    sys.exit(app.exec_())
