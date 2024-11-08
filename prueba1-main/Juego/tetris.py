import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 480, 800  # Ventana más grande
BLOCK_SIZE = 40  # Tamaño de los bloques (más grande)
ROWS, COLS = HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (255, 0, 0),   # Rojo
    (0, 255, 0),   # Verde
    (0, 0, 255),   # Azul
    (255, 255, 0), # Amarillo
    (255, 165, 0), # Naranja
    (128, 0, 128), # Morado
    (0, 255, 255)  # Cian
]

# Formas de las piezas
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

# Clase para las piezas
class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Crear la matriz del juego
def create_board():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Dibujar la cuadrícula
def draw_board(surface, board):
    for r in range(ROWS):
        for c in range(COLS):
            if isinstance(board[r][c], tuple):
                pygame.draw.rect(surface, board[r][c], (c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(surface, BLACK, (c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Comprobar colisiones
def valid_space(piece, board):
    for r in range(len(piece.shape)):
        for c in range(len(piece.shape[r])):
            if piece.shape[r][c]:
                if (piece.x + c < 0 or piece.x + c >= COLS or
                    piece.y + r >= ROWS or (piece.y + r >= 0 and isinstance(board[piece.y + r][piece.x + c], tuple))):
                    return False
    return True

# Unir la pieza con el tablero
def merge(piece, board):
    for r in range(len(piece.shape)):
        for c in range(len(piece.shape[r])):
            if piece.shape[r][c]:
                board[piece.y + r][piece.x + c] = piece.color

# Limpiar líneas completas
def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0 for _ in range(COLS)])
    return new_board, lines_cleared

# Función para mostrar el menú de pausa
def pause_menu(surface):
    font = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)
    paused_text = font.render("PAUSADO", True, WHITE)
    resume_text = font_small.render("Presiona 'R' para continuar", True, WHITE)
    quit_text = font_small.render("Presiona 'Q' para salir", True, WHITE)
    
    surface.fill(BLACK)
    surface.blit(paused_text, (WIDTH // 4, HEIGHT // 4))
    surface.blit(resume_text, (WIDTH // 8, HEIGHT // 2))
    surface.blit(quit_text, (WIDTH // 8, HEIGHT // 2 + 40))
    pygame.display.flip()

# Función para mostrar el mensaje de "Game Over"
def game_over_menu(surface, score):
    font = pygame.font.Font(None, 74)
    font_small = pygame.font.Font(None, 36)
    game_over_text = font.render("GAME OVER", True, WHITE)
    score_text = font_small.render(f"Puntuación: {score}", True, WHITE)
    restart_text = font_small.render("Presiona 'R' para reiniciar", True, WHITE)
    quit_text = font_small.render("Presiona 'Q' para salir", True, WHITE)

    surface.fill(BLACK)
    surface.blit(game_over_text, (WIDTH // 4, HEIGHT // 4))
    surface.blit(score_text, (WIDTH // 8, HEIGHT // 2))
    surface.blit(restart_text, (WIDTH // 8, HEIGHT // 2 + 40))
    surface.blit(quit_text, (WIDTH // 8, HEIGHT // 2 + 80))
    pygame.display.flip()

# Función principal
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # Inicializar variables del juego
    board = create_board()
    piece = Piece()
    fall_time = 0
    fall_speed = 500  # Tiempo en milisegundos
    score = 0  # Inicializar la puntuación
    running = True
    paused = False  # Estado de pausa

    while running:
        fall_time += clock.get_time()
        clock.tick(60)

        if not paused:
            if fall_time >= fall_speed:
                piece.y += 1
                if not valid_space(piece, board):
                    piece.y -= 1
                    merge(piece, board)
                    piece = Piece()
                    if not valid_space(piece, board):
                        # Mostrar menú de Game Over
                        while True:
                            game_over_menu(screen, score)
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_r:  # Reiniciar
                                        main()  # Reiniciar el juego
                                    if event.key == pygame.K_q:  # Salir
                                        running = False
                        break
                    board, lines_cleared = clear_lines(board)
                    score += lines_cleared * 100  # Incrementar la puntuación
                fall_time = 0

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Presiona 'P' para pausar
                    paused = not paused
                if paused:
                    if event.key == pygame.K_r:  # Presiona 'R' para reanudar
                        paused = False
                    if event.key == pygame.K_q:  # Presiona 'Q' para salir
                        running = False
                else:
                    if event.key == pygame.K_LEFT:
                        piece.x -= 1
                        if not valid_space(piece, board):
                            piece.x += 1
                    if event.key == pygame.K_RIGHT:
                        piece.x += 1
                        if not valid_space(piece, board):
                            piece.x -= 1
                    if event.key == pygame.K_DOWN:
                        piece.y += 1
                        if not valid_space(piece, board):
                            piece.y -= 1
                    if event.key == pygame.K_UP:
                        piece.rotate()
                        if not valid_space(piece, board):
                            piece.rotate()
                    if event.key == pygame.K_SPACE:  # Presiona 'ESPACIO' para bajar la pieza instantáneamente
                        while valid_space(piece, board):
                            piece.y += 1
                        piece.y -= 1  # Ajustar la posición para que no se salga

        # Dibujar todo
        screen.fill(BLACK)
        draw_board(screen, board)

        # Dibujar la pieza actual con su color
        for r in range(len(piece.shape)):
            for c in range(len(piece.shape[r])):
                if piece.shape[r][c]:
                    pygame.draw.rect(screen, piece.color, 
                                     ((piece.x + c) * BLOCK_SIZE, (piece.y + r) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Mostrar la puntuación
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Puntuación: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Mostrar menú de pausa si está pausado
        if paused:
            pause_menu(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()