#####This module contains all functions needed to run this program, except for####
##### functions using an object of class "Urn", which are in the main module######
#####Do not run this module to run the program. To run the program, run the module entitled "MainCode" ##########

#import necessary functions from other modules
from random import choice, randint, choices
from os import listdir
from GUIandCustomWidgets import *

#Access the directory for later functions and set up a timer for use in animations
results=listdir()
timer=QTimer()

#This function turns the page
def nextPage ():
    currentPage = ui.exprmtStackedWdgt.currentIndex()
    ui.exprmtStackedWdgt.setCurrentIndex(currentPage+1)

#This function connects a list of clicked buttons to the nextPage function
def connectToNextPage(buttonUI):
    buttonUI.clicked.connect(nextPage)

#This function hides labels
def hideThisLabel(label):
    label.hide()

#This function checks that consent has been given
def checkConsent():
    if ui.consentCheckBx.isChecked()==True and ui.noConsentCheckBx.isChecked()==False:
        nextPage()
    else:
        ui.noConsentMsg.show()

#This function hides the flashing labels after they appear
def hideFlashingLabel():
    ui.loseLbl.hide()
    ui.winLbl.hide()

#This function displays the correct error labels for the demographics page
def showErrorMessage(errorLabel, errorFieldLabel, text):
    errorFieldLabel.setText("Please indicate your "+ text + " before submitting")
    errorFieldLabel.show()
    errorLabel.show()

#These functions check that all fields in the demographics page are filled out properly
def checkDemographics():
    if ui.ageSpinBox.value() == 0:
        showErrorMessage(ui.demogErrorLbl, ui.demogErrorFieldLbl, "age")
    elif ui.ageSpinBox.value() <18:
        ui.demogErrorFieldLbl.setText ("Sorry, you must be over 18 years of age to participate.")
        ui.demogErrorFieldLbl.show()
    elif ui.EduComboBx.currentIndex()==0:
        showErrorMessage(ui.demogErrorLbl, ui.demogErrorFieldLbl, "education")
    elif ui.maleWidg.isChecked() == False and ui.femaleWidg.isChecked() == False and ui.nonBinaryWidg.isChecked()==False:
        showErrorMessage(ui.demogErrorLbl, ui.demogErrorFieldLbl, "gender")
    elif ui.ageSpinBox.value() == 0 and ui.EduComboBx.currentIndex()==0 and ui.maleWidg.isChecked() == False and ui.femaleWidg.isChecked() == False:
        showErrorMessage(ui.demogErrorLbl, ui.demogErrorFieldLbl,"information")
    else:
        nextPage()
def recordGender ():
    if ui.maleWidg.isChecked()==True:
        gender="male"
        return gender
    if ui.femaleWidg.isChecked()==True:
        gender="female"
        return gender
    if ui.nonBinaryWidg.isChecked()==True:
        gender="nonbinary"
        return gender

