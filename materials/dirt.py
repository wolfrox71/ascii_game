from info import scale
import pygame
class dirt:
    value = 3
    colour = "green"
    solid = True
    image = pygame.image.load(f"./sprites/dirt_{scale}.png")
    score_increase = 0
    collectable = False