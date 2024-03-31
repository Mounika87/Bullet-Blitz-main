import pygame
import os

import EnemyAI as AI
import BombHandler as BH
import Render as Graphic
import Tutorial
from State import State as GameState
from Terrain import Terrain as TerrainHandler
from Menu import Menu
from KeyBindings import KeyBindings

from EnemyAI import EnemyHandler
 
#from pygame.sprite import _Group

# Initialising game
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.6)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), depth=32)

pygame.display.set_caption("Bullet Blitz")

# To set a frame time

clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75
LOWER_FLOOR = 500
TILE_SIZE = 64#40
TILE_TYPES = 21

# Define player actions variable
move_left = False
move_right = False
shoot = False

# Define bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

#define camera offset
camera_offsetX = 600
camera_offsetY = 0

#pick up boxes
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
item_boxes = {
	'Health'	: health_box_img,
	'Ammo'		: ammo_box_img,
}

White = (255, 255, 255)

font = pygame.font.SysFont('',30)
large_font = pygame.font.SysFont('',50)



class Soldier(pygame.sprite.Sprite):
     def __init__(self , char_type, x, y , scale, speed, ammo):  # Creating instance for the movement of characters of sprites 
         self.alive = True
         self.jump_sound = pygame.mixer.Sound('img/explosion/jump-AI.mp3')
         self.walk_sound = pygame.mixer.Sound('img/explosion/walk.mp3')
         self.char_type = char_type 
         self.speed = speed
         self.ammo = ammo
         self.start_ammo = ammo
         self.shoot_cooldown = 0
         self.health = 100
         self.max_health = self.health
         self.direction = 1
         self.vel_y = 0
         self.jump = False
         self.in_air = True
         self.flip = False
         self.animation_list = []
         self.frame_index = 0
         self.action = 0
         self.update_time = pygame.time.get_ticks()


         animation_types = ['Idle', 'Run', 'Jump', 'Death']
         for animation in animation_types:
            temp_list = []
            #Get a list of all the files in the directory
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        

         # To create a boundary tp contol the environemnt , 
         # where the image is drawn and self controls as instance 
         self.image = self.animation_list[self.action][self.frame_index]
         self.rect = img.get_rect()

         # Aligning to the cordinates
         self.rect.center = (x ,y)
         
         # initialize and sets the sensors for the characters
         self.left_sensor = pygame.Rect(x,y, 10, self.rect.height-8)
         self.left_sensor.center = self.rect.midleft
         self.right_sensor = pygame.Rect(x,y, 10, self.rect.height-8)
         self.right_sensor.center = (self.rect.right-20, self.rect.centery)
         self.bottom_sensor = pygame.Rect(self.rect.left+5, self.rect.bottom-5, self.rect.width-30, 10)

         # These instances are like blue prints,
         #  we can create as many as we want for the various actions

     def update(self):
         self.update_animation()
         self.check_alive()
         if self.shoot_cooldown > 0:
             self.shoot_cooldown -= 1

     def movement(self, move_left, move_right): # Create variables for the movements
         self.movementBase(move_left, move_right, currentTerrain)

         if move_left or move_right:
            self.walk_sound.play()
         else:
            self.walk_sound.stop()

     def movementBase(self, move_left, move_right, terrainList): # Create variables for the movements
         #set movement variables
         dx = 0
         dy = 0
        
         # will move the character left or right
         # if collision with terrain, will stop movement in the corresponding direction
         if move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
            if pygame.Rect.collidelist(self.left_sensor, terrainList) > -1:
                dx = 0
         if move_right:
             self.flip = False
             self.direction = 1
             dx = self.speed
             if pygame.Rect.collidelist(self.right_sensor, terrainList) > -1:
                dx = 0
        
         # checks if the player have collision downwards and set the vairable "self.in_air" accorddingly
         terrain_index = pygame.Rect.collidelist(self.bottom_sensor, terrainList)
         if terrain_index > -1:
            terrain = terrainList[terrain_index]
            dy = terrain.top - self.rect.bottom
            self.in_air = False
            self.vel_y = 0
         else: 
            self.in_air = True

         # Jump
         if self.jump == True and self.in_air == False:
            self.vel_y = -12
            self.jump = False
            self.in_air = True
        
        # Gravity
         if self.in_air:
            self.vel_y += GRAVITY
            if self.vel_y > 10:
                self.vel_y
            dy += self.vel_y
         
         if self.char_type == 'player2':
            #print(dy, self.rect.y, self.rect.bottom, LOWER_FLOOR, currentGameState)
            if(currentGameState == GameState.GAME and self.rect.y > LOWER_FLOOR):
                self.health = 0

         #if self.rect.bottom + dy > LOWER_FLOOR:
         #   dy = LOWER_FLOOR - self.rect.bottom
         #   self.in_air = False

        # Update rect position   
         self.rect.x += dx
         self.rect.y += dy
         
         # updates the x and y for the sensors
         self.left_sensor.x += dx
         self.left_sensor.y += dy
         self.right_sensor.x += dx
         self.right_sensor.y += dy
         self.bottom_sensor.x += dx
         self.bottom_sensor.y += dy

         if self.char_type == 'player' or self.char_type == 'player2':
            global camera_offsetX, camera_offsetY
            camera_offsetX += dx
            camera_offsetY += dy


     def jump(self):
        # Play jump sound when jumping
        self.jump_sound.play() 
            

     def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            gunSound.play()
            self.shoot_cooldown = 20 # Reload number, lower number faster speed
            bullet = Bullet(self.rect.centerx + (0.6* self.rect.size[0]* self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
    
     def update_animation(self):
        #as long as it fast enough it can update animation prefectly.
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #when animation ran out then reset it
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index =0

     def update(self):
        self.update_animation()
        self.check_alive()

        # Stop walk sound if not moving
        if not (move_left or move_right):
            self.walk_sound.stop()

     
     def update_action(self, new_action):
		#check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
			#update settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
     def check_alive(self):
         if self.health <= 0:
             self.health = 0
             self.speed = 0
             self.alive = False
             self.update_action(3)

     def draw(self): # Create methods to reduce the calling
         
          #Blit function copies image from the surface to the screen 
          # using Object Oriented Programmingm

          # tests - used to visualize the sensor of the soldiers (inlc. the player)
         #pygame.draw.rect(screen, (0,0,0), pygame.Rect((self.right_sensor.x-camera_offsetX), (self.right_sensor.y-camera_offsetY), self.right_sensor.width, self.right_sensor.height))
         #pygame.draw.rect(screen, (0,0,100), pygame.Rect((self.left_sensor.x-camera_offsetX), (self.left_sensor.y-camera_offsetY), self.left_sensor.width, self.left_sensor.height))
         #pygame.draw.rect(screen, (0,0,200), pygame.Rect((self.bottom_sensor.x-camera_offsetX), (self.bottom_sensor.y-camera_offsetY), self.bottom_sensor.width, self.bottom_sensor.height))
         #pygame.draw.rect(screen, (0,0,0), self.right_sensor)
         #pygame.draw.rect(screen, (0,0,100), self.left_sensor)
         #pygame.draw.rect(screen, (0,0,200), self.bottom_sensor)
         
         screen.blit(pygame.transform.flip(self.image, self.flip, False),
                         pygame.Rect((self.rect.x-camera_offsetX), (self.rect.y-camera_offsetY), self.rect.width, self.rect.height)) 
         #screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) 
         


class ItemBox(pygame.sprite.Sprite):
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
        # Check  collision 
		
		if pygame.sprite.collide_rect(self, player):
			#check what kind of box it was
			if self.item_type == 'Health':
				player.health += 25
				if player.health > player.max_health:
					player.health = player.max_health
			elif self.item_type == 'Ammo':
				player.ammo += 15
			self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # Bullet move forward
        self.rect.x += (self.direction * self.speed)
        # If bullet disppaer from screen then kill it 
        if self.rect.right < (0+camera_offsetX) or self.rect.left > (SCREEN_WIDTH+camera_offsetX):
            self.kill()
        # Collision check
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        #get collision of all enemies and pick out the first in the list
        listOfHitEnemies = EnemyHandler.checkSpriteCollision(bullet_group)
        if listOfHitEnemies: # check if non empty list
            hitEnemy = listOfHitEnemies[0]
            if hitEnemy.alive:
                hitEnemy.health -= 20
                self.kill()
        #if pygame.sprite.spritecollide(enemy, bullet_group, False):
        #    if enemy.alive:
        #        enemy.health -= 20
        #        self.kill()

    #def draw(self, surface):
    #    surface.blit(self.image, pygame.Rect((self.rect.x-camera_offsetX), (self.rect.y-camera_offsetY), self.rect.width, self.rect.height)) 

# Create a group for bullte 
bullet_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()







 
# player2 = Soldier(400, 200, 3) #since we have created instances, just need to specify the co ordinates
#x = 200        
#y = 200
#scale = 3 # Try to avoid a float

#TODO
keyBindings = KeyBindings()
renderEngine = Graphic.Render(pygame, screen, SCREEN_WIDTH, SCREEN_HEIGHT)
terrainHandler = TerrainHandler(pygame, screen, SCREEN_WIDTH, SCREEN_HEIGHT, LOWER_FLOOR, TILE_SIZE)
currentTerrain = terrainHandler.getGameTerrain()
menuHandler = Menu(renderEngine, keyBindings)


bombHandler = BH.ChickenBombHandler()
EnemyHandler = AI.EnemyHandler()
TutorialPlayer = Tutorial.Tutorial(screen, SCREEN_WIDTH, SCREEN_HEIGHT, renderEngine, keyBindings, terrainHandler.getTutorialTerrain())





background_size = 1376 * 2 

pygame.mixer.init()
gunSound = pygame.mixer.Sound("click.wav")

#Event handler
running = True
gameStarted = False

currentGameState = GameState.MENU
nextGameState = GameState.MENU

while running:
    
    # print(currentGameState)

    renderEngine.updateSelectedValues(gameStarted, currentGameState, nextGameState)
    renderEngine.updateCameraOffset(camera_offsetX, camera_offsetY)
    (camera_offsetX, camera_offsetY) = renderEngine.getCameraOffset()

    terrainHandler.updateTerrain(currentGameState, nextGameState)
    currentTerrain = terrainHandler.getCurrentTerrrain()
    nextTerrain = terrainHandler.getNextTerrrain()
    renderEngine.updateTerrain(currentTerrain, nextTerrain)

    if currentGameState == GameState.MENU:
        #tick camera offset to have scrolling background
        clock.tick(FPS)
        
        startGame = False
        startTutorial = False

        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                running = False

        if running:
            (startGame, startTutorial, running) = menuHandler.updateMenu(eventList)

        if startGame:
            # print("Starting game")
            nextGameState = GameState.GAME
            currentGameState = GameState.TRANSITION
            gameStarted = True
            renderEngine.disableCameraOffset(False, True)

            camera_offsetX = 600
            camera_offsetY = 0

            item_box_group.empty()
            item_box = ItemBox('Health', 800, 435)
            item_box_group.add(item_box)
            item_box = ItemBox('Ammo', 700, 435)
            item_box_group.add(item_box)


            #Creating instances with the given x,y and size co ordinates
            player = Soldier('player2', 1100, 450, 3, 5, 20)
            enemy1 = Soldier('enemy2', 1050, 250, 3, 5, 20)
            enemy2 = Soldier('enemy2', 1100, 300, 3, 5, 20)
          
            currentTerrain = terrainHandler.getGameTerrain()
            bombHandler.setup(player, screen, EnemyHandler, terrainHandler.getGameTerrain())
            EnemyHandler.setup(player, screen, terrainHandler.getGameTerrain())
            EnemyHandler.empty() # Clear any old enemies from the list
            EnemyHandler.addEnemyToList(enemy1)
            EnemyHandler.addEnemyToList(enemy2)

        if startTutorial:
            nextGameState = GameState.TUTORIAL
            currentGameState = GameState.TRANSITION
            TutorialCharacter = Soldier('player2', SCREEN_WIDTH/2, -100, 3, 5, 20)
            TutorialPlayer.startTutorial(TutorialCharacter, camera_offsetX, camera_offsetY)

        pygame.display.update()
    elif currentGameState == GameState.GAME:

        clock.tick(FPS)
        renderEngine.draw_bg()
        renderEngine.draw_terrain(currentTerrain)
        renderEngine.draw_text(f'{renderEngine.getTextFromFile("game", 0)}:{player.ammo}',font,White, 15, 20, False, False)
        renderEngine.draw_text(f'{renderEngine.getTextFromFile("game", 1)}:{player.health}',font,White, 15, 50, False, False)
    
        player.update()
        player.draw() 
        
        EnemyHandler.update()

        bombHandler.update(camera_offsetX, camera_offsetY)
        
        bullet_group.update()
        # have to blit and not call ".draw" of group as camera offset doesn't work.
        for spr in bullet_group.sprites():
            bullet_group.spritedict[spr] = screen.blit(spr.image, pygame.Rect((spr.rect.x-camera_offsetX), (spr.rect.y-camera_offsetY), spr.rect.width, spr.rect.height))

        item_box_group.update()
        # have to blit and not call ".draw" of group as camera offset doesn't work.
        for spr in item_box_group.sprites():
            item_box_group.spritedict[spr] = screen.blit(spr.image, pygame.Rect((spr.rect.x-camera_offsetX), (spr.rect.y-camera_offsetY), spr.rect.width, spr.rect.height))
        #item_box_group.draw(screen)
        



        if player.alive:
            if shoot:
                player.shoot()
            if player.in_air:
                player.update_action(2)#2: jump
            elif move_left or move_right:
                player.update_action(1)#1: run
            else:
                player.update_action(0)#0: idle
            player.movement(move_left, move_right)
        else:
            renderEngine.draw_text("Game Over", large_font, (255,255,255), 415, 490, False, False)
            # TODO: Fix parameters for game over message to less arbitrary position, and make message multi-lingual  
          

        
        for event in pygame.event.get():

            # To quit game
            if event.type == pygame.QUIT:
                running = False

            # Event handler for Keyboard controls  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # keyboard button a is set for the left movemen
                    nextGameState = GameState.MENU
                    currentGameState = GameState.TRANSITION
                    renderEngine.disableCameraOffset(False, False)
                if event.key in keyBindings.getGameCurrentBindings()["left"]: # keyboard button a is set for the left movemen
                    move_left = True    
                if event.key in keyBindings.getGameCurrentBindings()["right"]: # keyboard button b is set for the right movemen
                    move_right  = True 
                if event.key in keyBindings.getGameCurrentBindings()["shoot"]: # keyboard button SPACE is set for shooting
                    shoot  = True    
                if event.key in keyBindings.getGameCurrentBindings()["jump"] and player.alive:
                    player.jump = True
                if event.key in keyBindings.getGameCurrentBindings()["bomb"]:
                    bombHandler.spawn_chicken_bomb(player)

            # Set a release mode
            if event.type == pygame.KEYUP:
                if event.key in keyBindings.getGameCurrentBindings()["left"]:
                    move_left = False    
                if event.key in keyBindings.getGameCurrentBindings()["right"]:
                    move_right = False    
                if event.key in keyBindings.getGameCurrentBindings()["shoot"]: 
                    shoot = False  
                if event.key in keyBindings.getGameCurrentBindings()["pause"]: # set a button for esc button
                    run = False 
    
        # To update and call the image according to the rectangle  from the blit
        pygame.display.update()
    elif currentGameState == GameState.TUTORIAL:
        clock.tick(FPS)
        
        renderEngine.draw_bg()

        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                running = False

        if running:
            renderEngine.draw_terrain(currentTerrain)
            TutorialPlayer.updateTutorial(eventList)

        if TutorialPlayer.TutorialEnd:
            (camera_offsetX, camera_offsetY) = TutorialPlayer.resetTutorial()
            renderEngine.disableCameraOffset(False, False)
            nextGameState = GameState.MENU
            currentGameState = GameState.TRANSITION

        pygame.display.update()
    elif currentGameState == GameState.TRANSITION:
        clock.tick(FPS)

        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                running = False

        if running:
            renderEngine.black_Transition()
            (currentGameState, nextGameState) = renderEngine.getStates()
        pygame.display.update()
    else:
        running = False
    

pygame.quit()







