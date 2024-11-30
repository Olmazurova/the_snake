from random import choice, randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет отравы
POISON_COLOR = (102, 0, 255)

# Цвет змейки
SNAKE_COLOR = (119, 221, 119)

# Цвет камня
STONE_COLOR = (127, 118, 121)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Абстрактный класс для объектов игры."""

    position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def __init__(self, body_color=None):
        """Инициализирует атрибут цвета объекта."""
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для отрисовки объектов на игровом поле."""
        pass

    def randomize_position(self):
        """Задаёт случайные координаты объекта."""
        self.position = (choice(tuple(range(0, SCREEN_WIDTH, GRID_SIZE))),
                         choice(tuple(range(0, SCREEN_HEIGHT, GRID_SIZE))))


class Apple(GameObject):
    """Описывает яблоко, его артрибуты и методы."""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализирует атрибуты яблока: позицию и цвет."""
        self.randomize_position()
        self.body_color = body_color

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Poison(GameObject):
    """Описывает отраву, её атрибуты и методы."""

    def __init__(self, body_color=POISON_COLOR):
        """Инициализирует атрибуты отравы: позицию и цвет."""
        self.randomize_position()
        self.body_color = body_color

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описывает змейку, её атрибуты и методы."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует атрибуты змейки.

        length - длина
        positions - список координат каждой ячейки змейки
        direction - текущее направление движения змейки
        next_direction - следующее направление движения змейки
        body_color - цвет змейки
        """
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = body_color

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head = (self.positions[0][0] + self.direction[0] * GRID_SIZE,
                self.positions[0][1] + self.direction[1] * GRID_SIZE)

        self.positions.insert(0, self._normalize_position(head))

        if self.length < len(self.positions):
            for _ in range(len(self.positions) - self.length):
                self.last = self.positions.pop()
                self.draw_background()
        else:
            self.last = self.positions[-1]

    @staticmethod
    def _normalize_position(position):
        """Нормализует координаты относительно размера игрового поля."""
        position_x = position[0] % SCREEN_WIDTH
        position_y = position[1] % SCREEN_HEIGHT
        return (position_x, position_y)

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
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
            self.draw_background()

    def draw_background(self, coordinates=None):
        """Затирает переданные координаты цветом игрового поля."""
        if coordinates is None:
            coordinates = self.last
        last_rect = pygame.Rect(coordinates, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        for coordinate in [*self.positions, self.last]:
            self.draw_background(coordinate)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = self.body_color
        self.last = None


class Stone(GameObject):
    """Описывает препятствие - камень, его атрибуты и методы."""

    def __init__(self, body_color=STONE_COLOR):
        """Инициализирует атрибуты камня: позицию и цвет."""
        self.randomize_position()
        self.body_color = body_color

    def draw(self):
        """Отрисовывает камень на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Изменяет направление движения змейки от нажатой клавиши."""
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
    """Основной процесс игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    poison = Poison()
    stones = [Stone() for _ in range(1, randint(2, 4))]

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка: съедено ли яблоко и увеличение длины змейки
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Проверка: съедена ли отрава и уменьшение длины змейки
        if snake.get_head_position() == poison.position:
            snake.length -= 1
            if snake.length == 0:
                snake.reset()
            poison.randomize_position()

        # Проверка: врезалась ли змейка сама в себя
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Проверка: врезалась ли змейка в камень
        if snake.get_head_position() in [stone.position for stone in stones]:
            snake.reset()

        # Отрисовка объектов
        snake.draw()
        apple.draw()
        poison.draw()
        for stone in stones:
            stone.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
