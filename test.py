import pygame
import random

# Ekran boyutunu ayarla
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Labirent ayarları
CELL_SIZE = 20
WALL_THICKNESS = CELL_SIZE

# İki boyutlu labirent dizisi
maze = []

# Labirenti oluştur
def create_maze():
    global maze
    maze = []
    for i in range(SCREEN_HEIGHT // CELL_SIZE):
        row = []
        for j in range(SCREEN_WIDTH // CELL_SIZE):
            if i == 0 or i == SCREEN_HEIGHT // CELL_SIZE - 1 or j == 0 or j == SCREEN_WIDTH // CELL_SIZE - 1:
                # Labirentin dışındaki tüm hücrelerin duvar olmasını sağla
                row.append(1)
            else:
                # Labirentin içinde rastgele duvar ve patika oluştur
                row.append(random.randint(0, 1))
        maze.append(row)

    # Labirentin başlangıç ve bitiş noktalarını belirle
    start_row = random.randint(1, SCREEN_HEIGHT // CELL_SIZE - 2)
    start_col = random.randint(1, SCREEN_WIDTH // CELL_SIZE - 2)
    end_row = random.randint(1, SCREEN_HEIGHT // CELL_SIZE - 2)
    end_col = random.randint(1, SCREEN_WIDTH // CELL_SIZE - 2)
    maze[start_row][start_col] = 0
    maze[end_row][end_col] = 0

    # Labirenti çöz
    solve_maze(start_row, start_col, end_row, end_col)

# Labirenti çözmek için recursive bir fonksiyon
def solve_maze(row, col, end_row, end_col):
    if row == end_row and col == end_col:
        # Bitiş noktasına ulaşıldı
        return True

    if maze[row][col] == 1:
        # Duvar
        return False

    if maze[row][col] == 2:
        # Ziyaret edildi
        return False

    # Ziyaret edildi olarak işaretle
    maze[row][col] = 2

    # Komşu hücreleri ziyaret et
    if solve_maze(row - 1, col, end_row, end_col): # Kuzey
        return True
    if solve_maze(row + 1, col, end_row, end_col): # Güney
        return True
    if solve_maze(row, col - 1, end_row, end_col): # Batı
        return True
    if solve_maze(row, col + 1, end_row, end_col): # Doğu
        return True

    # Çözülemiyor
    return False

# Pygame başlat
pygame.init()

# Ekran oluştur
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Oyun döngüsü
running = True
while running:
    # Olayları yakala
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Labirenti yeniden oluştur
            create_maze()

# Ekranı temizle
screen.fill(WHITE)

# Labirenti çiz
for row in range(len(maze)):
    for col in range(len(maze[row])):
        if maze[row][col] == 1:
            # Duvar
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        elif maze[row][col] == 2:
            # Çözüm yolu
            pygame.draw.rect(screen, (100, 100, 255), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Başlangıç ve bitiş noktalarını çiz
pygame.draw.circle(screen, (0, 255, 0), (start_col * CELL_SIZE + CELL_SIZE // 2, start_row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
pygame.draw.circle(screen, (255, 0, 0), (end_col * CELL_SIZE + CELL_SIZE // 2, end_row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

# Ekranı güncelle
pygame.display.flip()

pygame.quit()

