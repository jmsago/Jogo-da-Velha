import pygame
import sys

# Inicialização do pygame
pygame.init()

# Configurações da janela
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Cores
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Criar a janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Velha")

# Tabuleiro (0 = vazio, 1 = O, 2 = X)
board = [[0]*BOARD_COLS for _ in range(BOARD_ROWS)]

# Desenha as linhas
def draw_lines():
    screen.fill(BG_COLOR)
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2*SQUARE_SIZE), (WIDTH, 2*SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2*SQUARE_SIZE, 0), (2*SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Desenha as marcas (círculos e X)
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                   (col * SQUARE_SIZE + SQUARE_SIZE//2,
                                    row * SQUARE_SIZE + SQUARE_SIZE//2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)

# Verifica vitória
def check_win(player):
    # Linhas
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_win_line(row, 0, row, 2)
            return True
    
    # Colunas
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_win_line(0, col, 2, col)
            return True
    
    # Diagonal principal
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_win_line(0, 0, 2, 2)
        return True

    # Diagonal secundária
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        draw_win_line(0, 2, 2, 0)
        return True

    return False

# Desenha a linha da vitória
def draw_win_line(start_row, start_col, end_row, end_col):
    start_pos = (start_col * SQUARE_SIZE + SQUARE_SIZE//2,
                 start_row * SQUARE_SIZE + SQUARE_SIZE//2)
    end_pos = (end_col * SQUARE_SIZE + SQUARE_SIZE//2,
               end_row * SQUARE_SIZE + SQUARE_SIZE//2)
    pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, WIN_LINE_WIDTH)

# Reinicia o jogo
def restart():
    global board, player, game_over
    board = [[0]*BOARD_COLS for _ in range(BOARD_ROWS)]
    game_over = False
    draw_lines()

# Controle do jogo
player = 1
game_over = False
draw_lines()

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Clique do mouse
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if board[clicked_row][clicked_col] == 0:
                board[clicked_row][clicked_col] = player
                if check_win(player):
                    game_over = True
                player = 2 if player == 1 else 1

                draw_figures()

        # Tecla R para reiniciar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()

    pygame.display.update()
