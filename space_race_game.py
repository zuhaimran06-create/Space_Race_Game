import pygame
import random

pygame.init()

# Screen dimensions
sw = 800
sh = 800
self_y = 650
ogY = self_y
speed = 3

# Window
win = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Space Race Game")

# Timer and fonts
clock = pygame.time.Clock()
font_large = pygame.font.SysFont("arial", 80)
font_medium = pygame.font.SysFont("arial", 50)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (160, 80, 255)
PINK = (255, 120, 180)
BLUE = (80, 160, 255)


class Thing:
    def isCollision(self, thing):
        if self.x < thing.x + thing.w and self.x + self.w > thing.x:
            if self.y < thing.y + thing.h and self.y + self.h > thing.y:
                return True
        return False


class Player(Thing):
    def __init__(self, x, color):
        self.x = x
        self.y = self_y
        self.w = 60
        self.h = 60
        self.yv = 0
        self.color = color
        self.score = 0

    def draw(self, win):
        pygame.draw.ellipse(win, self.color, (self.x, self.y, self.w, self.h))
        pygame.draw.ellipse(win, WHITE, (self.x + 15, self.y + 15, 10, 10))
        pygame.draw.ellipse(win, WHITE, (self.x + 35, self.y + 15, 10, 10))

    def update_speed(self):
        self.y += self.yv

        # Keep player inside the screen
        if self.y < 0:
            self.y = 0
        if self.y > ogY:
            self.y = ogY

    def checkIncreaseScore(self):
        if self.y <= 100:
            self.score += 1
            self.y = ogY


class Rock(Thing):
    def __init__(self):
        self.w = 28
        self.h = 28
        self.y = random.randint(108, sh - 200 - self.h)

        if random.choice([0, 1]) == 0:
            self.x = -50 - self.w
            self.xv = 2
        else:
            self.x = sw + 50
            self.xv = -2

    def draw(self, win):
        pygame.draw.rect(win, YELLOW, (self.x, self.y, self.w, self.h))
        pygame.draw.circle(win, RED, (self.x + self.w // 2, self.y + self.h // 2), 8)

    def move(self):
        self.x += self.xv


def draw_background():
    win.fill(BLACK)

    # Simple stars instead of galaxy image
    for i in range(40):
        x = (i * 53) % sw
        y = (i * 97) % sh
        pygame.draw.circle(win, WHITE, (x, y), 2)

    # Finish line
    pygame.draw.line(win, WHITE, (0, 100), (sw, 100), 3)


def redrawGameWindow():
    draw_background()

    p1.draw(win)
    p2.draw(win)

    for r in rocks:
        r.draw(win)

    p1ScoreText = font_medium.render(str(p1.score), 1, WHITE)
    p2ScoreText = font_medium.render(str(p2.score), 1, WHITE)

    win.blit(p1ScoreText, (200 - p1ScoreText.get_width() / 2, 740))
    win.blit(p2ScoreText, (600 - p2ScoreText.get_width() / 2, 740))

    pygame.display.update()


# Home screen
def home_screen():
    waiting = True

    while waiting:
        win.fill(BLACK)

        title = font_large.render("SPACE RACE GAME", 1, YELLOW)
        win.blit(title, (sw // 2 - title.get_width() // 2, 200))

        start_button = pygame.Rect(sw // 2 - 100, 400, 200, 80)
        pygame.draw.rect(win, GREEN, start_button)

        start_text = font_medium.render("START", 1, BLACK)
        win.blit(start_text, (sw // 2 - start_text.get_width() // 2, 420))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    waiting = False


# Play again screen
def play_again_screen():
    waiting = True

    while waiting:
        win.fill(BLACK)

        text = font_large.render("GAME OVER", 1, RED)
        win.blit(text, (sw // 2 - text.get_width() // 2, 200))

        button = pygame.Rect(sw // 2 - 150, 400, 300, 80)
        pygame.draw.rect(win, GREEN, button)

        btn_text = font_medium.render("PLAY AGAIN", 1, BLACK)
        win.blit(btn_text, (sw // 2 - btn_text.get_width() // 2, 420))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    waiting = False


# Main game function
def main_game():
    global p1, p2, rocks

    p1 = Player(175, PINK)
    p2 = Player(575, BLUE)

    rocks = []
    count = 0
    run = True

    while run:
        clock.tick(100)

        p1.update_speed()
        p2.update_speed()

        p1.checkIncreaseScore()
        p2.checkIncreaseScore()

        # Check winner
        if p1.score >= 3 or p2.score >= 3:
            winner = p1 if p1.score >= 3 else p2
            win_text = "Player 1 Wins!" if p1.score >= 3 else "Player 2 Wins!"

            win.fill(BLACK)
            text = font_large.render(win_text, 1, YELLOW)
            win.blit(text, (sw // 2 - text.get_width() // 2, sh // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)

            # Animate winner reaching finish line
            finish_y = 50

            while winner.y > finish_y:
                winner.y -= 5

                draw_background()
                p1.draw(win)
                p2.draw(win)

                for r in rocks:
                    r.draw(win)

                win.blit(text, (sw // 2 - text.get_width() // 2, 10))
                pygame.display.update()
                pygame.time.delay(50)

            pygame.time.delay(1000)
            run = False

            play_again_screen()
            main_game()

        count += 1

        if count % 60 == 0:
            rocks.append(Rock())
            rocks.append(Rock())

        # Move rocks safely
        for r in rocks[:]:
            r.move()

            if r.xv > 0 and r.x > sw:
                rocks.remove(r)

            if r.xv < 0 and r.x < -r.w:
                rocks.remove(r)

            if p1.isCollision(r):
                rocks.remove(r)
                p1.y = ogY

            if p2.isCollision(r):
                rocks.remove(r)
                p2.y = ogY

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    p2.yv = speed
                if event.key == pygame.K_UP:
                    p2.yv = -speed
                if event.key == pygame.K_s:
                    p1.yv = speed
                if event.key == pygame.K_w:
                    p1.yv = -speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    p2.yv = 0
                if event.key == pygame.K_UP:
                    p2.yv = 0
                if event.key == pygame.K_s:
                    p1.yv = 0
                if event.key == pygame.K_w:
                    p1.yv = 0

        redrawGameWindow()


# Start game
home_screen()
main_game()
