import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 400, 400
ROWS, COLS = 10, 10
SQUARE_SIZE = WIDTH // COLS
MINE_COUNT = 10

# Цвета
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper Pygame")
font = pygame.font.SysFont('Arial', 24, bold=True)

def create_board():
    # Создаем пустое поле
    board = [[{'mine': False, 'revealed': False, 'flagged': False, 'neighbors': 0} 
              for _ in range(COLS)] for _ in range(ROWS)]
    
    # Расставляем мины
    mines_placed = 0
    while mines_placed < MINE_COUNT:
        r, c = random.randint(0, ROWS-1), random.randint(0, COLS-1)
        if not board[r][c]['mine']:
            board[r][c]['mine'] = True
            mines_placed += 1
            
    # Считаем соседей
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c]['mine']:
                continue
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc]['mine']:
                        board[r][c]['neighbors'] += 1
    return board

def reveal(board, r, c):
    if board[r][c]['revealed'] or board[r][c]['flagged']:
        return
    board[r][c]['revealed'] = True
    if board[r][c]['neighbors'] == 0 and not board[r][c]['mine']:
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    reveal(board, nr, nc)

def draw(board):
    screen.fill(WHITE)
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            cell = board[r][c]
            
            if cell['revealed']:
                pygame.draw.rect(screen, GRAY, rect)
                if cell['mine']:
                    pygame.draw.circle(screen, BLACK, rect.center, SQUARE_SIZE // 3)
                elif cell['neighbors'] > 0:
                    text = font.render(str(cell['neighbors']), True, BLUE)
                    screen.blit(text, text.get_rect(center=rect.center))
            else:
                pygame.draw.rect(screen, DARK_GRAY, rect)
                if cell['flagged']:
                    pygame.draw.line(screen, RED, rect.topleft, rect.bottomright, 3)
                    pygame.draw.line(screen, RED, rect.topright, rect.bottomleft, 3)
            
            pygame.draw.rect(screen, BLACK, rect, 1) # Сетка
    pygame.display.flip()

def main():
    board = create_board()
    run = True
    game_over = False

    while run:
        draw(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                c, r = x // SQUARE_SIZE, y // SQUARE_SIZE
                
                if event.button == 1: # Левый клик
                    if board[r][c]['mine']:
                        print("БУМ! Проигрыш.")
                        game_over = True
                        # Открываем все мины при проигрыше
                        for row in board:
                            for cell in row:
                                if cell['mine']: cell['revealed'] = True
                    else:
                        reveal(board, r, c)
                
                elif event.button == 3: # Правый клик
                    board[r][c]['flagged'] = not board[r][c]['flagged']

    pygame.quit()

if __name__ == "__main__":
    main()