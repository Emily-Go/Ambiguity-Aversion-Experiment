########This module contains the code that is not functions stored in the "Functions" module or customized widgets in the "GUIandCustomWidgets" module#################################################################
#########This is the module to be run in order to run the experiment###################################
            #Apart from this file, it also requires Assessment2Colours.ui, Assessment2Colours.py, GUIandCustomWidgets.py,
            #Functions.py. blueBallface.png, redBallFace.png, uniofleicesterlogo.png,
            #and urnImage.png to be in the same directory
            #Running this module will open the experiment window for participants to use


#import from random, the Functions module, and the module holding the GUI import commands/custom widgets
import random
from Functions import *
from GUIandCustomWidgets import *

#This list and function hide the error messages and other labels that need to be hidden at the start of the program
listOfLabels=[ui.noConsentMsg, ui.demogErrorFieldLbl, ui.demogErrorLbl, ui.redBallAngryLbl, ui.blueBallHappyLbl]
for label in listOfLabels:
    hideThisLabel(label)

#Create an urn object using the urn class in "Functions"
myUrn=Urn()
window.lineInCSV = ""

#The functions below use the object "myUrn" of the class "Urn" and are therefore left in this module instead of the "Functions" module
#This function calls the Urn method "addToCSV", found in the Functions mdodule, which adds a line to the CSV file
def writeCSVLine():
    myUrn.addToCSV(myUrn.lineInCSV)

#This function identifies which urn the user chose, records this information for later csv writing using the urn method "addToLine", calls the urn's result generation method, and chooses the correct result label based on outcome
def pickedUrn():
    whichButtonClicked=window.sender()
    if whichButtonClicked.text()==myUrn.whichUrnIsRandom:
        myUrn.addToLine(str(0)) #if the user chooses the random/ambiguous urn, it is coded in the csv as "0"
        myUrn.result(ui.winLbl, ui.loseLbl)
    else:
        myUrn.addToLine(str(1)) #if the user chooses the known 50-50 distribution urn, it is coded in the csv as "1"
        myUrn.result(ui.winLbl, ui.loseLbl, ambiguous=False)

#This function records which urn had the random distribution and uses the urn method "addToLine" to store trial information in the line that will be written to the csv
def myDemographics(ambiguousUrn):
    if myUrn.randomUrnPlacementInstructions(ui.instrctnLbl)=="Urn A":
        randomUrnCsv=str(1) #if Urn A is random/ambiguous, it is coded in the csv as "1"
    else:
        randomUrnCsv=str(0) #if Urn B is random/ambiguous, it is coded in the csv as "0"
    demogList=[str(myUrn.lineCounter), str(ui.ageSpinBox.value()), recordGender(), ui.EduComboBx.currentText(), str(myUrn.balls), randomUrnCsv]
    for item in demogList:
        myUrn.addToLine(item)

#These lines connect all navigation buttons to the connectToNextPage function (found in the "Functions" module or to conditional next page functions
#Both "checkConsent" and "checkDemographics" are in the "Functions" module
#myDemographics and pickedUrn are in this module because they use the "myUrn" object
#This loop connects a list of buttons to the connectToNextPage function
listOfButtons=[ui.nxtBtn, ui.ContinueBtn, ui.urnAPushBtn, ui.urnBPushBtn, ui.proceedPushBtn]
for button in listOfButtons:
    connectToNextPage(button)
ui.consentSubmitPushBtn.clicked.connect(checkConsent)
ui.demogSubmitPushBtn.clicked.connect(checkDemographics)
ui.nxtBtn.clicked.connect(myDemographics)
ui.urnAPushBtn.clicked.connect(pickedUrn)
ui.urnBPushBtn.clicked.connect(pickedUrn)
ui.proceedPushBtn.clicked.connect(writeCSVLine)
ui.proceedPushBtn.clicked.connect(hideFlashingLabel)
ui.finishPushBtn.clicked.connect(endTrial)

window.show()
sys.exit(app.exec_())
