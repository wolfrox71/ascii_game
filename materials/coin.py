from info import scale
import pygame
class coin:
    value = 4
    colour = "yellow"
    solid = False
    image = pygame.image.load(f"./sprites/coin_{scale}.png")
    collectable = True

    def on_collection(character):
        score_increase = 1
        character.score += score_increase