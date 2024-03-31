from State import State as GameState

class Terrain():
    def __init__(self, engine, screen, SCREEN_WIDTH, SCREEN_HEIGHT, LOWER_FLOOR, TILE_SIZE):
        self.renderEngine = engine

        self.screen = screen

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.LOWER_FLOOR = LOWER_FLOOR
        self.TILE_SIZE = TILE_SIZE #64

        self.gameTerrain = None
        self.tutorialTerrain = None

        self.currentTerrain = None
        self.nextTerrain = None

        self.generateTerrain()

    def generateTerrain(self):
        
        upper_platform = self.renderEngine.Rect(1600, 400, 192, self.TILE_SIZE)
        ground_platform = self.renderEngine.Rect((-100, self.LOWER_FLOOR), (self.SCREEN_WIDTH*3, self.SCREEN_HEIGHT-400))
        second_platform = self.renderEngine.Rect((1300, 450), (640, self.TILE_SIZE))
        right_wall = self.renderEngine.Rect((0, 200), (576, 300))

        self.gameTerrain = [upper_platform, second_platform, right_wall, ground_platform]

        self.platformEdge = 14
        floorLevel = self.SCREEN_HEIGHT - (64 * 1)
        floor = self.renderEngine.Rect((0, floorLevel), (self.SCREEN_WIDTH, self.SCREEN_HEIGHT-floorLevel))
        rightPlatform = self.renderEngine.Rect((64*self.platformEdge, floorLevel-64), (64*self.platformEdge, self.SCREEN_HEIGHT-floorLevel))
        leftWall = self.renderEngine.Rect((-10, 0), (10, self.SCREEN_HEIGHT))
        rightWall = self.renderEngine.Rect((self.SCREEN_WIDTH, 0), (10, self.SCREEN_HEIGHT))
        test = self.renderEngine.Rect((200, 200), (256, 256))

        #self.tutorialTerrain = [floor, rightPlatform, test, leftWall, rightWall]
        self.tutorialTerrain = [floor, rightPlatform]

    def updateTerrain(self, currentGameState, nextGameState):
        if currentGameState == GameState.GAME:
            self.currentTerrain = self.gameTerrain
        elif currentGameState == GameState.TUTORIAL:
            self.currentTerrain = self.tutorialTerrain

        if nextGameState == GameState.GAME:
            self.nextTerrain = self.gameTerrain
        elif nextGameState == GameState.TUTORIAL:
            self.nextTerrain = self.tutorialTerrain
        
    def getCurrentTerrrain(self):
        return self.currentTerrain

    def getNextTerrrain(self):
        return self.nextTerrain

    def getGameTerrain(self):
        return self.gameTerrain

    def getTutorialTerrain(self):
        return self.tutorialTerrain