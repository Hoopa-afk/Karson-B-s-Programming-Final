import pygame
import sys
import time

def main():
    pygame.init()
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tamagotchi Pet")
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()

    # This is the Pet class
    class Pet:
        def __init__(self):
            self.hunger = 50
            self.happiness = 50
            self.cleanliness = 50
            self.alive = True

        def feed(self):
            self.hunger = min(100, self.hunger + 10)

        def play(self):
            self.happiness = min(100, self.happiness + 10)

        def clean(self):
            self.cleanliness = min(100, self.cleanliness + 10)

        def update(self):
            self.hunger -= 0.1
            self.happiness -= 0.05
            self.cleanliness -= 0.07
            if self.hunger <= 0 or self.happiness <= 0 or self.cleanliness <= 0:
                self.alive = False

        def draw(self):
            stats = f"Hunger: {int(self.hunger)}  Happiness: {int(self.happiness)}  Cleanliness: {int(self.cleanliness)}"
            text = font.render(stats, True, BLACK)
            screen.blit(text, (20, 20))
            face = ":)" if self.alive else "X("
            face_text = font.render(f"Pet: {face}", True, BLACK)
            screen.blit(face_text, (20, 60))
            instructions = font.render("F: Feed  P: Play  C: Clean", True, BLACK)
            screen.blit(instructions, (20, 100))



    pet = Pet()
    main()