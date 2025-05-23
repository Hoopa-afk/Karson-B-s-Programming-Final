import pygame
import sys

def main():
    pygame.init()
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tamagotchi Friend")

    WHITE = (255, 255, 255)
    BLUE = (0, 112, 255)
    font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()

    class Pet:
        def __init__(self):
            self.hunger = 50
            self.happiness = 50
            self.cleanliness = 50
            self.alive = True
            self.age = 0  # Tracks growth
            self.stage = "baby"
            self.poop_timer = 0
            self.has_poop = False
            self.poop_image = pygame.transform.scale(pygame.image.load("poop.png"), (40, 40))


            # Load all image set
            self.sprites = {
            "baby": {
                "idle": pygame.transform.scale(pygame.image.load("pet_idle.png"), (100, 100)),
                "feed": [pygame.transform.scale(pygame.image.load("pet_feed.png"), (100, 100)),
                         pygame.transform.scale(pygame.image.load("pet_feed2.png"), (100, 100))],
                "play": [pygame.transform.scale(pygame.image.load("pet_play.png"), (100, 100)),
                         pygame.transform.scale(pygame.image.load("pet_play2.png"), (100, 100))],
                "clean": [pygame.transform.scale(pygame.image.load("pet_clean.png"), (100, 100)),
                          pygame.transform.scale(pygame.image.load("pet_clean2.png"), (100, 100))]
            },
            "adult": {
                "idle": pygame.transform.scale(pygame.image.load("adult_idle.png"), (100, 100)),
                "feed": [pygame.transform.scale(pygame.image.load("adult_feed.png"), (100, 100)),
                         pygame.transform.scale(pygame.image.load("adult_feed2.png"), (100, 100))],
                "play": [pygame.transform.scale(pygame.image.load("adult_play.png"), (100, 100)),
                         pygame.transform.scale(pygame.image.load("adult_play2.png"), (100, 100))],
                "clean": [pygame.transform.scale(pygame.image.load("adult_clean.png"), (100, 100)),
                          pygame.transform.scale(pygame.image.load("adult_clean2.png"), (100, 100))]}}
            
            self.dead_image = pygame.transform.scale(pygame.image.load("pet_dead.png"), (100, 100))
            

            self.mood_images = {"happy": pygame.transform.scale(pygame.image.load("happy.png"), (50, 50)),
            "okay": pygame.transform.scale(pygame.image.load("okay.png"), (50, 50)),
            "sad": pygame.transform.scale(pygame.image.load("sad.png"), (50, 50)),
            "miserable": pygame.transform.scale(pygame.image.load("miserable.png"), (50, 50)),}


            self.state = "idle"
            self.state_timer = 0

            self.feed_frame = 0
            self.feed_frame_timer = 0

            self.play_frame = 0
            self.play_frame_timer = 0

            self.clean_frame = 0
            self.clean_frame_timer = 0

        def get_mood(self):
            avg = (self.hunger + self.happiness + self.cleanliness) / 3
            if avg > 80:
                return "happy"
            elif avg > 50:
                return "okay"
            elif avg > 20:
                return "sad"
            else:
                return "miserable"


        def feed(self):
            self.hunger = min(100, self.hunger + 10)
            self.state = "feed"
            self.state_timer = 30
            self.feed_frame_timer = 0

        def play(self):
            self.happiness = min(100, self.happiness + 10)
            self.state = "play"
            self.state_timer = 30
            self.play_frame_timer = 0

        def clean(self):
            self.cleanliness = min(100, self.cleanliness + 10)
            self.state = "clean"
            self.state_timer = 30
            self.clean_frame_timer = 0

        def update(self):

            mood = self.get_mood()
            if mood in ["happy", "okay"]:
                self.age += 1
                if self.age == 900:
                    self.stage = "adult"

                    
            # Decrease stats
            self.hunger = max(0, self.hunger - 0.04)
            self.happiness = max(0, self.happiness - 0.05)
            self.cleanliness = max(0, self.cleanliness - 0.07)

            if self.state_timer > 0:
                self.state_timer -= 1

                if self.state == "feed":
                    self.feed_frame_timer += 1
                    if self.feed_frame_timer >= 10:
                        self.feed_frame = 1 - self.feed_frame
                        self.feed_frame_timer = 0

                elif self.state == "play":
                    self.play_frame_timer += 1
                    if self.play_frame_timer >= 10:
                        self.play_frame = 1 - self.play_frame
                        self.play_frame_timer = 0

                elif self.state == "clean":
                    self.clean_frame_timer += 1
                    if self.clean_frame_timer >= 10:
                        self.clean_frame = 1 - self.clean_frame
                        self.clean_frame_timer = 0
            else:
                self.state = "idle"

            # Check if pet dies
            if self.hunger <= 0 or self.happiness <= 0 or self.cleanliness <= 0:
                self.alive = False


            self.poop_timer += 1
            if self.poop_timer >= 1200 and not self.has_poop:  # ~20 seconds
                self.has_poop = True
                self.poop_timer = 0

            if self.has_poop:
                self.cleanliness = max(0, self.cleanliness - 0.1)


        def get_mood(self):
            avg = (self.hunger + self.happiness + self.cleanliness) / 3
            if avg > 80:
                return "happy"
            elif avg > 50:
                return "okay"
            elif avg > 20:
                return "sad"
            else:
                return "miserable"
            

        def draw(self):
            overlay = pygame.Surface((WIDTH, 150))
            overlay.set_alpha(100)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            stats = f"Hunger: {int(self.hunger)}  Happiness: {int(self.happiness)}  Cleanliness: {int(self.cleanliness)}"
            text = font.render(stats, True, WHITE)
            screen.blit(text, (20, 20))

            face = ":)" if self.alive else "X("
            face_text = font.render(f"Pet: {face}", True, WHITE)
            screen.blit(face_text, (20, 60))

            instructions = font.render("F: Feed  P: Play  C: Clean  K: Pick up Poo", True, WHITE)
            screen.blit(instructions, (20, 100))

            mood_text = font.render(f"Mood: {self.get_mood()}", True, WHITE)
            mood = self.get_mood()
            screen.blit(mood_text, (20, 130))
            screen.blit(self.mood_images[mood], (120, 125))

            pygame.draw.rect(screen, WHITE, (20, 170, 200, 10))
            progress = min(1.0, self.age / 900)  # this caps at 100 %
            pygame.draw.rect(screen, BLUE, (20, 170, int(200 * progress), 10))


            # Choose the right animation frame
            if self.alive:
                sprites = self.sprites[self.stage]
                if self.state == "feed":
                    screen.blit(sprites["feed"][self.feed_frame], (250, 200))
                elif self.state == "play":
                    screen.blit(sprites["play"][self.play_frame], (250, 200))
                elif self.state == "clean":
                    screen.blit(sprites["clean"][self.clean_frame], (250, 200))
                else:
                    screen.blit(sprites["idle"], (250, 200))
            else:
                screen.blit(self.dead_image, (260, 200))

            if self.has_poop:
                screen.blit(self.poop_image, (260, 300))  

                

    # Load background
    background_img = pygame.image.load("hamster.jpg")
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

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

            if not pet.alive and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pet = Pet()

            if pet.alive and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    if pet.has_poop:
                        pet.has_poop = False

        pet.update()
        pet.draw()
        

        if not pet.alive:
            restart_text = font.render("Pet has died! Press R to restart.", True, WHITE)
            screen.blit(restart_text, (20, 160))

        pygame.display.flip()
        clock.tick(30)



if __name__ == "__main__":
    main()
