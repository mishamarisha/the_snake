from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREENS_CENTER = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, RIGHT, LEFT]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """Родительский класс для всех классов игровых объектов.
    Описывает их общие атрибуты и методы.
    """

    def __init__(self):
        self.position = SCREENS_CENTER
        self.body_color = None

    def draw(self):
        """Заготовка для методов, которые отрисовывают игровые объекты.
        Определяется в каждом классе-наследнике.
        """
        pass


class Apple(GameObject):
    """Класс для создания объека 'яблоко'."""

    def __init__(self):
        super().__init__()
        self.position = SCREENS_CENTER
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Метод изменяет позицию яблока, присваивая случайные координаты
        в пределах игрового поля.
        """
        self.position = (
            (randint(0, GRID_WIDTH - 1) * GRID_SIZE),
            (randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        )

    def draw(self):
        """Отрисовывает яблоко по заданным координатам."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для создания объекта 'змейка'."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [(SCREENS_CENTER)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Обновляет направление после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает координаты головы змейки"""
        return self.positions[0]

    def move(self):
        """Управляет движением змейки, изменяя список
        с координатами её сегментов.
        """
        position_now = self.get_head_position()
        new_x = (
            position_now[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (
            position_now[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        self.positions.insert(0, new_position)

    # Метод draw класса Snake
    def draw(self):
        """Отрисовывает змейку по заданным координатам."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Откатывает состояние змейки к начальному."""
        self.length = 1
        self.positions = [(SCREENS_CENTER)]
        self.direction = choice(DIRECTIONS)


def handle_keys(game_object):
    """Обрабатывает действия пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Создаёт экземпляры классов Apple и Snake, запускает игровой цикл."""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
