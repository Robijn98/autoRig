import sys
from PySide2 import QtCore, QtGui, QtWidgets

sys.path.append("C:\\Users\\robin\\PycharmProjects\\autoRig\\UI\\")
from autoRigFunctions import custom_print
from collapsibleBoxClass import CollapsibleBox

sys.path.append("C:\\Users\\robin\\PycharmProjects\\autoRig\\bodyRig\\")
from arm_utils import ik_arm
def create_collapsible_box(tab_name='', color=(), buttons=[], functions=[]):
    box = CollapsibleBox(tab_name, color)
    main_layout.addWidget(box)
    lay = QtWidgets.QVBoxLayout()
    multiplier = 0.8

    for num, j in enumerate(buttons):
        push_button = QtWidgets.QPushButton("{}".format(j))
        mul_color = tuple(min(int(channel * multiplier), 255) for channel in color)
        push_button.setStyleSheet(f"color: black; background-color: rgb{mul_color};border-radius: 5px;")

        push_button.clicked.connect(functions[num])  # Use clicked signal instead of pressed

        multiplier += 0.2
        lay.addWidget(push_button)

    box.setContentLayout(lay)

if __name__ == "__main__":

    w = QtWidgets.QMainWindow()
    w.setCentralWidget(QtWidgets.QWidget())
    main_layout = QtWidgets.QVBoxLayout(w.centralWidget())

    tab_list = ['Skeleton Tools', 'Body Rig Tools', 'Face Rig Tools',
                'Skinning Tools', 'Connection Tools', 'Parent Tools']

    rainbow = [
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

    create_collapsible_box(tab_list[0], rainbow[0], ['R_arm_test', 'anotherButton'], [lambda: ik_arm('R_shoulder_JNT', 'R_elbow_JNT', 'R_wrist_JNT', 'R'), lambda: custom_print('and with two')])
    create_collapsible_box(tab_list[1], rainbow[1], ['testButton', 'anotherButton'], [lambda: custom_print('hallelujah'), lambda: custom_print('and with two')])
    create_collapsible_box(tab_list[2], rainbow[2], ['look', 'something'], [lambda: custom_print('print this'), lambda: custom_print('and with two')])
    create_collapsible_box(tab_list[3], rainbow[3], ['look', 'something'], [lambda: custom_print('print this'), lambda: custom_print('and with two')])
    create_collapsible_box(tab_list[4], rainbow[4], ['lecture', 'rigging'], [lambda: custom_print('this'), lambda: custom_print('and with two')])

    w.setWindowTitle("autoRig tools")

    main_layout.addStretch()
    w.resize(500, 500)
    w.show()

