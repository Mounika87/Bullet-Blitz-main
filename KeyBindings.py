
import pygame

class KeyBindings():
    def __init__(self):

        self.menuDefaultValue = {
            "left": [pygame.K_LEFT, pygame.K_a],
            "right": [pygame.K_RIGHT, pygame.K_d],
            "up": [pygame.K_UP, pygame.K_w],
            "down": [pygame.K_DOWN, pygame.K_s],
            "select": [pygame.K_RETURN, pygame.K_SPACE],
            "esc": [pygame.K_ESCAPE, None]
        }
        self.gameDefaultValue = {
            "left": [pygame.K_LEFT, pygame.K_a],
            "right": [pygame.K_RIGHT, pygame.K_d],
            "jump": [pygame.K_UP, pygame.K_w],
            "shoot": [pygame.K_SPACE, None],
            "bomb": [pygame.K_b, None],
            "pause": [pygame.K_ESCAPE, None]
        }
        self.gameCurrentValue = self.gameDefaultValue

    def getMenuDefaultBindings(self):
        return self.menuDefaultValue

    def getGameCurrentBindings(self):
        return self.gameCurrentValue

    #only supports game bindings
    def setNewBinding(self, type, index, key):
        #If any keybindings is using the newly selected key
        # remove itself from the list and replace with None
        for gameKeys in self.gameCurrentValue.values():
            for i in range(2):
                if gameKeys[i] == key:
                    gameKeys[i] = None
        
        self.gameCurrentValue[type][index] = key


