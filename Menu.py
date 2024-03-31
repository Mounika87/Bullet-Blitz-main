import pygame

class Menu():
    def __init__(self, renderEngine, keyBindings):
        self.renderEngine = renderEngine
        self.keyBindings = keyBindings

        # contains:
        # lenght of elements to print
        # textOffset in the txt file to fetch text
        # list of elements
        self.optionList = {
            "main": [4, 0, [0,1,2,3]],
            "settings": [4, 5, [0,1,2,3]], #language, difficulty, key bindings and back to main
            "language": [len(renderEngine.getTextHandler().getLanguageList()), 10, renderEngine.getTextHandler().getLanguageList()],
            "difficulty": [3, 12, [0,1,2]],
            "keys": [len(keyBindings.getGameCurrentBindings()), 15, keyBindings.getGameCurrentBindings()],
            "selectingKey": [len(keyBindings.getGameCurrentBindings()), 15, [0,1]]
        }
        
        self.selectedOption = 0
        self.currentMenu = "main"
        self.currentKeyType = None
        self.currentKeyTypeIndex = None

        self.waitingKeyInput = False

        self.difficulty = 0
    
    def updateMenu(self, eventList):
        
        if self.currentMenu == "main":
            self.renderEngine.draw_menu_bg(True)
            self.renderEngine.draw_menu(self.selectedOption)
        else:
            self.renderEngine.draw_menu_bg(False)
            self.renderEngine.draw_settings(self.selectedOption, self.currentMenu, self.optionList, self.difficulty, self.currentKeyTypeIndex)

        
        startGame = False
        startTutorial = False
        exitGame = False

        select = False
        goBack = False
        newKey = None
        for event in eventList:
            # Event handler for Keyboard controls  
            if event.type == pygame.KEYDOWN:
                
                if self.waitingKeyInput:
                    newKey = event.key
                    select = True
                else:
                    if event.key in self.keyBindings.getMenuDefaultBindings()["left"]:
                        if (self.currentMenu == "language" or 
                                self.currentMenu == "difficulty" or 
                                self.currentMenu == "keys"):
                            goBack = True
                        if self.currentMenu == "selectingKey":
                            self.selectedOption -= 1
                    if event.key in self.keyBindings.getMenuDefaultBindings()["right"]:
                        if self.currentMenu == "settings" and self.selectedOption != 3:
                            select = True
                        if self.currentMenu == "selectingKey":
                            self.selectedOption += 1
                    if event.key in self.keyBindings.getMenuDefaultBindings()["up"]:
                        if self.currentMenu != "selectingKey":
                            self.selectedOption -= 1
                    if event.key in self.keyBindings.getMenuDefaultBindings()["down"]:
                        if self.currentMenu != "selectingKey":
                            self.selectedOption += 1
                    # only one of select and go back can be true
                    if event.key in self.keyBindings.getMenuDefaultBindings()["select"]:
                        select = True
                    elif event.key in self.keyBindings.getMenuDefaultBindings()["esc"]:
                        goBack = True
        
        self.selectedOption = self.selectedOption % len(self.optionList[self.currentMenu][2])

        if select:
            if self.currentMenu == "main":
                if self.selectedOption == 0:
                    startGame = True
                elif self.selectedOption == 1:
                    startTutorial = True
                elif self.selectedOption == 2:
                    self.currentMenu = "settings"
                    self.selectedOption = 0
                elif self.selectedOption == 3:
                    exitGame = True
        # -------------------------------------------------------------------------------------------
            elif self.currentMenu == "settings":
                if self.selectedOption == 0:
                    self.currentMenu = "language"
                    self.selectedOption = 0
                elif self.selectedOption == 1:
                    self.currentMenu = "difficulty"
                    self.selectedOption = 0
                elif self.selectedOption == 2:
                    self.currentMenu = "keys"
                    self.selectedOption = 0
                elif self.selectedOption == 3:
                    goBack = True
        # -------------------------------------------------------------------------------------------
            elif self.currentMenu == "language":
                language = self.optionList["language"][2][self.selectedOption]
                self.renderEngine.getTextHandler().setLanguage(language)
                pass
        # -------------------------------------------------------------------------------------------
            elif self.currentMenu == "difficulty":
                self.difficulty = self.selectedOption
        # -------------------------------------------------------------------------------------------
            elif self.currentMenu == "keys":
                for (i, keyBind) in zip(range(self.optionList["keys"][0]), self.optionList["keys"][2]):
                    if i == self.selectedOption:
                        self.currentKeyType = keyBind
                        self.currentKeyTypeIndex = i
                        break
                self.currentMenu = "selectingKey"
        # -------------------------------------------------------------------------------------------
            elif self.currentMenu == "selectingKey":
                self.waitingKeyInput = True
                if newKey != None:
                    self.keyBindings.setNewBinding(self.currentKeyType, self.selectedOption, newKey)
                    self.optionList["keys"][2] = self.keyBindings.getGameCurrentBindings()
                    self.waitingKeyInput = False
                    goBack = True
        
        if goBack:
            if self.currentMenu == "settings":
                self.currentMenu = "main"
                self.selectedOption = 2
            #elif (self.currentMenu == "language" or 
            #        self.currentMenu == "difficulty" or 
            #        self.currentMenu == "keys"):
            elif (self.currentMenu == "language"):
                self.currentMenu = "settings"
                self.selectedOption = 0
            elif (self.currentMenu == "difficulty"):
                self.currentMenu = "settings"
                self.selectedOption = 1
            elif (self.currentMenu == "keys"):
                self.currentMenu = "settings"
                self.selectedOption = 2
            elif (self.currentMenu == "selectingKey"):
                self.currentMenu = "keys"
                self.selectedOption = 0

        
        # inverse the boolean exit game to correspond with the value in main.py
        running = not exitGame
        return (startGame, startTutorial, running)

    def getDifficulty(self):
        return self.difficulty

    def getLanguage(self):
        return self.language