import sys
sys.path.append("/UI\\")
from autoRigFunctions import custom_print
from junkYard.collapsibleBoxClass_pyQt5 import CollapsibleBox

from PyQt5.QtWidgets import (
    QVBoxLayout,
    QMainWindow,
    QApplication,
    QWidget,
    QPushButton
)


def create_collapsableBox(tabName='', color=(), buttons=[], functions=[]):
    box = CollapsibleBox(tabName, color)
    main_layout.addWidget(box)
    lay = QVBoxLayout()
    multiplier = 0.8

    for num, j in enumerate(buttons):
        pushButton = QPushButton("{}".format(j))
        mul_color = tuple(min(int(channel * multiplier), 255) for channel in color)
        pushButton.setStyleSheet(f"color: black; background-color: rgb{mul_color};border-radius: 5px;")

        pushButton.clicked.connect(functions[num])  # Use clicked signal instead of pressed

        multiplier += 0.2
        lay.addWidget(pushButton)

    box.setContentLayout(lay)


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
    create_collapsableBox(tab_list[2], rainBow[2], ['look', 'something'], [lambda: custom_print('print this'), lambda: custom_print('and with two')])
    create_collapsableBox(tab_list[3], rainBow[3], ['look', 'something'], [lambda: custom_print('print this'), lambda: custom_print('and with two')])
    create_collapsableBox(tab_list[4], rainBow[4], ['lecture', 'rigging'], [lambda: custom_print('this'), lambda: custom_print('and with two')])

    w.setWindowTitle("autoRig tools")

    main_layout.addStretch()
    w.resize(500, 500)
    w.show()
    sys.exit(app.exec_())
