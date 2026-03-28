import random
import pygame
import sys

pygame.init()
pygame.mixer.init()  # Инициализация звука

screen_width = 900
screen_height = 450
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
FPS = 30

# Загрузка изображений
dino_img = pygame.transform.scale(pygame.image.load("The_Lonely_T_Rex.png"), (60, 60))
dead_dino_img = pygame.transform.scale(pygame.image.load("Dead_Chrome_T-Rex.webp.png"), (60, 60))
one_cactus_image = pygame.transform.scale(pygame.image.load("1_Cactus_Chrome_Dino.webp.png"), (60, 60))
three_cactus_image = pygame.transform.scale(pygame.image.load("3_Cactus_Chrome_Dino.webp.png"), (110, 60))
horizon_image = pygame.image.load("Chromium_T-Rex-horizon.png")
cloud_image = pygame.transform.scale(pygame.image.load("Chromium_T-Rex-cloud.png"), (140, 60))
font = pygame.font.Font("PressStart2P-Regular.ttf", 20)

# Загрузка звуков (замените названия, если файлы называются иначе)
try:
    jump_sound = pygame.mixer.Sound("jump.wav")
    die_sound = pygame.mixer.Sound("die.wav")
    pygame.mixer.music.load("music.mp3")
except:
    # Если файлов нет, игра просто будет без звука
    jump_sound = die_sound = None


class Dino:
    def __init__(self):
        self.x = 50
        self.y = 350
        self.width = 60
        self.height = 60
        self.jump_count = 10
        self.is_jumping = False
        self.rect = pygame.Rect(self.x, self.y, self.width - 10, self.height - 10)

    def draw(self, screen1):
        screen1.blit(dino_img, (self.x, self.y))

    def draw_dead(self, screen1):
        screen1.blit(dead_dino_img, (self.x, self.y))

    def jump(self):
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10
        self.rect.topleft = (self.x, self.y)


class Obstacle:
    def __init__(self, speed):
        self.reset(speed)

    def reset(self, speed):
        self.image = random.choice([one_cactus_image, three_cactus_image])
        self.width = self.image.get_width()
        self.x = screen_width + random.randint(100, 300)
        self.y = 355
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.image.get_height())
        self.scored = False

    def move(self):
        self.x -= self.speed
        if self.x <= -self.width:
            self.reset(self.speed)
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen1):
        screen1.blit(self.image, (self.x, self.y))


class Ground:
    def __init__(self, speed):
        self.image = horizon_image
        self.width = self.image.get_width()
        self.x1, self.x2 = 0, self.width
        self.y = 400
        self.speed = speed

    def move(self):
        self.x1 -= self.speed
        self.x2 -= self.speed
        if self.x1 <= -self.width: self.x1 = self.x2 + self.width
        if self.x2 <= -self.width: self.x2 = self.x1 + self.width

    def draw(self, screen1):
        screen1.blit(self.image, (self.x1, self.y))
        screen1.blit(self.image, (self.x2, self.y))


def game_start():
    # Стартовое меню
    screen.fill((255, 255, 255))
    text = font.render("PRESS SPACE TO START", True, (83, 83, 83))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if jump_sound: jump_sound.play()
                waiting = False


def game_over_screen():
    text = font.render("G A M E  O V E R", True, (83, 83, 83))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 50))
    pygame.display.update()
    pygame.time.delay(1000)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


record = 0

while True:
    game_start()

    # Сброс игры
    dino = Dino()
    base_speed = 10  # Начальная скорость
    obstacle = Obstacle(base_speed)
    ground = Ground(base_speed)
    score = 0
    game_active = True

    # Запуск фоновой музыки
    try:
        pygame.mixer.music.play(-1)
    except:
        pass

    while game_active:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not dino.is_jumping:
                    dino.is_jumping = True
                    if jump_sound: jump_sound.play()  # Звук прыжка

        # Увеличение сложности каждые 100 очков
        current_speed = base_speed + (score // 100)
        obstacle.speed = current_speed
        ground.speed = current_speed

        # Логика движений
        dino.jump()
        obstacle.move()
        ground.move()

        # Начисление очков
        if obstacle.x + obstacle.width < dino.x and not obstacle.scored:
            score += 1
            obstacle.scored = True
        if score > record: record = score

        # Коллизия
        if dino.rect.colliderect(obstacle.rect):
            pygame.mixer.music.stop()
            if die_sound: die_sound.play()  # Звук столкновения
            dino.draw_dead(screen)
            game_over_screen()
            game_active = False

        # Отрисовка
        ground.draw(screen)
        obstacle.draw(screen)
        dino.draw(screen)

        score_txt = font.render(f"HI {record:05} {score:05}", True, (83, 83, 83))
        screen.blit(score_txt, (screen_width - 350, 20))

        pygame.display.update()
        clock.tick(FPS)