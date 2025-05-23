from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)

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


class GameObject:
    """Родительский класс для всех классов игровых объектов.
    Описывает их общие атрибуты и методы.
    """

    def __init__(self, position=SCREEN_CENTER, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw_one_sector(self, position=None):
        """Используется для отрисовки одной клетки объекта.
        Для объектов, состоящих более чем из одной клетки,
        вызывать с аргументом position
        """
        rect = pygame.Rect(
            (position if position is not None else self.position),
            (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Заготовка для методов, которые отрисовывают игровые объекты.
        Определяется в каждом классе-наследнике.
        """
        raise NotImplementedError('Метод draw не определён.')


class Apple(GameObject):
    """Класс для создания объека 'яблоко'."""

    def __init__(self, position=SCREEN_CENTER, body_color=APPLE_COLOR):
        super().__init__(position=position, body_color=body_color)

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
        self.draw_one_sector()


class Snake(GameObject):
    """Класс для создания объекта 'змейка'."""

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR):
        super().__init__(position=position, body_color=body_color)
        self.reset()

    def is_opposite_direction(self, direction, current_direction):
        """Проверяет, не является ли новое направление
        противоположным текущему.
        """
        return direction == tuple(-x for x in current_direction)

    def update_direction(self, new_direction):
        """Обновляет направление после нажатия на кнопку"""
        self.direction = new_direction

    def get_head_position(self):
        """Возвращает координаты головы змейки"""
        return self.positions[0]

    def move(self):
        """Управляет движением змейки, изменяя список
        с координатами её сегментов.
        """
        head_x, head_y = self.get_head_position()
        new_x = (
            head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (
            head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        self.positions.insert(0, new_position)

    def draw(self):
        """Отрисовывает змейку по заданным координатам."""
        # Отрисовка головы змейки
        self.draw_one_sector(self.get_head_position())

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Откатывает состояние змейки к начальному."""
        self.length = 1
        self.positions = [(SCREEN_CENTER)]
        self.direction = choice(DIRECTIONS)
        self.last = None


def handle_keys(game_object):
    """Обрабатывает действия пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            actions_directions = {
                pygame.K_UP: UP,
                pygame.K_DOWN: DOWN,
                pygame.K_LEFT: LEFT,
                pygame.K_RIGHT: RIGHT,
            }
            if event.key in actions_directions:
                direction = actions_directions[event.key]
                opposit_direction = game_object.is_opposite_direction(
                    direction, game_object.direction)
                if opposit_direction:
                    continue
                game_object.update_direction(direction)


def main():
    """Создаёт экземпляры классов Apple и Snake, запускает игровой цикл."""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            while apple.position in snake.positions:
                apple.randomize_position()
        if snake.get_head_position() in snake.positions[3:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
