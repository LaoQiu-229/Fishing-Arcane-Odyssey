from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
import sys, os
import time
import threading
import cv2, pyautogui, numpy, keyboard
import json
import ctypes
import subprocess

from modules.SimpleComponents import Button, Label
from modules.GlobalVariables import *
from modules.SettingsWindow import SettingsWindow
from modules.LogsWindow import LogsWindow

# Vetex, this message is for you. If I get caught, I think I deserve to be praised...

# Ha-ha
# while I was writing the program I spent 10 days and caught only two sunken treasures (i caught 5000+ fish)
# but i got Expert Angler title, hah

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    
    return os.path.join(base_path, relative_path)

def locateImage(img, threshold: float):
    screenshot = pyautogui.screenshot()
    screenshot = numpy.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    image = numpy.uint8(img)
    result = cv2.matchTemplate(screenshot, image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        return (max_loc[0], max_loc[1])
    return None

def getLastSize() -> list[int]:
    file = open(resource_path("DB.json"), "r")
    data = json.loads(file.read())
    size = data["screenSize"][0]
    return [size["width"], size["height"]]

def changeLastSize(newSize: list[int]) -> None:
    with open(resource_path("DB.json"), "r") as file:
        data = json.loads(file.read())
        settings = data["settings"][0]
    newDBobject = {
        "settings": [settings],
        "screenSize": [{
            "width": newSize[0],
            "height": newSize[1]
        }]}
    with open(resource_path('DB.json'), 'w') as file:
        json.dump(newDBobject, file)

def changeImageSize(path: str, monitorSize: list[int], lastUsedSize: list[int]) -> None:
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    imgW = img.shape[1]
    imgH = img.shape[0]
    ratioW = monitorSize[0] * 100 / lastUsedSize[0] * 0.01
    ratioH = monitorSize[1] * 100 / lastUsedSize[1] * 0.01
    targetSize = (int(ratioW*imgW)+4, int(ratioH*imgH)+1)
    outIMG = cv2.resize(img, targetSize, cv2.INTER_LINEAR)
    cv2.imwrite(path, outIMG)

class MainWindow(QMainWindow):
    title: str = "title"
    isFishing: bool = False
    tryCatchFish: bool = False
    startThisTry: float = 0
    maxTimeForWait: int = 70
    startFishingTimer: float = 0
    startCheckMealTimer: float = 0
    checkMealTimer: int = 0
    startCheckPotionTimer: float = 0
    checkPotionTimer: int = 0
    shouldStopFishing: bool = False
    fishCount: int = 0

    def __init__(self, title: str):
        super().__init__()

        self.title: str = title
        self.icon = APP_ICON
        
        self.setObjectName("MainWindow")

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon))
        self.setFixedSize(300, 30)
        self.move((screenSize.width() // 2) - (self.width() // 2), 0)
        self.setStyleSheet(CSS)

        self.fishingThread = threading.Thread(target = self.fishing)

        self.settingsWindow = SettingsWindow(self)
        self.logsWindow = LogsWindow(self)

        self.btn_start = Button(self, "START", 2, 2, 75, 26, "btn_standart", self.startFishing)
        self.btn_start.setToolTip("Start fishing")
        btn_close = Button(self, EXIT_ICON, self.width() - 28, 2, 26, 26, "btn_red", self.closeEvent)
        btn_close.setToolTip("Close window")
        btn_settings = Button(self, SETTING_ICON, self.width() - 56, 2, 26, 26, "btn_standart", self.openSettings)
        btn_settings.setToolTip("Settings window")
        btn_logs = Button(self, LOGS_ICON, self.width() - 84, 2, 26, 26, "btn_standart", self.openLogsWindow)
        btn_logs.setToolTip("History window")
        self.__countLabel = Label(self, 79, 2, 135, 26, "", f"Caught: {self.fishCount}")

        self.ShouldStopFishingTimer = QTimer(self)
        self.ShouldStopFishingTimer.setInterval(500)
        self.ShouldStopFishingTimer.timeout.connect(self.checkShouldStopFishing)
        self.ShouldStopFishingTimer.start()

    def openSettings(self) -> None:
        if self.settingsWindow.isVisible():
            self.settingsWindow.hide()
        else:
            self.settingsWindow.show()

    def openLogsWindow(self) -> None:
        if self.logsWindow.isVisible():
            self.logsWindow.hide()
        else:
            self.logsWindow.show()

    def startFishing(self) -> None:
        self.isFishing = not (self.isFishing)
        if self.isFishing and not self.shouldStopFishing:
            self.btn_start.setObjectName("btn_red")
            self.btn_start.setText("STOP")
            self.btn_start.setToolTip("Stop fishing")
            self.isFishing = True
            self.startFishingTimer = time.time()
            self.startCheckMealTimer = time.time()
            self.startCheckPotionTimer = time.time()
            self.logsWindow.logs.append([time.localtime(), "start"])
            self.setStyleSheet(CSS)
        else:
            self.shouldStopFishing = True

    def checkShouldStopFishing(self) -> None:
        if self.shouldStopFishing:
            self.btn_start.setObjectName("btn_standart")
            self.btn_start.setText("START")
            self.btn_start.setToolTip("Start fishing")
            self.isFishing = False
            self.tryCatchFish = False
            self.logsWindow.logs.append([time.localtime(), "stop"])
            self.setStyleSheet(CSS)
            self.shouldStopFishing = False
        self.ShouldStopFishingTimer.start()

    def closeEvent(self, event) -> None:
        self.settingsWindow.close()
        self.logsWindow.close()
        self.close()

    def executeBaitAHK(self, baitType: str) -> None:
        """Execute the appropriate AHK script based on bait type."""
        # Map bait types to script filenames
        bait_scripts = {
            "Normal": "reelect_baits_normal.ahk",
            "Swarm": "reelect_baits_swarm.ahk",
            "Giant": "reelect_baits_giant.ahk",
            "Magic": "reelect_baits_magic.ahk"
        }
        
        # Default to Normal if invalid bait type
        if baitType not in bait_scripts:
            baitType = "Normal"
        
        # Construct script path using resource_path
        script_path = resource_path(os.path.join("script", bait_scripts[baitType]))
        
        # Execute AHK script
        try:
            if os.path.exists(script_path):
                subprocess.Popen([script_path], shell=True)
                time.sleep(0.1)
            else:
                print(f"Warning: AHK script not found: {script_path}")
        except Exception as e:
            print(f"Error executing AHK script: {e}")

    def fishing(self) -> None:
        while self.isVisible():
            if self.isFishing:
                self.timeForWait = time.time() - self.startFishingTimer
                self.checkMealTimer = time.time() - self.startCheckMealTimer
                self.checkPotionTimer = time.time() - self.startCheckPotionTimer
                if locateImage(IMG_START, 0.7):
                    self.tryCatchFish = True
                    self.startThisTry = time.time()
                    while self.tryCatchFish:
                        pyautogui.click(button = "left")
                        timeForThisTry = time.time() - self.startThisTry
                        if (locateImage(IMG_FISH, 0.8) or locateImage(IMG_JUNK, 0.8)) and (timeForThisTry <= self.settingsWindow.timeForTry):
                            self.endTry("fish")
                            self.addFishCount()
                        else: pyautogui.click(button = "left")
                        if locateImage(IMG_TREASURE, 0.7) and (timeForThisTry <= self.settingsWindow.timeForTry) and self.tryCatchFish:
                            self.endTry("treasure")
                            self.addFishCount()
                        else: pyautogui.click(button = "left")
                        if locateImage(IMG_SUNKEN, 0.8) and (timeForThisTry <= self.settingsWindow.timeForTry) and self.tryCatchFish:
                            self.endTry("sunken")
                            self.addFishCount()
                        else: pyautogui.click(button = "left")
                        if timeForThisTry > self.settingsWindow.timeForTry:
                            time.sleep(1)
                            self.endTry("timeError")
                        else: pyautogui.click(button = "left")

                elif self.timeForWait >= self.maxTimeForWait:
                    if locateImage(IMG_DISCONNECTED, 0.8): self.shouldStopFishing = True
                    else: self.endTry("timeError")

                elif (self.checkMealTimer >= self.settingsWindow.mealTimer) and (self.settingsWindow.useMeal):
                    # Eat meal 5 times with 1 second delay
                    keyboard.press_and_release(f"{self.settingsWindow.mealKey}")
                    for i in range(5):
                        pyautogui.click(button = "left")
                        time.sleep(1)
                    
                    # Select rod and bait
                    keyboard.press_and_release(f"{self.settingsWindow.rodKey}")
                    time.sleep(0.1)
                    self.executeBaitAHK(self.settingsWindow.baitType)
                    time.sleep(0.1)
                    pyautogui.click(button = "left")
                    
                    self.logsWindow.logs.append([time.localtime(), "consumeMeal"])
                    self.startFishingTimer = time.time()
                    self.startCheckMealTimer = time.time()
                    
                elif (self.checkPotionTimer >= self.settingsWindow.potionTimer) and (self.settingsWindow.usePotion):
                    keyboard.press_and_release(f"{self.settingsWindow.potionKey}")
                    if self.settingsWindow.potionKey != "e":
                        pyautogui.click(button = "left")
                        time.sleep(0.75)
                    
                    # Select rod and bait
                    keyboard.press_and_release(f"{self.settingsWindow.rodKey}")
                    time.sleep(0.1)
                    self.executeBaitAHK(self.settingsWindow.baitType)
                    time.sleep(0.1)
                    pyautogui.click(button = "left")
                    
                    self.logsWindow.logs.append([time.localtime(), "consumePotion"])
                    self.startFishingTimer = time.time()
                    self.startCheckPotionTimer = time.time()

                time.sleep(0.25)

    def endTry(self, log: str) -> None:
        rodKey = f"{self.settingsWindow.rodKey}"
        self.tryCatchFish = False
        self.startFishingTimer = time.time()
        self.logsWindow.logs.append([time.localtime(), log])
        time.sleep(0.2)
        keyboard.press_and_release(rodKey)
        time.sleep(0.1)
        keyboard.press_and_release(rodKey)
        time.sleep(0.1)
        # Execute bait selection AHK script
        self.executeBaitAHK(self.settingsWindow.baitType)
        time.sleep(0.1)
        pyautogui.click(button = "left")

    def addFishCount(self) -> None:
        self.fishCount += 1
        self.__countLabel.setText(f"Caught: {self.fishCount}")

    def resetFishCount(self) -> None:
        self.fishCount = 0
        self.__countLabel.setText(f"Caught: {self.fishCount}")

if __name__ == "__main__":
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()

    app = QApplication(sys.argv)
    screenSize = app.primaryScreen().geometry()

    allImagesPath = [
        resource_path('images/forScript/start.png'),
        resource_path('images/forScript/fish.png'),
        resource_path('images/forScript/treasure.png'),
        resource_path('images/forScript/junk.png'),
        resource_path('images/forScript/sunken.png'),
        resource_path('images/forScript/disconnected.png')
    ]

    actualScreenSize = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    lastUsedSize = getLastSize()
    if lastUsedSize[0] != actualScreenSize[0]:
        for i in allImagesPath:
            changeImageSize(i, actualScreenSize, lastUsedSize)
        changeLastSize(actualScreenSize)

    IMG_START = cv2.imread(allImagesPath[0])
    IMG_FISH = cv2.imread(allImagesPath[1])
    IMG_TREASURE = cv2.imread(allImagesPath[2])
    IMG_JUNK = cv2.imread(allImagesPath[3])
    IMG_SUNKEN = cv2.imread(allImagesPath[4])
    IMG_DISCONNECTED = cv2.imread(allImagesPath[5])

    window = MainWindow("Auto fishing")
    window.show()
    window.fishingThread.start()
    sys.exit(app.exec())

#  pyinstaller -w -F -i"images\icons\APP_ICON.ico" -n "auto fishing" main.py