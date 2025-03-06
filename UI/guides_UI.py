from PySide2.QtWidgets import QApplication, QWidget

def main():

    app = QApplication.instance()
    if not app:
        app = QApplication([])

    window = QWidget()
    window.setWindowTitle("PySide2 Test")
    window.resize(400, 300)
    window.show()

    app.exec_()

main()

# sys.path.append('/home/s5725067/myRepos/autoRig/utils/')
# try:
#     import create_guides
#     importlib.reload(create_guides)
#     from create_guides import guides
# except ImportError:
#     print("Error importing create_guides")

# sys.path.append('/home/s5725067/myRepos/autoRig/UI/')
# try:
#     import collapsibleBoxClass
#     importlib.reload(collapsibleBoxClass)
#     from collapsibleBoxClass import CollapsibleBox
# except ImportError:
#     print("Error importing collapsibleBoxClass")


# def create_collapsible_box(main_layout, tab_name='', color=(), buttons=[], functions=[]):
#     box = CollapsibleBox(tab_name, color)
#     main_layout.addWidget(box)
#     lay = QtWidgets.QVBoxLayout()
#     multiplier = 0.8

#     for num, j in enumerate(buttons):
#         push_button = QtWidgets.QPushButton("{}".format(j))
#         mul_color = tuple(min(int(channel * multiplier), 255) for channel in color)
#         push_button.setStyleSheet(f"color: black; background-color: rgb{mul_color};border-radius: 5px;")

#         push_button.clicked.connect(functions[num])  # Use clicked signal instead of pressed

#         multiplier += 0.2
#         lay.addWidget(push_button)

#     box.setContentLayout(lay)

# def custom_print(text):
#     print(text)

# def main():
#     w = QtWidgets.QMainWindow()
#     print("UI loaded")
#     w.setCentralWidget(QtWidgets.QWidget())
#     main_layout = QtWidgets.QVBoxLayout(w.centralWidget())
#     print("UI layout set")

#     tab_list = ['Create Guides']

#     rainbow = [
#         (255, 182, 193),
#         (255, 204, 153),
#         (255, 255, 153),
#         (144, 238, 144),
#         (173, 216, 230),
#         (221, 160, 221),
#         (255, 228, 225),
#         (255, 218, 185),
#         (255, 235, 205),
#         (250, 250, 210),
#         (152, 251, 152),
#         (175, 238, 238),
#         (240, 128, 128),
#         (255, 182, 193),
#         (173, 216, 230),
#         (240, 230, 140),
#         (255, 160, 122)
#     ]

#     print("colors set")

#     create_collapsible_box(main_layout, tab_list[0], rainbow[0], ['R_arm_test', 'anotherButton'], [lambda: custom_print("hello"), lambda: custom_print('and with two')])
#     # create_collapsible_box(main_layout, tab_list[1], rainbow[1], ['testButton', 'anotherButton'], [lambda: custom_print('hallelujah'), lambda: custom_print('and with two')])
#     # create_collapsible_box(main_layout, tab_list[2], rainbow[2], ['look', 'something'], [lambda: custom_print('print this'), lambda: custom_print('and with two')])
#     # create_collapsible_box(main_layout, tab_list[3], rainbow[3], ['look', 'something'], [lambda: custom_print('print this'), lambda: custom_print('and with two')])
#     # create_collapsible_box(main_layout, tab_list[4], rainbow[4], ['lecture', 'rigging'], [lambda: custom_print('this'), lambda: custom_print('and with two')])
    
#     print("created boxes")

#     w.setWindowTitle("autoRig tools")
#     print("set title")  
#     main_layout.addStretch()
#     print("added stretch")
#     w.resize(500, 500)
#     print("resized")
#     w.show()
#     print("showed window")
