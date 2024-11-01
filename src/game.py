import pygame
from random import randint
from pipe import Pipe
from bird import Bird
from time import sleep
import numpy as np
from PIL import Image
class Game:
    def __init__(self, screen_width=400, screen_height=600):
        pygame.init()
        pygame.mixer.init()
        self.screen_width,self.screen_height = screen_width, screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Flappy Bird RL")

        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0

        self.load_assets()
        self.reset_game()

    def load_assets(self):
        """Load game assets."""
        self.hit_sfx = pygame.mixer.Sound("assets/sfx/sfx_hit.wav")
        self.background_texture = pygame.image.load("assets/images/background-day.png")
        self.background_texture = pygame.transform.scale(self.background_texture,(self.background_texture.get_width()+self.screen_height-self.background_texture.get_height(), self.screen_height))
        original_floor_texture = pygame.image.load("assets/images/base.png")
        self.floor_texture = pygame.transform.scale(original_floor_texture, (self.screen.get_width(), original_floor_texture.get_height()))
        
    def reset_game(self):
        """Reset the game to initial state."""
        self.bird = Bird(x=self.screen_width//2 - 50, y=randint(self.screen.get_height() // 2,self.screen.get_height() // 2 + self.screen.get_height() // 4))
        self.pipes = []
        self.bird_status = "alive"
        self.floor_y = self.screen.get_height() - self.floor_texture.get_height() // 2
        self.floor_x1 = 0
        self.floor_x2 = self.floor_texture.get_width()
        self.pipe_gap = 200
        self.pipe_spawn_time = 700
        self.last_pipe_spawn = pygame.time.get_ticks()
        self.pipe_speed = 5
        self.floor_speed = 5
        self.score = 0

    def spawn_pipes(self):
        """Spawn new pipes at intervals."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe_spawn >= self.pipe_spawn_time:
            y_position = randint(200, 400)
            pipe = Pipe(x=self.screen.get_width() + 10, y=y_position, gap=self.pipe_gap, speed=self.pipe_speed)
            self.pipes.append(pipe)
            self.last_pipe_spawn = current_time

    def handle_events(self):
        """Handle game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if self.bird_status == "dead" and event.key == pygame.K_SPACE:
                    self.reset_game()

    def update(self, action):
        """Update game state based on action."""
        if self.bird_status == "alive":
            keys = pygame.key.get_pressed()
            self.bird.fly(keys)
            if action == 0:  # action = 0 means the bird taps (flies)
                self.bird.tap()

            self.bird.animate()
            self.spawn_pipes()

            # Check if bird hit the ground
            if self.bird.rect.y >= self.floor_y:
                #pygame.mixer.Sound.play(self.hit_sfx)
                self.bird_status = "dead"

            for pipe in self.pipes:
                pipe.move()
                if pipe.collides_with(self.bird.rect):
                    #pygame.mixer.Sound.play(self.hit_sfx)
                    self.bird_status = "dead"

                # Check if bird passed the pipe for scoring
                if pipe.rect_top.x + pipe.rect_top.width < self.bird.rect.x and not pipe.passed:
                    self.score += 1
                    pipe.passed = True  # Mark the pipe as passed
            for i in range(len(self.pipes)-1):
                if self.pipes[i].rect_top.colliderect(self.pipes[i+1].rect_top):
                    self.pipes.pop(i)

            # Move the floor
            self.floor_x1 -= self.floor_speed
            self.floor_x2 -= self.floor_speed

            # Reset floor positions
            if self.floor_x1 <= -self.floor_texture.get_width():
                self.floor_x1 = self.floor_x2 + self.floor_texture.get_width()
            if self.floor_x2 <= -self.floor_texture.get_width():
                self.floor_x2 = self.floor_x1 + self.floor_texture.get_width()

            # Remove pipes that have moved off-screen
            self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]

        return self.state(), self.reward(), self.is_done()

    def render(self):
        """Draw all game elements."""
        self.screen.fill((135, 206, 235))  # Sky color
        # Draw background texture 3 times to cover the entire window
        for i in range(3):
            self.screen.blit(self.background_texture, (self.background_texture.get_width()*i,0))
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # Draw the floor
        self.screen.blit(self.floor_texture, (self.floor_x1, self.floor_y))
        self.screen.blit(self.floor_texture, (self.floor_x2, self.floor_y))

        # Draw the score
        self.draw_score()

        pygame.display.flip()

    def draw_score(self):
        """Render and display the score on the screen."""
        font = pygame.font.Font("assets/04B_19.TTF", 30)
        score_surface = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_surface, (10, 10))

    def reward(self):
        """Calculate reward."""
        if self.bird_status == "dead":
            return -1000  # Negative reward for game over
        elif self.pipes and self.pipes[0].passed:
            return 1  # Positive reward for passing a pipe
        return 0

    def is_done(self):
        """Check if the game is over."""
        return self.bird_status == "dead"

    def state(self):
        """Return current state for Q-learning."""
        if self.pipes:
            pipe = self.pipes[0]
            dist_x = abs(pipe.rect_top.x - self.bird.rect.x)
            dist_y = abs(pipe.rect_top.x - self.bird.rect.y)
            return (self.bird.rect.y, dist_x, dist_y, 0 if self.bird_status == "alive" else 1)
        return (self.bird.rect.y, 0, 0, 1)

    def run_step(self, action):
        """Run a single step of the game and return the state, reward, done status, and captured image."""
        state, reward, done = self.update(action)
        return state, reward, done

    def mainloop(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update(1)
            self.render()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.mainloop()