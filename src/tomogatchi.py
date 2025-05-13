import pygame
import sys

def main():
    pygame.init()
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tamagotchi Friend")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 112, 255)
    font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()

    class Pet:
        def __init__(self):
            self.hunger = 50
            self.happiness = 50
            self.cleanliness = 50
            self.alive = True

            # Load and scale all sprites
            self.idle_image = pygame.transform.scale(pygame.image.load("pet_idle.png"), (100, 100))
            self.feed_image = pygame.transform.scale(pygame.image.load("pet_feed.png"), (100, 100))
            self.play_image = pygame.transform.scale(pygame.image.load("pet_play.png"), (100, 100))
            self.clean_image = pygame.transform.scale(pygame.image.load("pet_clean.png"), (100, 100))
            self.dead_image = pygame.transform.scale(pygame.image.load("pet_dead.png"), (100, 100))

            self.state = "idle"
            self.state_timer = 0  # Used to return to idle state after action

        def feed(self):
            self.hunger = min(100, self.hunger + 10)
            self.state = "feed"
            self.state_timer = 30  # Show feed image for 1 second

        def play(self):
            self.happiness = min(100, self.happiness + 10)
            self.state = "play"
            self.state_timer = 30

        def clean(self):
            self.cleanliness = min(100, self.cleanliness + 10)
            self.state = "clean"
            self.state_timer = 30

        def update(self):
            self.hunger = max(0, self.hunger - 0.04)
            self.happiness = max(0, self.happiness - 0.05)
            self.cleanliness = max(0, self.cleanliness - 0.07)

            if self.state_timer > 0:
                self.state_timer -= 1
            else:
                self.state = "idle"

            if self.hunger <= 0 or self.happiness <= 0 or self.cleanliness <= 0:
                self.alive = False

        def draw(self):
            stats = f"Hunger: {int(self.hunger)}  Happiness: {int(self.happiness)}  Cleanliness: {int(self.cleanliness)}"
            text = font.render(stats, True, BLUE)
            screen.blit(text, (20, 20))
            face = ":)" if self.alive else "X("
            face_text = font.render(f"Pet: {face}", True, BLUE)
            screen.blit(face_text, (20, 60))
            instructions = font.render("F: Feed  P: Play  C: Clean", True, WHITE)
            screen.blit(instructions, (20, 100))

            if self.alive:
                if self.state == "feed":
                    screen.blit(self.feed_image, (250, 200))
                elif self.state == "play":
                    screen.blit(self.play_image, (250, 200))
                elif self.state == "clean":
                    screen.blit(self.clean_image, (250, 200))
                else:
                    screen.blit(self.idle_image, (250, 200))
            else:
                screen.blit(self.dead_image, (250, 200))

    pet = Pet()

    background_img = pygame.image.load("hamster.jpg")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

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

            if not pet.alive and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pet = Pet()

        if pet.alive:
            pet.update()

        pet.draw()

        if not pet.alive:
            restart_text = font.render(
                "Pet has died! Press R to restart.", True, WHITE
            )
            screen.blit(restart_text, (20, 140))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
