import pygame

class Pipe:
    def __init__(self, x, y, gap, speed):
        # Create the top and bottom pipes
        self.image_top = pygame.image.load("assets/images/pipe-top.png")
        self.image_bottom = pygame.image.load("assets/images/pipe-bottom.png")
        self.rect_top = self.image_top.get_rect(midbottom=(x, y - gap // 2))
        self.rect_bottom = self.image_bottom.get_rect(midtop=(x, y + gap // 2))
        self.speed = speed
        self.passed = False

    def move(self):
        # Move pipes to the left
        self.rect_top.x -= self.speed
        self.rect_bottom.x -= self.speed

    def draw(self, screen):
        # Draw the pipes on the screen
        screen.blit(self.image_top, self.rect_top)
        screen.blit(self.image_bottom, self.rect_bottom)

    def is_off_screen(self):
        # Check if the pipes have moved off the left side of the screen
        return self.rect_top.right < 0

    def collides_with(self, bird):
        # Check for collision with the bird
        return self.rect_top.colliderect(bird) or self.rect_bottom.colliderect(bird)