#This class creates an Urn object with a set number of balls. It assigns the balls number so that each condition
#will have equal number of balls by accessing the previous trials from the csv. If it is the first trial, it creates
#a csv. It then creates a random distribution for the random urn and assigns which urn is random
#The "randomUrnPlacementInstructions" method changes the instruction label to reflect the trial conditions
#The "result" method randomly picks a ball once the user has clicked on an urn
#"addToCSV" method adds the full line to the CSV at the end of the trial
#"addToLine" method adds pieces of data to the line that will eventually be added to the CSV
#In order to add or change the ball conditions, modifications need to be made to Urn def_init_self()
class Urn:
    def __init__(self):
        #initialise the conditions and count of participants per condition
        self.conditionPossibilities = [2, 10, 100]
        self.conditionsDictionary = {2: 0, 10: 0, 100: 0}
        self.HundredCondition=0
        self.TwoCondition = 0
        self.TenCondition = 0
        self.directory=listdir()          #Check the directory for the csv recording trials
        self.headers="ID,Age, Gender, Education, Ball Condition, Urn Position, Urn Choice, Marble Color "
        if "Output.csv" not in self.directory: #If the csv does not exist yet, write the headers.
            file = open("Output.csv", "w")
            file.write(self.headers + "\n")
            file.close()
        file=open("Output.csv", "r")
        linesofCSV=file.readlines()  #If it exists, count the lines in order to assign the current participant an ID number "ui.prtcpntIDAssignmtLbl")
        self.lineCounter=0
        for line in linesofCSV:
            self.lineCounter+=1
        file.close()
        ui.prtcptntIDAssignmtLbl.setText(str(self.lineCounter))
        #Count the number of participants who have already participated in each condition. Record this number in both a dictionary and a counter.
        #Both data structures are used because they are useful in different ways in the coming code
        #The counters are then made into a list which is sorted from lowest to highest in order to determine which conditions require more participants
        #The dictionary is used to compare the number of participants across conditions more easily
        for line in linesofCSV:
            line = line.strip("\n").split(",")
            if line[4] == "100":
                self.conditionsDictionary[100] += 1
                self.HundredCondition+=1
            elif line[4] == "10":
                self.conditionsDictionary[10] += 1
                self.TenCondition+=1
            elif line[4] == "2":
                self.conditionsDictionary[2] += 1
                self.TwoCondition+=1
        self.listOfConditions = [self.HundredCondition, self.TenCondition, self.TwoCondition]
        #if all conditions have equal numbers of participants, choose a condition randomly
        if self.conditionsDictionary[100]==self.conditionsDictionary[10]==self.conditionsDictionary[2]:
                self.balls = choice(self.conditionPossibilities)
        else:
            #these lines check which condition(s) have fewest participants by using the sorted list and the dictionary of conditions and trials
            sortedConditions=sorted(self.listOfConditions)
            item1 = sortedConditions[0]
            item2 = sortedConditions[1]
            for item in self.conditionsDictionary:
                if self.conditionsDictionary[item]==item1:      #identifies which condition had the fewest participants
                    firstNumber=item
                if self.conditionsDictionary[item]==item2:      #identifies which condition had the second fewest participants
                    secondNumber=item
            if sortedConditions[0]==sortedConditions[1]:  #if two conditions had equal numbers of participants and that number was less than another condition
                self.balls=choice([firstNumber,secondNumber]) #choose randomly between the two conditions with fewer participants
            else:
                self.balls=firstNumber #if one condition had fewer participants than all other conditions, assign the current participant to that condition
        self.ballColors = ["blue", "red"]
        self.randomBlueBalls = randint(0, self.balls) #choose a random number of blue balls somewhere between zero and the number of total balls
        self.randomRedBalls = self.balls - self.randomBlueBalls #the number of red balls in the random/ambiguous condition equals the number of balls total minus the randomly asisgned blue balls
        self.randomUrnOptions=["Urn A", "Urn B"]
        self.whichUrnIsRandom=choice(self.randomUrnOptions) #randomly choose which urn will be the random/ambiguous distribution
        self.lineInCSV = "" #initialise the csv line
    def randomUrnPlacementInstructions(self, instructionLabel): #this method modifies the instructions displayed based on the assigned ball condition
        if self.whichUrnIsRandom == "Urn A":
            equalUrn = "Urn B"
            ambiguousUrn = "Urn A"
        else:
            equalUrn = "Urn A"
            ambiguousUrn = "Urn B"
        halfBallNumber = str(int(self.balls / 2))
        revisedInstructions = "\n\n" + equalUrn + "  contains " + halfBallNumber + " red and " + halfBallNumber + " blue marbles. " + ambiguousUrn + " contains " + str(
            self.balls) + " marbles in an unknown color ratio, from " + str(
            self.balls) + " red marbles and 0 blue marbles to 0 red marbles and " + str(
            self.balls) + " blue marbles. \n\nThe mixture of red and blue marbles in " + ambiguousUrn + " has been decided by writing the numbers 0, 1, . . .,"+ str(self.balls)+ " on separate slips of paper, shuffling the slips thoroughly, and then drawing one of them at random.The number chosen was used to determine the number of blue marbles to be put into " + ambiguousUrn+ ", but you do not know the number. Every possible mixture of red and blue marbles in "+ ambiguousUrn+ " is equally likely. \n\nYou have to decide whether you prefer to draw a marble at random from Urn A or Urn B. What you hope is to draw a blue marble and be entered for the £30 lottery draw. \n\nConsider very carefully from which urn you prefer to draw the marble, then press Continue, which will lead you to the next screen. On the next screen you will draw a marble from your chosen urn by clicking that urn's button. Press Continue when you are ready to make your choice.\n"
        instructionLabel.setText(revisedInstructions)
        return ambiguousUrn #the function returns which urn is random/ambiguous
    def result (self, winLabel, loseLabel, ambiguous=True): #this method picks a ball from the chosen urn and displays the result
        if ambiguous==True:
            self.pickABallAmbiguous=choices(self.ballColors, weights=[self.randomBlueBalls, self.randomRedBalls], k=1) #random choice from the ambiguous distribution
            if self.pickABallAmbiguous==["blue"]: #display win label and animation if a blue ball is picked
                ui.winLbl.show()
                ui.blueBallHappyLbl.show()
                timer.start(45)
                timer.timeout.connect(moveBlue)
                self.addToLine("blue")
            else:
                ui.redBallAngryLbl.show() #display lose label and animation if a red ball is picked
                ui.loseLbl.show()
                timer.start(45)
                timer.timeout.connect(moveRed)
                self.addToLine("red")
        else:
            pickABallFiftyFifty=choices(self.ballColors, weights=[50,50], k=1) #random choice from the fifty-fifty distribution
            if pickABallFiftyFifty==["blue"]: #display win label and animation if a blue ball is picked
                ui.blueBallHappyLbl.show()
                timer.start(45)
                timer.timeout.connect(moveBlue)
                self.addToLine("blue")
                ui.winLbl.show()
            else:
                self.addToLine("red") #display win label and animation if a red ball is picked
                ui.redBallAngryLbl.show()
                timer.start(45)
                timer.timeout.connect(moveRed)
                ui.loseLbl.show()
    def addToLine(self,addition): #this method adds to the line to be added to the csv
        self.lineInCSV += addition + ","
        return (self.lineInCSV)
    def addToCSV (self,contents, file="Output.csv"): #this method writes the csv
        CSVOpened=open (file, "a")
        CSVOpened.write(contents+"\n")
        CSVOpened.close()

def endTrial (): #this function ends the trial by closing the window
    window.close()

