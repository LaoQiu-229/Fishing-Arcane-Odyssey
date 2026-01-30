from PyQt6 import QtWidgets, QtGui, QtCore
import json

from modules.SimpleComponents import WindowTitleBar, Button, Entry, Label
from modules.GlobalVariables import CSS, EXIT_ICON

class SettingsWindow(QtWidgets.QMainWindow):
    rodKey: int = 0
    luminousKey: int = 9
    potionKey: int = 8
    useLuminous: bool = False
    usePotion: bool = False
    timeForTry: int = 22.5
    luminousTimer: int = 300
    potionTimer: int = 300
    baitChoice: str = "Normal"

    def __init__(self, parent: QtWidgets.QMainWindow):
        super().__init__()

        self.title = "AF  |  Settings"
        self.icon = parent.icon

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon))
        self.setFixedSize(360, 290)
        self.move(parent.pos().x() - 75, parent.height() + 10)
        self.setObjectName("Window")
        self.setStyleSheet(CSS)

        windowTitle = WindowTitleBar(self)
        btn_close = Button(self, EXIT_ICON, self.width() - 28, 2, 26, 26, "btn_red", self.close)
        btn_close.setToolTip("Close window")
        btn_cancel = Button(self, "Cancel", self.width() - 80, 2, 50, 26, "btn_red", self.clearEntrys)
        btn_cancel.setToolTip("Cancel all changes")
        btn_save = Button(self, "Save", self.width() - 132, 2, 50, 26, "btn_standart", self.saveChanges)
        btn_save.setToolTip("Save changes")    

        grid = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel(self)
        grid.setColumnMinimumWidth(1, 100)

        label_rodKey = Label(self, 0, 0, 0, 0, "label", "Rod key")
        label_rodKey.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)    
        self.__entry_rodKey = Entry(self, 0, 0, 0, 0, "EMPTY", False, "entry_standart")
        grid.addWidget(label_rodKey, 0, 0)
        grid.addWidget(self.__entry_rodKey, 0, 1, 1, 2)

        label_luminousKey = Label(self, 0, 0, 0, 0, "label", "Luminous key")
        label_luminousKey.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__button_useLuminous = Button(self, "Use luminous", 0, 0, 0, 0, "btn_red", self.changeLuminousFlag)
        self.__entry_luminousKey = Entry(self, 0, 0, 0, 0, "EMPTY", False, "entry_standart")
        label_luminousTimer = Label(self, 0, 0, 0, 0, "label", "Luminous timer")
        label_luminousTimer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__entry_luminousTimer = Entry(self, 0, 0, 0, 0, "EMPTY", False, "entry_standart")
        grid.addWidget(label_luminousKey, 1, 0)
        grid.addWidget(self.__button_useLuminous, 1, 1)
        grid.addWidget(self.__entry_luminousKey, 1, 2)
        grid.addWidget(label_luminousTimer, 2, 0)
        grid.addWidget(self.__entry_luminousTimer, 2, 1, 1, 2)

        label_potionKey = Label(self, 0, 0, 0, 0, "lable", "Potion key")
        label_potionKey.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__button_usePotion = Button(self, "Use potion", 0, 0, 0, 0, "btn_red", self.changePotionFlag)
        self.__entry_potionKey = Entry(self, 0, 0, 0, 0, "EMPTY", False, "entry_standart")
        label_potionTimer = Label(self, 0, 0, 0, 0, "label", "Potion timer")
        label_potionTimer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__entry_potionTimer = Entry(self, 0, 0, 0, 0, "EMPTY", False, "entry_standart")
        grid.addWidget(label_potionKey, 3, 0)
        grid.addWidget(self.__button_usePotion, 3, 1)
        grid.addWidget(self.__entry_potionKey, 3, 2)
        grid.addWidget(label_potionTimer, 4, 0)
        grid.addWidget(self.__entry_potionTimer, 4, 1, 1, 2)

        label_seaChoice = Label(self, 0, 0, 0, 0, "label", "Sea choice")
        label_seaChoice.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__sea_combo = QtWidgets.QComboBox(self)
        self.__sea_combo.addItems(["Normal sea", "Dark sea"])
        grid.addWidget(label_seaChoice, 5, 0)
        grid.addWidget(self.__sea_combo, 5, 1, 1, 2)

        label_baitChoice = Label(self, 0, 0, 0, 0, "label", "Bait choice")
        label_baitChoice.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.__bait_combo = QtWidgets.QComboBox(self)
        self.__bait_combo.addItems(["Normal", "Swarm", "Giant", "Magic"])
        grid.addWidget(label_baitChoice, 6, 0)
        grid.addWidget(self.__bait_combo, 6, 1, 1, 2)

        label.setFixedSize(self.width() - 4, self.height() - 34)
        label.move(2, 32)
        label.setLayout(grid)

        self.readDataBase()

    def changeLuminousFlag(self) -> None:
        self.useLuminous = not self.useLuminous
        if self.useLuminous: self.__button_useLuminous.setObjectName("btn_standart")
        else: self.__button_useLuminous.setObjectName("btn_red")
        self.setStyleSheet(CSS)

    def changePotionFlag(self) -> None:
        self.usePotion = not self.usePotion
        if self.usePotion: self.__button_usePotion.setObjectName("btn_standart")
        else: self.__button_usePotion.setObjectName("btn_red")
        self.setStyleSheet(CSS)

    def clearEntrys(self) -> None:
        self.__entry_rodKey.clear()
        self.__entry_luminousKey.clear()
        self.__entry_potionKey.clear()
        self.__entry_luminousTimer.clear()
        self.__entry_potionTimer.clear()

        self.__entry_rodKey.setObjectName("entry_standart")
        self.__entry_luminousKey.setObjectName("entry_standart")
        self.__entry_potionKey.setObjectName("entry_standart")
        self.__entry_luminousTimer.setObjectName("entry_standart")
        self.__entry_potionTimer.setObjectName("entry_standart")
        self.setStyleSheet(CSS)

        if self.timeForTry == 22.5: self.__sea_combo.setCurrentIndex(0)
        elif self.timeForTry == 30: self.__sea_combo.setCurrentIndex(1)

        if self.baitChoice == "Normal": self.__bait_combo.setCurrentIndex(0)
        elif self.baitChoice == "Swarm": self.__bait_combo.setCurrentIndex(1)
        elif self.baitChoice == "Giant": self.__bait_combo.setCurrentIndex(2)
        elif self.baitChoice == "Magic": self.__bait_combo.setCurrentIndex(3)

        self.close()

    def checkEntry(self, variable: int, entry: Entry):
        newVariable = entry.text().lower()
        if (newVariable in ['1','2','3','4','5','6','7','8','9','0']) or (newVariable == ''):
            if newVariable in ['1','2','3','4','5','6','7','8','9','0']:
                newVariable = int(newVariable)
            elif newVariable == '':
                newVariable = variable
            entry.setObjectName("entry_standart")
            entry.setPlaceholderText(f"0-9, default is {newVariable}")
            self.setStyleSheet(CSS)
            return newVariable, True
        else:
            entry.setObjectName("entry_red")
            self.setStyleSheet(CSS)
            return variable, False
        
    def checkEntryWithTime(self, variable: int|str, entry: Entry):
        newValue = entry.text()
        try:
            newValue = int(newValue)
            entry.setObjectName("entry_standart")
            boolResult = True
        except:
            if newValue == "":
                newValue = variable
                boolResult = True
                entry.setObjectName("entry_standart")
            else:
                entry.setObjectName("entry_red")
                self.setStyleSheet(CSS)
                newValue = variable
                boolResult = False
        self.setStyleSheet(CSS)
        entry.setPlaceholderText(f"{newValue} seconds")
        return newValue, boolResult

    def saveChanges(self) -> None:
        check1 = self.checkEntry(self.rodKey, self.__entry_rodKey)
        check2 = self.checkEntry(self.luminousKey, self.__entry_luminousKey)
        check3 = self.checkEntry(self.potionKey, self.__entry_potionKey)
        check4 = self.checkEntryWithTime(self.luminousTimer, self.__entry_luminousTimer)
        check5 = self.checkEntryWithTime(self.potionTimer, self.__entry_potionTimer)

        self.rodKey = check1[0]
        self.luminousKey = check2[0]
        self.potionKey = check3[0]
        self.luminousTimer = check4[0]
        self.potionTimer = check5[0]
        sea = self.__sea_combo.currentText()
        if sea == "Normal sea": self.timeForTry = 22.5
        elif sea == "Dark sea": self.timeForTry = 30

        self.baitChoice = self.__bait_combo.currentText()

        if check1[1] and check2[1] and check3[1] and check4[1] and check5[1]:
            self.clearEntrys()

            with open("DB.json", "r") as file:
                data = json.loads(file.read())
                screenSize = data["screenSize"][0]

            newDBobject = {
                "settings": [{
                    "rodKey": self.rodKey,
                    "luminousKey": self.luminousKey,
                    "potionKey": self.potionKey,
                    "useLuminous": self.useLuminous,
                    "usePotion": self.usePotion,
                    "luminousTimer": self.luminousTimer,
                    "potionTimer": self.potionTimer,
                    "timeForTry": self.timeForTry,
                    "baitChoice": self.baitChoice
                }],
                "screenSize": [screenSize]}

            with open('DB.json', 'w') as file:
                json.dump(newDBobject, file)

    def readDataBase(self) -> None:
        file = open("DB.json", "r")
        data = json.loads(file.read())

        settings = data['settings'][0]

        self.rodKey = settings["rodKey"]
        self.luminousKey = settings["luminousKey"]
        self.potionKey = settings["potionKey"]
        self.useLuminous = settings["useLuminous"]
        self.usePotion = settings["usePotion"]
        self.luminousTimer = settings["luminousTimer"]
        self.potionTimer = settings["potionTimer"]
        self.timeForTry = settings["timeForTry"]
        self.baitChoice = settings.get("baitChoice", "Normal")

        self.__entry_rodKey.setPlaceholderText(f"0-9, default is {self.rodKey}")
        self.__entry_luminousKey.setPlaceholderText(f"0-9, default is {self.luminousKey}")
        self.__entry_potionKey.setPlaceholderText(f"0-9, default is {self.potionKey}")
        if self.useLuminous: self.__button_useLuminous.setObjectName("btn_standart")
        if self.usePotion: self.__button_usePotion.setObjectName("btn_standart")
        self.__entry_luminousTimer.setPlaceholderText(f"{self.luminousTimer} seconds")
        self.__entry_potionTimer.setPlaceholderText(f"{self.potionTimer} seconds")
        if self.timeForTry == 22.5: self.__sea_combo.setCurrentIndex(0)
        elif self.timeForTry == 30: self.__sea_combo.setCurrentIndex(1)

        if self.baitChoice == "Normal": self.__bait_combo.setCurrentIndex(0)
        elif self.baitChoice == "Swarm": self.__bait_combo.setCurrentIndex(1)
        elif self.baitChoice == "Giant": self.__bait_combo.setCurrentIndex(2)
        elif self.baitChoice == "Magic": self.__bait_combo.setCurrentIndex(3)