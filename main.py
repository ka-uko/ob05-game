import pygame
import random
import time

pygame.init()

# Константы
WIDTH, HEIGHT = 400, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
RED = (255, 0, 0)
FPS = 60

# Основной экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ловушка квадратов")

# Класс для игрока
class Player:
    def __init__(self):
        self.original_width = 100
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT - 50, self.original_width, 20)
        self.speed = 5
        self.shrunk = False
        self.shrink_time = 0

    def move(self, dx):
        if self.rect.left + dx >= 0 and self.rect.right + dx <= WIDTH:
            self.rect.x += dx

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)

    def shrink(self):
        if not self.shrunk:
            self.rect.width //= 2
            self.shrunk = True
            self.shrink_time = time.time()

    def update(self):
        # Проверяем, прошло ли 10 секунд после уменьшения
        if self.shrunk and time.time() - self.shrink_time > 10:
            self.rect.width = self.original_width
            self.shrunk = False

# Класс для падающих фигур
class FallingShape:
    def __init__(self, x, y, size, shape_type):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = random.randint(3, 6)
        self.shape_type = shape_type  # 'square', 'diamond', 'triangle'

    def fall(self):
        self.rect.y += self.speed

    def draw(self, surface):
        if self.shape_type == 'square':
            pygame.draw.rect(surface, BLACK, self.rect)
        elif self.shape_type == 'diamond':
            pygame.draw.polygon(surface, BLACK, [self.rect.midtop,
                                                 self.rect.midright,
                                                 self.rect.midbottom,
                                                 self.rect.midleft])
        elif self.shape_type == 'triangle':
            pygame.draw.polygon(surface, RED, [self.rect.midbottom,
                                                 (self.rect.left, self.rect.top),
                                                 (self.rect.right, self.rect.top)])

# Основная функция
def main():
    clock = pygame.time.Clock()
    player = Player()
    shapes = []
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-player.speed)
        if keys[pygame.K_RIGHT]:
            player.move(player.speed)

        # Добавляем новые фигуры
        if random.random() < 0.02:  # Вероятность появления новой фигуры
            x = random.randint(0, WIDTH - 30)
            shape_type = random.choice(['square', 'diamond', 'triangle'])
            shapes.append(FallingShape(x, 0, 30, shape_type))

        # Обновление состояния игры
        for shape in shapes[:]:
            shape.fall()
            if shape.rect.colliderect(player.rect):
                if shape.shape_type == 'square':  # Ловим только квадраты
                    score += 1
                elif shape.shape_type == 'triangle':  # Ловим треугольники
                    player.shrink()
                shapes.remove(shape)
            elif shape.rect.top > HEIGHT:
                shapes.remove(shape)

        # Обновляем игрока
        player.update()

        # Отрисовка
        screen.fill(WHITE)
        player.draw(screen)
        for shape in shapes:
            shape.draw(screen)

        # Отображаем счет
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()