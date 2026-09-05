"""Jogo Snake desenvolvido com Pygame."""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass

import pygame


CELL_SIZE = 24
GRID_WIDTH = 30
GRID_HEIGHT = 22
HUD_HEIGHT = 64
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + HUD_HEIGHT
FPS = 60
MOVE_INTERVAL = 110

BACKGROUND = (13, 23, 32)
GRID_COLOR = (20, 35, 46)
HUD_COLOR = (9, 17, 25)
TEXT_COLOR = (232, 244, 237)
SNAKE_HEAD = (88, 214, 141)
SNAKE_BODY = (42, 166, 108)
FOOD_COLOR = (245, 93, 93)
OVERLAY_COLOR = (5, 10, 15, 205)
BUTTON_COLOR = (42, 166, 108)
BUTTON_HOVER_COLOR = (62, 190, 126)


@dataclass(frozen=True)
class Direction:
    x: int
    y: int


UP = Direction(0, -1)
DOWN = Direction(0, 1)
LEFT = Direction(-1, 0)
RIGHT = Direction(1, 0)


class SnakeGame:
    """Controla o estado, as regras e a renderizacao do jogo."""

    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 30)
        self.title_font = pygame.font.Font(None, 56)
        self.reset()

    def reset(self) -> None:
        center = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.snake = [center, (center[0] - 1, center[1]), (center[0] - 2, center[1])]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.food = self._new_food_position()
        self.score = 0
        self.game_over = False
        self.last_move = pygame.time.get_ticks()

    def _new_food_position(self) -> tuple[int, int]:
        available = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in getattr(self, "snake", [])
        ]
        return random.choice(available)

    def change_direction(self, direction: Direction) -> None:
        if direction.x + self.direction.x == 0 and direction.y + self.direction.y == 0:
            return
        self.next_direction = direction

    def update(self) -> None:
        if self.game_over:
            return

        now = pygame.time.get_ticks()
        if now - self.last_move < MOVE_INTERVAL:
            return
        self.last_move = now
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction.x, head_y + self.direction.y)

        will_eat = new_head == self.food
        body_to_check = self.snake if will_eat else self.snake[:-1]
        hit_wall = not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT)
        hit_body = new_head in body_to_check
        if hit_wall or hit_body:
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        if will_eat:
            self.score += 1
            self.food = self._new_food_position()
        else:
            self.snake.pop()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND)
        self._draw_grid(screen)

        food_rect = self._cell_rect(self.food).inflate(-5, -5)
        pygame.draw.rect(screen, FOOD_COLOR, food_rect, border_radius=7)

        for index, segment in enumerate(self.snake):
            color = SNAKE_HEAD if index == 0 else SNAKE_BODY
            pygame.draw.rect(screen, color, self._cell_rect(segment).inflate(-2, -2), border_radius=6)

        pygame.draw.rect(screen, HUD_COLOR, (0, 0, SCREEN_WIDTH, HUD_HEIGHT))
        score = self.font.render(f"Pontos: {self.score}", True, TEXT_COLOR)
        controls = self.font.render("Setas/WASD para mover", True, (160, 181, 191))
        screen.blit(score, (18, 18))
        screen.blit(controls, (SCREEN_WIDTH - controls.get_width() - 18, 18))

        if self.game_over:
            self._draw_game_over(screen)

    def draw_start_screen(self, screen: pygame.Surface, mouse_position: tuple[int, int]) -> pygame.Rect:
        screen.fill(BACKGROUND)
        self._draw_grid(screen)

        title = self.title_font.render("SNAKE", True, SNAKE_HEAD)
        subtitle = self.font.render("Jogo da Cobrinha", True, TEXT_COLOR)
        screen.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 145))
        screen.blit(subtitle, ((SCREEN_WIDTH - subtitle.get_width()) // 2, 205))

        button = pygame.Rect(0, 0, 220, 64)
        button.center = (SCREEN_WIDTH // 2, 315)
        color = BUTTON_HOVER_COLOR if button.collidepoint(mouse_position) else BUTTON_COLOR
        pygame.draw.rect(screen, color, button, border_radius=10)
        label = self.font.render("INICIAR", True, TEXT_COLOR)
        screen.blit(label, label.get_rect(center=button.center))

        instruction = self.font.render("Clique no botao ou pressione ENTER", True, (160, 181, 191))
        screen.blit(instruction, ((SCREEN_WIDTH - instruction.get_width()) // 2, 405))
        return button

    def _draw_grid(self, screen: pygame.Surface) -> None:
        for x in range(GRID_WIDTH + 1):
            position = x * CELL_SIZE
            pygame.draw.line(screen, GRID_COLOR, (position, HUD_HEIGHT), (position, SCREEN_HEIGHT))
        for y in range(GRID_HEIGHT + 1):
            position = HUD_HEIGHT + y * CELL_SIZE
            pygame.draw.line(screen, GRID_COLOR, (0, position), (SCREEN_WIDTH, position))

    def _draw_game_over(self, screen: pygame.Surface) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - HUD_HEIGHT), pygame.SRCALPHA)
        overlay.fill(OVERLAY_COLOR)
        screen.blit(overlay, (0, HUD_HEIGHT))

        title = self.title_font.render("GAME OVER", True, FOOD_COLOR)
        message = self.font.render("Pressione R ou ENTER para reiniciar", True, TEXT_COLOR)
        area_top = HUD_HEIGHT + (GRID_HEIGHT * CELL_SIZE - title.get_height()) // 2
        screen.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, area_top - 20))
        screen.blit(message, ((SCREEN_WIDTH - message.get_width()) // 2, area_top + 42))

    @staticmethod
    def _cell_rect(cell: tuple[int, int]) -> pygame.Rect:
        x, y = cell
        return pygame.Rect(x * CELL_SIZE, HUD_HEIGHT + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Snake - Jogo da Cobrinha")
    # Sem pygame.RESIZABLE, a janela permanece com dimensoes fixas.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=0)
    _disable_window_resize()
    clock = pygame.time.Clock()
    game = SnakeGame()
    started = False
    running = True

    key_directions = {
        pygame.K_UP: UP,
        pygame.K_w: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_s: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_a: LEFT,
        pygame.K_RIGHT: RIGHT,
        pygame.K_d: RIGHT,
    }
    start_button = pygame.Rect(0, 0, 220, 64)
    start_button.center = (SCREEN_WIDTH // 2, 315)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not started:
                if start_button.collidepoint(event.pos):
                    started = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not started:
                    started = True
                elif event.key == pygame.K_RETURN and game.game_over:
                    game.reset()
                elif event.key in key_directions and started and not game.game_over:
                    game.change_direction(key_directions[event.key])
                elif event.key == pygame.K_r and started and game.game_over:
                    game.reset()

        if started:
            game.update()
            game.draw(screen)
        else:
            start_button = game.draw_start_screen(screen, pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def _disable_window_resize() -> None:
    """Remove a possibilidade de maximizar/redimensionar pela API SDL2."""
    try:
        from pygame._sdl2.video import Window

        # Tambem funciona no Linux/WSL, onde a janela e gerenciada pelo SDL2.
        Window.from_display_module().resizable = False
    except (ImportError, RuntimeError):
        pass

    if sys.platform != "win32":
        return

    import ctypes

    window_handle = pygame.display.get_wm_info().get("window")
    if not window_handle:
        return

    get_window_long = ctypes.windll.user32.GetWindowLongPtrW
    set_window_long = ctypes.windll.user32.SetWindowLongPtrW
    get_window_long.argtypes = [ctypes.c_void_p, ctypes.c_int]
    get_window_long.restype = ctypes.c_longlong
    set_window_long.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_longlong]
    set_window_long.restype = ctypes.c_longlong

    style_index = -16  # GWL_STYLE
    maximize_box = 0x00010000
    thick_frame = 0x00040000
    style = get_window_long(window_handle, style_index)
    set_window_long(window_handle, style_index, style & ~(maximize_box | thick_frame))

    # Atualiza a moldura nativa sem alterar posicao ou tamanho da janela.
    ctypes.windll.user32.SetWindowPos(
        window_handle,
        0,
        0,
        0,
        0,
        0,
        0x0001 | 0x0002 | 0x0004 | 0x0020,  # SWP_NOSIZE|SWP_NOMOVE|SWP_NOZORDER|SWP_FRAMECHANGED
    )


if __name__ == "__main__":
    main()
