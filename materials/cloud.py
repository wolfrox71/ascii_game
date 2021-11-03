from info import scale
import pygame
class cloud:
    value = 1
    colour = "white"
    solid = False
    image = pygame.image.load(f"./sprites/cloud_{scale}.png")
    score_increase = 0
    collectable = False