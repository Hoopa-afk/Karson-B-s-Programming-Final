import pygame
import sys
import time

def main():
    pygame.init()
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tamagotchi Friend")

    background_img = pygame.image.load("hamster.jpg")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
                                            
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
            text = font.render(stats, True, WHITE)
            screen.blit(text, (20, 20))
            face = ":)" if self.alive else "X("
            face_text = font.render(f"Pet: {face}", True, WHITE)
            screen.blit(face_text, (20, 60))
            instructions = font.render("F: Feed  P: Play  C: Clean", True, WHITE)
            screen.blit(instructions, (20, 100))



    # This the  pet instance
    pet = Pet()

    # Game loop
    while True:
        screen.blit(background_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pet.alive and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pet.feed()
                elif event.key == pygame.K_p:
                    pet.play()
                elif event.key == pygame.K_c:
                    pet.clean()

        if pet.alive:
            pet.update()

        pet.draw()
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()