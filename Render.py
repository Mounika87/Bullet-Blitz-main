
from State import State as GameState
from TextHandler import TextHandler

import math
import codecs

class Render():
    def __init__(self, engine, screen, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.renderEngine = engine

        self.screen = screen

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        
        # variables used for title screen paralax scrolling
        self.Xsky = 0
        self.Xmountain = 0
        self.Xpine1 = 0
        self.Xpine2 = 0

        #timder used when transitioning between scen
        self.transitionTimer = 0
        self.transitionTimerMax = 120
        self.middlePotionHalf = 2

        #load text from 
        self.textHandler = TextHandler()

        self.loadImages()
        self.loadColours()
        self.loadTextFonts()
        
        #dim to make the background darker
        self.backgroundDim = engine.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.backgroundDim.set_alpha(100)
        self.backgroundDim.fill((0,0,0))

        # coordinates of drawing a star
        self.starCoordinates = []
        outerRadius = 20
        innerRadius = 10
        for i in range(5):
            x = outerRadius * math.cos((2*math.pi*i)/5 + (math.pi/2))
            y = outerRadius * math.sin((2*math.pi*i)/5 + (math.pi/2))
            self.starCoordinates.append((x,y))
            x = innerRadius * math.cos((2*math.pi*i)/5 + (math.pi/2) + (math.pi/5))
            y = innerRadius * math.sin((2*math.pi*i)/5 + (math.pi/2) + (math.pi/5))
            self.starCoordinates.append((x,y))

        #saved variable for settings menu for dislaying when not selecting anything
        self.rightSettingsMenu = "language"

        # variables updates during runtime
        self.gameStarted = False

        self.currentGameState = None
        self.nextGameState = None
        self.currentTerrain = None
        self.nextTerrain = None

        self.camera_offsetX = 0
        self.camera_offsetY = 0

        self.camera_offsetX_disabled = False
        self.camera_offsetY_disabled = False

    def loadImages(self):
        
        TILE_SIZE = 64#40
        TILE_TYPES = 21

        self.img_list = []
        for x in range(TILE_TYPES):
            img = self.renderEngine.image.load(f'img/Tile/{x}.png')
            img = self.renderEngine.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            self.img_list.append(img)

        #load images
        self.pine1_img = self.renderEngine.image.load('img/Background/pine1.png').convert_alpha()
        self.pine2_img = self.renderEngine.image.load('img/Background/pine2.png').convert_alpha()
        self.mountain_img = self.renderEngine.image.load('img/Background/mountain.png').convert_alpha()
        self.sky_img = self.renderEngine.image.load('img/Background/sky_cloud.png').convert_alpha()

        self.title_image = self.renderEngine.image.load('img/Title2.png').convert_alpha()
        self.title_img = self.renderEngine.transform.scale(self.title_image, (int(self.title_image.get_width() * 1), int(self.title_image.get_height() * 1)))
        #store tiles in a list
        self.water_img = self.renderEngine.image.load('img/tile/0.png').convert_alpha()

    def loadColours(self):
        self.BG = (255, 201, 120)
        self.White = (255, 255, 255)

    def loadTextFonts(self):
        self.font = self.renderEngine.font.SysFont('',30)
        self.large_font = self.renderEngine.font.SysFont('',50)
        self.header_font = self.renderEngine.font.SysFont('',80)



    # -------------------------------------------------------------------------------------------
    #                       Drawing Menu
    #
    # -------------------------------------------------------------------------------------------

    def draw_menu_bg(self, animated):
        self.screen.fill(self.BG)
        width = self.sky_img.get_width()
        
        increase = 1

        if animated:
            self.Xsky += increase
            self.Xmountain += increase
            self.Xpine1 += increase
            self.Xpine2 += increase

        if self.Xsky > width * 2:
            self.Xsky = 0
        if self.Xmountain > width * (1/0.6):
            self.Xmountain = 0
        if self.Xpine1 > width * (1/0.7):
            self.Xpine1 = 0
        if self.Xpine2 > width * 1.25:
            self.Xpine2 = 0

        for x in range(4):
            self.screen.blit(self.sky_img, ((x * width) - self.Xsky * 0.5, 0))
        for x in range(4):
            self.screen.blit(self.mountain_img, ((x * width) - self.Xmountain * 0.6, self.SCREEN_HEIGHT - self.mountain_img.get_height() - 300))
        for x in range(4):
            self.screen.blit(self.pine1_img, ((x * width) - self.Xpine1 * 0.7, self.SCREEN_HEIGHT - self.pine1_img.get_height() - 150))
        for x in range(4):
            self.screen.blit(self.pine2_img, ((x * width) - self.Xpine2 * 0.8, self.SCREEN_HEIGHT - self.pine2_img.get_height()))
        self.screen.blit(self.title_img, (50, 0))

    #TODO
    def draw_menu(self, selectedMenuOption):

        boxWidth = 290
        boxHeight = 43

        xPlacement = self.SCREEN_WIDTH/2 - boxWidth/2
        yPlacement = 480

        yIncrease = boxHeight + 15
        textOffset = 22

        for i in range(4):
            color = (0,0,0)
            if selectedMenuOption == i:
                color = (100,100,100)
                
            self.renderEngine.draw.rect(self.screen, color, self.renderEngine.Rect(xPlacement, yPlacement+(yIncrease*i), boxWidth, boxHeight))
        
        # draw text "start game" or "continue game" TODO
        #if self.gameStarted:
        self.draw_text(self.getTextFromFile("menu", 0), self.large_font, (255,255,255), 0, yPlacement+textOffset, True, False)
        #else:
        #    self.draw_text(self.getTextFromFile("menu", 1), self.large_font, (255,255,255), 0, yPlacement+textOffset, True, False)

        # draw text tutorial, settings and quit game
        # for loop for i: 1-3
        for i in range(1,4):
            self.draw_text(self.getTextFromFile("menu", 1+i), self.large_font, (255,255,255), 0, yPlacement+(yIncrease*i)+textOffset, True, False)
            
        """
        if self.selectedDiffuculty is not 2:
            self.renderEngine.draw.polygon(self.screen, color, [(xPlacement-30, yPlacement+(yIncrease*2)+boxHeight/2), 
                                                (xPlacement-10, yPlacement+(yIncrease*2)),
                                                (xPlacement-10, yPlacement+(yIncrease*2)+boxHeight)])
        if self.selectedDiffuculty is not 0:
            self.renderEngine.draw.polygon(self.screen, color, [(xPlacement+boxWidth+30, yPlacement+(yIncrease*2)+boxHeight/2),
                                                (xPlacement+boxWidth+10, yPlacement+(yIncrease*2)), 
                                                (xPlacement+boxWidth+10, yPlacement+(yIncrease*2)+boxHeight)])
        """
        
    def draw_settings(self, selectedMenuOption, currentMenu, optionList, currentDifficulty, currentKey):
        self.screen.blit(self.backgroundDim, (0,0))
        
        xLeftMenu = 80
        yLeftMenu = 150
        
        boxWidth = 310
        boxHeight = 43
        
        yIncrease = boxHeight + 15
        textIndent = 10
        textOffset = 5
        
        textFileOffset = optionList["settings"][1]
        self.draw_text(self.getTextFromFile("menu", textFileOffset), self.header_font, (255,255,255), 0, 100, True, True)
        for i in range(4):
            color = (0,0,0)
            if selectedMenuOption == i and currentMenu == "settings":
                color = (100,100,100)
                
            self.renderEngine.draw.rect(self.screen, color, self.renderEngine.Rect(xLeftMenu, yLeftMenu+(yIncrease*i), boxWidth, boxHeight))
            self.draw_text(self.getTextFromFile("menu", textFileOffset+1+i), self.large_font, (255,255,255), 
                            xLeftMenu+textIndent, yLeftMenu+(yIncrease*i)+textOffset, False, False)
        
        
        xRightMenu = 450
        yRightMenu = 150
        
        boxWidth = 270

        if currentMenu == "settings":
            if selectedMenuOption == 0:
                self.rightSettingsMenu = "language"
            elif selectedMenuOption == 1:
                self.rightSettingsMenu = "difficulty"
            elif selectedMenuOption == 2:
                self.rightSettingsMenu = "keys"
        else:
            self.rightSettingsMenu = currentMenu


        length = optionList[self.rightSettingsMenu][0]
        textFileOffset = optionList[self.rightSettingsMenu][1]
        
        rightList = optionList[self.rightSettingsMenu][2]
        if self.rightSettingsMenu == "selectingKey":
            rightList = optionList["keys"][2]

        for (i, arr) in zip(range(length), rightList):
            color = (0,0,0)

            if currentMenu == "selectingKey" and currentKey == i:
                color = (100,100,100)
            if selectedMenuOption == i and currentMenu != "settings" and currentMenu != "selectingKey":
                color = (100,100,100)
            
            if ((self.rightSettingsMenu == "language" and arr == self.textHandler.getLanguage()) or
                    (self.rightSettingsMenu == "difficulty" and arr == currentDifficulty)):
                xStar = xRightMenu
                yStar = yRightMenu + yIncrease*i
                drawStar = []
                for (x,y) in self.starCoordinates:
                    drawStar.append((x+xStar, y+yStar))
                self.renderEngine.draw.polygon(self.screen, (255,255,0), drawStar)
                
            self.renderEngine.draw.rect(self.screen, color, self.renderEngine.Rect(xRightMenu, yRightMenu+(yIncrease*i), boxWidth, boxHeight))
            self.draw_text(self.getTextFromFile("menu", textFileOffset+i), self.large_font, (255,255,255), 
                            xRightMenu+textIndent, yRightMenu+(yIncrease*i)+textOffset, False, False)
        

        boxWidth = 150
        if self.rightSettingsMenu == "keys" or self.rightSettingsMenu == "selectingKey":
            for (i, arr) in zip(range(length), optionList["keys"][2].values()):
                
                boxOffset = 160
                for j in range(2):
                    color = (0,0,0)
                    if selectedMenuOption == j and i == currentKey and currentMenu == "selectingKey":
                        color = (100,100,100)
                    
                    self.renderEngine.draw.rect(self.screen, color, 
                            self.renderEngine.Rect(xRightMenu+280+boxOffset*j, yRightMenu+(yIncrease*i), boxWidth, boxHeight))

                    if arr[j] == None:
                        txt = ""
                    else:
                        txt = self.renderEngine.key.name(arr[j])
                    self.draw_text(txt, self.large_font, (255,255,255), 
                                xRightMenu+textIndent+280+160*j, yRightMenu+(yIncrease*i)+textOffset, False, False)
                


    # -------------------------------------------------------------------------------------------
    #                       Drawing Game
    # -------------------------------------------------------------------------------------------

    #TODO
    def draw_bg(self):
        self.screen.fill(self.BG)
        width = self.sky_img.get_width()
        for x in range(5):
            self.screen.blit(self.sky_img, ((x * width) - self.camera_offsetX * 0.5, 0))
            self.screen.blit(self.mountain_img, ((x * width) - self.camera_offsetX * 0.6, self.SCREEN_HEIGHT - self.mountain_img.get_height() - 300))
            self.screen.blit(self.pine1_img, ((x * width) - self.camera_offsetX * 0.7, self.SCREEN_HEIGHT - self.pine1_img.get_height() - 150))
            self.screen.blit(self.pine2_img, ((x * width) - self.camera_offsetX * 0.8, self.SCREEN_HEIGHT - self.pine2_img.get_height()))

    #TODO
    #def draw_terrain(self, terrain_list):
    def draw_terrain(self, terrain_list):
        for terrain in terrain_list:
            self.drawTerrainForRect(terrain, True)

            #pygame.draw.rect(screen, White, pygame.Rect((terrain.x-camera_offsetX), (terrain.y-camera_offsetY), terrain.width, terrain.height))
        #pygame.draw.rect(screen, White, ground_platform)
        #pygame.draw.rect(screen, (0,0,255), upper_platform)
        #pygame.draw.rect(screen, (0,255,0), second_platform)

    #TODO
    def drawTerrainForRect(self, rect, withEdge):
        height = self.img_list[0].get_height()
        width = self.img_list[0].get_width()
        amount_height = math.ceil(rect.height / height)
        amount_width = math.ceil(rect.width / width)
            
        StartX = rect.x
        StartY = rect.y
        if withEdge:
            for x in range(1, amount_width-1):
                self.screen.blit(self.img_list[0], (StartX + x*width - self.camera_offsetX, 
                                        StartY - self.camera_offsetY))
                for y in range(1, amount_height):
                    self.screen.blit(self.img_list[4], (StartX + x*width - self.camera_offsetX, 
                                            StartY + y*height - self.camera_offsetY))
            self.screen.blit(self.img_list[1], (StartX - self.camera_offsetX, 
                                    StartY - self.camera_offsetY))
            self.screen.blit(self.img_list[2], (StartX + (amount_width-1)*width - self.camera_offsetX, 
                                    StartY - self.camera_offsetY))
            for y in range(1, amount_height):
                self.screen.blit(self.img_list[3], (StartX - self.camera_offsetX, 
                                        StartY + y * height - self.camera_offsetY))
                self.screen.blit(self.img_list[5], (StartX + (amount_width-1)*width - self.camera_offsetX, 
                                        StartY + y * height - self.camera_offsetY))
        else:
            for x in range(amount_width):
                self.screen.blit(self.img_list[0], (StartX + x*width - self.camera_offsetX, 
                                        StartY - self.camera_offsetY))
                for y in range(1, amount_height):
                    self.screen.blit(self.img_list[4], (StartX + x*width - self.camera_offsetX, 
                                            StartY + y*height - self.camera_offsetY))

    #TODO
    def black_Transition(self):
        #global transitionTimer, currentGameState, nextGameState, camera_offsetX, camera_offsetY

        self.transitionTimer += 1

        blackBackground = self.renderEngine.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        blackBackground.fill((0,0,0))
        alpha = 255
        firstHalf = (self.transitionTimerMax/2-self.middlePotionHalf)
        secondHalf = (self.transitionTimerMax/2+self.middlePotionHalf)

        if self.transitionTimer < firstHalf:
            alpha = (self.transitionTimer/firstHalf)*255
        elif self.transitionTimer > secondHalf:
            if self.nextGameState == GameState.MENU:
                self.draw_menu_bg(True)
                self.draw_menu(-1)
            elif  self.nextGameState == GameState.TUTORIAL:
                self.updateCameraOffset(0, 0)
                self.disableCameraOffset(True, True)
                self.draw_bg()
                self.draw_terrain(self.nextTerrain)
                #TutorialPlayer.updateTutorialTerrain()
            else:
                self.transitionTimer = self.transitionTimerMax+1
            alpha = ((self.transitionTimerMax-self.transitionTimer)/secondHalf)*255
        else:
            self.screen.fill((0,0,0))
        blackBackground.set_alpha(alpha)
        self.screen.blit(blackBackground, (0,0))

        if self.transitionTimer > self.transitionTimerMax:
            self.currentGameState = self.nextGameState
            self.transitionTimer = 0




    """
    def draw_text(self, text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        self.screen.blit(img, (x, y))
    
    #TODO
    """
    def draw_text(self, text, font, text_color, x, y, centerScreen, outLine):
        img = font.render(text, True, text_color)
        img_rect = (x,y)
        if centerScreen:
            img_rect = img.get_rect(center=(self.SCREEN_WIDTH/2, y))
        if outLine:
            for (offsetX, offsetY) in [(0,2),(0,-2),(2,0),(-2,0),(1,1),(-1,-1),(1,-1),(-1,1)]:
                outlineIMG = font.render(text, True, (0,0,0))
                outLine_rect = img.get_rect(center=(self.SCREEN_WIDTH/2+offsetX, y+offsetY))
                self.screen.blit(outlineIMG, outLine_rect)
        self.screen.blit(img, img_rect)
    

    def getTextFromFile(self, file, index):
        returnText = self.textHandler.getTextFile(file)[index]
        """
        if index == 0 or index == 1:
            returnText = self.TextList[index]
        else:
            textIndex = index + self.selectedLanguage * 9
            returnText = self.TextList[textIndex]
        """
        return returnText[:-2]

    def updateTerrain(self, currentTerrain, nextTerrain):
        self.currentTerrain = currentTerrain
        self.nextTerrain = nextTerrain

    def updateSelectedValues(self, gameStarted, currentGameState, nextGameState):
        self.gameStarted = gameStarted

        self.currentGameState = currentGameState
        self.nextGameState = nextGameState
    
    def updateCameraOffset(self, camera_offsetX, camera_offsetY):
        if not self.camera_offsetX_disabled:
            self.camera_offsetX = camera_offsetX
        if not self.camera_offsetY_disabled:
            self.camera_offsetY = camera_offsetY
    
    def disableCameraOffset(self, X_axis, Y_axis):
        self.camera_offsetX_disabled = X_axis
        self.camera_offsetY_disabled = Y_axis

    def getCameraOffset(self):
        return (self.camera_offsetX, self.camera_offsetY)

    def getStates(self):
        return (self.currentGameState, self.nextGameState)

    def getTextHandler(self):
        return self.textHandler