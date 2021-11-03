from info import scale
import pygame
class grass:
    value = 2
    colour = "green"
    solid = True
    image = pygame.image.load(f"./sprites/grass_{scale}.png")
    score_increase = 0
    collectable = False