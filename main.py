import pygame
from random import randint
from time import perf_counter
from info import scale, max_score
from materials.coin import coin
from materials.grass import grass
from materials.dirt import dirt
from materials.cloud import cloud
from materials.air import air
"""
        NOTES FOR FUTRE ME
        CANNOT JUMP WHILE CROUCHED -> REASON TO BE UNCROUCHED
        GET JUMPING WORKING
        HAVE A GOAL -> TIME TO GET N COINS?
        FIX YELLOW
"""

pygame.init()

level = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,2,2,2,0],
    [0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,2,3,3,3,2],
    [0,0,0,0,0,0,2,2,2,0,0,4,4,0,0,2,3,3,3,3,3],
    [0,0,0,0,0,0,0,0,0,0,0,2,2,0,2,3,3,3,3,3,3],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3]
]

start = perf_counter()

board_size = (len(level[0]),len(level))
print(board_size)

height_original = board_size[0]
width_original = board_size[1]

X = width_original*scale
Y = height_original*scale

display_surface = pygame.display.set_mode((Y, X))

# set the pygame window name
pygame.display.set_caption('Ascii game')

class player:
    def __init__(self):
        self.x = 8
        self.y = 3
        self.score = 0
        self.height = 2
        self.jump_count = 0
        self.crouch = False
        self.max_jump_count = 10
        self.jumping = False
        self.lower = pygame.image.load(f"./sprites/character/lower_{scale}.png")
        self.upper = pygame.image.load(f"./sprites/character/upper_{scale}.png")
        self.left_key = pygame.K_LEFT
        self.right_key = pygame.K_RIGHT
        self.up_key = pygame.K_UP
        self.down_key = pygame.K_DOWN
        self.crouch_key = pygame.K_LCTRL

    def gravity(self):
        valid = player.valid_position(self.x,self.y,True, -1, self)
        print(valid)
        if valid:
            self.y -= 1
            return True
        if not valid:
            return False
    def jump(self):
        print(self.jump_count)
        if self.jump_count  >= 10:
            if self.valid_position(self.x, self.y, True, +1, self):
                self.y += 1
            
        else:
            if not self.gravity():
                self.jumping = False
                print("AHHHHHHHHHHHHH")
        self.jump_count += 1
        if self.jump_count == self.max_jump_count:
            self.jumping = False
            self.jump_count = 0
        

    @staticmethod
    def valid_position(x,y, vertical, difference, character):
        if vertical: #this is somehow working
            y += difference
            yellow = pygame.image.load(f"./sprites/yellow_{scale}.png")

            factor = 0
            if character.crouch and difference > 0:
                factor = 1

            display_surface.blit(yellow, ((((board_size[0] - character.x))*scale),((board_size[1] -y+factor)*scale)))
            if x > 0 and x-1 <= board_size[0] and y > 0 and y + factor <= board_size[1]+2:
                for material in materials:
                    if material.value == level[board_size[1] -y+factor][(board_size[0] - character.x)]:
                        if (material.solid):
                            return False
                        
                        if material in collectable:
                            material.on_collection(character)
                            level[board_size[1] -y +factor][(board_size[0] - character.x)] = air.value
                        return True
            return False
        if not vertical: #this is not
            print(x,y)
            if x+difference > 0 and x+difference <= board_size[0]:
                yellow = pygame.image.load(f"./sprites/yellow_{scale}.png")
                new_foot_material = (level[board_size[1] -y][board_size[0] - x-difference])
                new_head_material = (level[board_size[1] -y-character.height+1][board_size[0] - x-difference])
                display_surface.blit(yellow, ((((board_size[0] - x-difference))*scale),((board_size[1] -y)*scale)))
                if not character.crouch:
                    display_surface.blit(yellow, ((((board_size[0] - x-difference))*scale),((board_size[1] -y-character.height+1)*scale)))

                for material in materials:
                    if material in solid_materials:
                        if new_foot_material == material.value:
                            return False
                        if new_head_material == material.value and not character.crouch:
                            return False
                    if material in collectable:
                        if new_foot_material == material.value:
                            material.on_collection(character)
                            print(board_size[0] - difference -x)
                            level[board_size[1] -y][board_size[0] - x-difference] = 0
                            return True
                        if new_head_material == material.value and not character.crouch:
                            material.on_collection(character)
                            print(level[board_size[1] -y-character.height+1][board_size[0] - x-difference])
                            level[board_size[1] -y-character.height+1][board_size[0] - x-difference] = 0
                            return True
                return True
            return False

materials = [cloud, air, dirt, grass, coin]
solid_materials = [dirt, grass]
non_solid_materials = [air, cloud, coin]
collectable = [coin]
# create a surface object, image is drawn on it.

# infinite loop
character = player()

font = pygame.font.SysFont(None, 48)
while True:
    
    if character.score >= max_score:
        print(perf_counter()-start)
        break
        
    pygame.time.Clock().tick(30)
	# completely fill the surface object
	# with white colour
	#display_surface.fill(white)
    

	# copying the image surface object
	# to the display surface object at
    # (0, 0) coordinate.
    
    for y in range(len(level)):
        for x in range(len(level[y])):
            j = level[y][x]
            
            for material in materials:
                if material.value == j:
                    #pass
                    display_surface.blit(material.image, (x*scale, y*scale))
    
    score_text = font.render(f"SCORE:{character.score}", True, (255,0,0))
    display_surface.blit(score_text, (Y/2.5, X//10))
    timer = font.render(f"Time:{round(perf_counter()-start,2)}", True, (255,0,0))
    display_surface.blit(timer, (Y//10, X//10))


    display_surface.blit(character.lower, ((board_size[0] - character.x)*scale, (board_size[1]-character.y)*scale))
    if not character.crouch:
        display_surface.blit(character.upper, ((board_size[0] - character.x)*scale, (board_size[1]-character.y-1)*scale))

    #display_surface.blit(grass, (0, 0))

	# iterate over the list of Event objects
	# that was returned by pygame.event.get() method.
    
    # ------------- gravity -------------- 
    if character.jumping:
        character.jump()

    coin_count = 0
    for x in level:
        for j in x:
            if j == coin.value:
                coin_count += 1

    if coin_count == 0:
        found = False
        while not found:
            new_x = randint(0,board_size[0]-1)
            new_y = randint(0,board_size[1]-1)
            for material in non_solid_materials:
                if material.value == level[new_y][new_x]:
                    found = True
                    level[new_y][new_x] = coin.value
                    found = True
    
    
    for event in pygame.event.get() :  

		# if event object type is QUIT
		# then quitting the pygame
		# and program both.
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:

			# deactivates the pygame library
            pygame.quit()

			# quit the program.
            quit()

        if event.type == pygame.KEYDOWN:
            # -----------------movement---------------------
            if event.key == character.left_key and player.valid_position(character.x,character.y, False, +1, character):
                character.x += 1
            if event.key == character.right_key and player.valid_position(character.x,character.y, False, -1, character):
                character.x -= 1
            if event.key == character.down_key and player.valid_position(character.x,character.y, True, -1, character):
                character.y -= 1
            if event.key == character.up_key and player.valid_position(character.x+1,character.y, True, character.height, character):
                character.y += 1

            if event.key == character.crouch_key:
                
                if player.valid_position(character.x, character.y, True, 2, character) and character.crouch:
                    character.crouch = False
                else:
                    character.crouch = True

            if event.key == pygame.K_SPACE:
                if not character.jumping:
                    character.jumping = True
            
            if event.key == pygame.K_c:
                print(character.x, character.y)

		# Draws the surface object to the screen
        # 
    pygame.display.update()