import pygame

class Bird:
    def __init__(self, x, y):
        # Preload textures and set initial variables
        self.textures = [
            pygame.image.load("assets/images/yellowbird-downflap.png"),
            pygame.image.load("assets/images/yellowbird-midflap.png"),
            pygame.image.load("assets/images/yellowbird-upflap.png")
        ]
        self.texture_index = 0
        self.image = self.textures[int(self.texture_index)]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.wing_sfx = pygame.mixer.Sound("assets/sfx/sfx_wing.wav")
        
        # Flight mechanics
        self.gravity = 0.5             # Gravity effect on the bird
        self.velocity = 0              # Current velocity (momentum)
        self.jump_strength = -10       # Upward force applied when jumping
        self.cooldown = 0              # Cooldown timer for jump control
        self.cooldown_time = 15        # Cooldown duration in frames (about 0.25 seconds at 60 FPS)
        self.last_texture_index = -1

    def fly(self, keys):
        # Handle jump with cooldown
        if keys[pygame.K_SPACE] and self.cooldown <= 0:
            self.tap()

        # Apply gravity to velocity
        self.velocity += self.gravity
        self.rect.y += int(self.velocity)  # Move bird by velocity

        # Update cooldown if it's active
        if self.cooldown > 0:
            self.cooldown -= 1
    
    def tap(self):
        # Ensure not to go out of the screen
        if self.rect.top > self.image.get_height()*10:
            self.velocity = self.jump_strength  # Apply upward force
            self.cooldown = self.cooldown_time  # Reset cooldown timer
            #pygame.mixer.Sound.play(self.wing_sfx)

    def animate(self):
        current_texture_index = int(self.texture_index)
        
        # Update texture only if index has changed
        if current_texture_index != self.last_texture_index:
            self.image = self.textures[current_texture_index]
            self.last_texture_index = current_texture_index
            
        # Increment texture_index and reset if it exceeds the available textures
        self.texture_index += 0.1
        if self.texture_index >= len(self.textures):
            self.texture_index = 0
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
