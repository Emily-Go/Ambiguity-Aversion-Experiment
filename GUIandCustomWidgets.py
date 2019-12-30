#######################################################################
##########This module contains the GUI commands########################
##########The module is then imported into other modules for use#######
##########Do not run this module to run the program.###################
########## To run the program, run the module entitled "MainCode" #####


#import from random and the "Functions" module for later use
import random
from Functions import *

#Set up the GUI
import sys
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*
from Assessment2Colours import*
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

#Set up the windowed application
app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

#The class colouredLabel is for creating a coloured label with methods that allow it to blink with a timer
#The "blink" method sets the blink colors and frequency
#The "onBlink" method does the actual blinking
#This class is then called into other modules in the program for use
class colouredLabel(QLabel):
    def setColour(self, colorString):
        self.setAutoFillBackground(True)
        myPalette = self.palette()
        myPalette.setColor(QPalette.Window, QColor(colorString))
        self.setPalette(myPalette)
    def blink(self, color1, color2):
        self.blinkColour1 = color1
        self.blinkColour2 = color2
        self.currentColour = color1
        self.blinkTimer = QTimer()
        self.blinkTimer.timeout.connect(self.onBlink)
        self.blinkTimer.start(500)
    def onBlink(self):
        if self.currentColour == self.blinkColour1:
            self.currentColour = self.blinkColour2
        else:
            self.currentColour = self. blinkColour1
        self.setColour(self.currentColour)

#This is a general function that animates/moves labels across the screen
def move(labelName):
    currentX=labelName.x()
    labelName.setGeometry(currentX+5, 90, 241, 191)
    if currentX==750:
        currentX = labelName.x()-800
        labelName.setGeometry(currentX + 5, 90, 241, 191)

#These are the objects made from class colouredLabel and the commands using the"move" function used in this program

#These lines make a "lose label" that is of class "coloured Label", has a lose message, and blinks
ui.loseLbl = colouredLabel(window)
ui.loseLbl.setText("Sorry, you drew a red ball.")
ui.loseLbl.setAlignment(QtCore.Qt.AlignCenter)
newFont = QFont ("Calibri", 18)
ui.loseLbl.setFont(newFont)
ui.loseLbl.setGeometry(250, 20, 300, 40)
ui.loseLbl.blink("red", "white")
ui.loseLbl.hide()

#These lines make a "win label" that is of class "coloured Label", has a win message, and blinks
ui.winLbl=colouredLabel(window)
ui.winLbl.setText("You got a blue ball and will be entered into the lottery!")
ui.winLbl.setAlignment(QtCore.Qt.AlignCenter)
newFont = QFont ("Calibri", 18)
ui.winLbl.setFont(newFont)
ui.winLbl.setGeometry(250, 20, 300, 40)
ui.winLbl.setWordWrap(True)
ui.winLbl.blink("Deepskyblue", "white")
ui.winLbl.hide()

#This is a specific function that connects the red ball picture label with the move function so that it animates/moves across the screen
def moveRed(label=ui.redBallAngryLbl):
    move(label)
#This is a specific function that connects the blue ball picture label with the move function so that it animates/moves across the screen
def moveBlue (label=ui.blueBallHappyLbl):
    move(label)
