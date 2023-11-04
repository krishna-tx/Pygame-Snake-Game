import pygame
import time
import random

pygame.init()
clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
        
class Food:
    def __init__(self, size=20, screen_width=500, screen_height=500):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size
        self.x, self.y = None, None

    def relocate(self, snake):
        # get random x and y that are multiples of self.size (to align coordinates with snake)
        self.x = random.randint(1, (self.screen_width - 2 * self.size) // self.size) * self.size
        self.y = random.randint(1, (self.screen_height - 2 * self.size) // self.size) * self.size
        if self() in snake:
            self.relocate(snake)

    def __call__(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class Game:
    def __init__(self, size=20, width=500, height=500):
        pygame.display.set_caption("Snake Game")
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.size = size
        self.score = 0
        with open("highscore.txt", 'r') as fin:
            self.high_score = int(fin.read())

        self.font = pygame.font.SysFont("timesnewroman", self.size)

        self.head_x = (width / 2) // self.size * self.size
        self.head_y = (height // 2) // self.size * self.size
        self.dir = "right"

        self.snake = [
            pygame.Rect(self.head_x, self.head_y, self.size, self.size),
            pygame.Rect(self.head_x - self.size, self.head_y, self.size, self.size),
            pygame.Rect(self.head_x - 2 * self.size, self.head_y, self.size, self.size),
            pygame.Rect(self.head_x - 3 * self.size, self.head_y, self.size, self.size)
        ]
        
        self.food = Food(self.size, width, height)
        self.food.relocate(self.snake)
        

    def play(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            
            key_pressed = pygame.key.get_pressed()
            if (key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]) and self.dir != "left":
                self.dir = "right"
            elif (key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]) and self.dir != "right":
                self.dir = "left"
            elif (key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]) and self.dir != "down":
                self.dir = "up"
            elif (key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]) and self.dir != "up":
                self.dir = "down"
            
            

            # move snake
            self.move_snake()
            # print(self.head_x, self.head_y)

            self.snake.insert(0, pygame.Rect(self.head_x, self.head_y, self.size, self.size))

            head = self.snake[0]

            # check if collision (to end the game)
            if self.food().colliderect(head):
                self.food.relocate(self.snake)
                self.score+=1
                self.high_score = max(self.high_score, self.score)
            else:
                self.snake.pop()

            if head.collidelist(self.snake[1:]) >= 0:
                self.show_collision()
                running = False

            self.update_screen()

            if self.head_y <= 0 or self.head_y >= self.height - self.size or self.head_x <= 0 or self.head_x >= self.width - self.size:
                self.show_collision()
                running = False

            clock.tick(20)

    def move_snake(self):
        if self.dir == "right":
            self.head_x += self.size
        elif self.dir == "left":
            self.head_x -= self.size
        elif self.dir == "up":
            self.head_y -= self.size
        elif self.dir == "down":
            self.head_y += self.size

    def update_screen(self):
        self.screen.fill(black)
        # offset = self.snake_body_size // 5
        for body_part in self.snake:
            pygame.draw.rect(self.screen, red, body_part)
            # pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(body_part.x + offset, body_part.y + offset,
            #     self.snake_size - 2 * offset, self.snake_size - 2 * offset))
        
        pygame.draw.rect(self.screen, green, self.food())

        score_text = self.font.render(f"Score: {self.score}", True, white)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, white)
        self.screen.blit(score_text, [100, 0])
        self.screen.blit(high_score_text, [self.width - 250, 0])
        pygame.display.update()

    def show_collision(self):
        sleep_duration = 0.25
        time.sleep(sleep_duration)
        for i in range(3):
            pygame.draw.rect(self.screen, black, self.snake[0])
            pygame.display.update()
            time.sleep(sleep_duration)

            pygame.draw.rect(self.screen, red, self.snake[0])
            pygame.display.update()
            time.sleep(sleep_duration)

    def __call__(self):
        return self.score, self.high_score
    


game = Game(size=25, width=1000, height=800)
game.play()
score, high_score = game()
print(f"Score: {score}")
with open("highscore.txt", 'w') as fout:
    fout.write(str(high_score))

pygame.quit()
