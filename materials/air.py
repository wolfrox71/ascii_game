from info import scale
import pygame
class air:
    value = 0
    colour = "blue"
    solid = False
    image = pygame.image.load(f"./sprites/air_{scale}.png")
    score_increase = 0
    collectable = False