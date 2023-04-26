import pygame
import random
import time
import math
from queue import PriorityQueue
import requests
import datetime
import button
import tkinter as tk

pygame.init()
#renk ve çözünürlük sabit veriler giriliyor
WIDTH = 600
HEIGHT = 800
ROBOT = (0, 35, 223)
TARGET = (255, 79, 20)
WALL = (25, 25, 25)
LAKE_SAFE = (0, 211, 248)
HOUSE_SAFE = (255, 209, 90)
TREE_SAFE = (108, 201, 113)
LAKE_UNSAFE = (4, 5, 87)
HOUSE_UNSAFE = (255, 132, 0)
TREE_UNSAFE = (33, 46, 17)
PATH = (206, 164, 119)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
#çözünürlük ve isim veriliyor
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("first attempt")
#start ve exit resimleri yükleniyor
start_img = pygame.image.load('start_btn.png').convert_alpha()
exit_img = pygame.image.load('exit_btn.png').convert_alpha()
#start ve exit butonları ayarlanıyor
exit_button = button.Button(380, 660, exit_img, 0.5)
start_button = button.Button(100, 660, start_img, 0.5)
#hücrelerimizin classı burada
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

#bu ekrandaki konumu döndürmek için

    def get_pos(self):
        return self.row, self.col
#buradali is ile başlayamlar kontrol amaçı hani gezerken neymiş ne değilmiş diye bakıcak ya bu is fonksiyonlarıyla sorguluyor
    def is_closed(self):
        return self.color == RED
#bu ekrandaki konumu döndürmek için
    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_tree(self):
        return self.color == TREE_SAFE

    def is_lake(self):
        return self.color == LAKE_SAFE

    def is_house(self):
        return self.color == HOUSE_SAFE

    def is_robot(self):
        return self.color == ROBOT

    def is_target(self):
        return self.color == TARGET

    def is_path(self):
        return self.color == PATH

    def is_tree(self):
        return self.color == TREE_SAFE

    def is_wall(self):
        return self.color == WALL

    def reset(self):
        self.color = WHITE
#buradaki make fonksiyonları hücreleri boyamak için yapıyor yani
    def make_start(self):
        self.color = ORANGE
#burada gecikme ekledim görelim diye yavaş yavaş
    def make_closed(self):
        time.sleep(0.05)
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_tree(self):
        self.color = TREE_SAFE

    def make_lake(self):
        self.color = LAKE_SAFE

    def make_house(self):
        self.color = HOUSE_SAFE

    def make_robot(self):
        self.color = ROBOT

    def make_target(self):
        self.color = TARGET

    def make_path(self):
        self.color = PATH

    def make_tree(self):
        self.color = TREE_SAFE

    def make_wall(self):
        self.color = WALL

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        time.sleep(0.1)
        self.color = PURPLE
#bu fonksiyon her bir hücreye sorulacak ve kendi rengini kendi konumuna boyayacak
    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

#çevresini kontrol edecek burada 3 tip bariyer kontrolü ve var olup olmadığı kontrolü ardından hala gezilebilir ise komşu stack ine ekleyecek
    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not (grid[self.row + 1][self.col].is_barrier() or grid[self.row + 1][self.col].is_tree() or grid[self.row + 1][self.col].is_lake() or grid[self.row + 1][self.col].is_house() or grid[self.row + 1][self.col].is_wall()):
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not (grid[self.row - 1][self.col].is_barrier() or grid[self.row - 1][self.col].is_tree() or grid[self.row - 1][self.col].is_house() or grid[self.row - 1][self.col].is_lake() or grid[self.row - 1][self.col].is_wall()):  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_rows - 1 and not (grid[self.row][self.col + 1].is_barrier() or grid[self.row][self.col + 1].is_lake() or grid[self.row][self.col + 1].is_tree() or grid[self.row][self.col + 1].is_house() or grid[self.row][self.col + 1].is_wall()):
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not (grid[self.row][self.col - 1].is_barrier() or grid[self.row][self.col - 1].is_house() or grid[self.row][self.col - 1].is_tree() or grid[self.row][self.col - 1].is_lake() or grid[self.row][self.col - 1].is_wall()):  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
#geldiği bir önceki yolu geri dönerek ve her defasında boyayarak bize ne kısa yolu gösterecek
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
        pygame.display.update()
#çözüm algoritması burada
def algorithm(draw, grid, start, end, way_counter):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
#burada olaylara en son olan işleri ilk kontrol ederek yaklaşıyoruz
#burada eğer robotumuz bitişe ulaştı ise en kısa yolu inşa ediyor
# ve gezilen tüm yerleri bize yazdırıyor
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            print("gidilen yer " + str(way_counter))
            return True
#komşu kontrolü burada yapılıyor
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

#ekranı çizdiriyoruz
        draw()
        pygame.display.update()

        if current != start:
            current.make_closed()
            way_counter += 1

    
    return False
#ızgara oluştruma fonku
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid
#ızgara çizdirme fonku
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
#bütün ekranı çizme fonku
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
#geçen zamanı ölçen fonk
def time_passed(start_timee):
    start_time = start_timee
    end_time = datetime.datetime.now()
    gecen_sure = end_time - start_time
    print("Geçen süre (saniye): ", gecen_sure.total_seconds())
    return(gecen_sure.total_seconds())
    




#ana fonk
def main(win, width):
    url = "http://bilgisayar.kocaeli.edu.tr/prolab2/url1.txt"

    response = requests.get(url)
    if response.status_code == 200:
        veri = response.content 
    else:
        print("Bir hata oluştu:", response.status_code)



    with open("labby.txt", "wb") as f:
        f.write(veri)
    print("Veri dosyaya kaydedildi.")

    with open("labby.txt") as f:
        a = f.readlines()
    a.append("\n")
    lenght = len(a)
    ROWS = len(a) + 2
    grid = make_grid(ROWS, WIDTH)
    lenght = len(a)
    ROWS = len(a) + 2
    grid = make_grid(ROWS, WIDTH)
    start_point = [0,0]
    end_point = [0,0]
    spawn_point = []
    row = 0
    way_counter = 0
    col = 0
    for i in a:
        col = 0
        row += 1
        for j in i:
            col += 1
            if j == "0" and row <= lenght and col <= lenght:
                spawn_point.append([row, col])
#başlangıç ve bitiş noktamızı rastgele seçip main fonksiyonumuzu randım değerlerini veridkten sonra çalıştırıyoruz
    print(spawn_point)
    start_point = random.choice(spawn_point)
    spawn_point.remove(start_point)
    end_point = random.choice(spawn_point)
#ekranda göstermek için font ızgara başlangıç ve bitiş noktaları ayarlanıyor
    font = pygame.font.Font('freesansbold.ttf', 32)

    grid = make_grid(ROWS, width)
    start = None
    end = None
    row, col = 1, 1
    spot = grid[row][col]
    total_time = 0
    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # durumumuzu çizdiriyoruz
        draw(win, grid, ROWS, width)

        #start butonuna bastığımızda algoritmayı çalıştırıyoruz sayaç ile ölçüyoruz
        if start_button.draw(WIN):
            for row in grid:
                    for spot in row:
                            spot.update_neighbors(grid)
            start_time = datetime.datetime.now()
            algorithm(lambda: draw(win, grid, ROWS, width),
                      grid, start, end, way_counter)
            total_time = time_passed(start_time)

#exit butonuna tıklar isek çıkış yapıyoruz
        if exit_button.draw(WIN):
            run = False
        
#burada url den çektiğimiz text dosyasını okuyoruz ve teker teker bakıyoruz duruma göre hücreleri karşılık gelen değerleri boyuyoruz
        c = 1
        for i in a:
            c += 1
            if col < lenght + 1:
                print(c)
                for j in i:
                    if j == "0":
                        row += 1
                        spot = grid[row][col]
                    elif j == "1":
                        spot.make_tree()
                        row += 1
                        spot = grid[row][col]
                    elif j == "2":
                        spot.make_house()
                        row += 1
                        spot = grid[row][col]
                    elif j == "3":
                        spot.make_lake()
                        row += 1
                        spot = grid[row][col]
                    elif j == lenght-1:
                        break
            row = 1
            col += 1
            if col == lenght:
                break
#rastgele çesilen başlangıç noktamızı boyuyoruz
        row, col = start_point
        spot = grid[row][col]
        start = spot
        start.make_robot()
#rastgele çesilen bitiş noktamızı boyuyoruz
        row, col = end_point
        spot = grid[row][col]
        end = spot
        end.make_target()
#ekranın en dışındaki surlarımızı boyuyoruz
        row = 0
        col = 0
        while True:
            i = 0
            spot = grid[row][col]
            spot.make_wall()
            row += 1
            if row == lenght + 1:
                break
        row = 0
        col = 0
        while True:
            i = 0
            spot = grid[row][col]
            spot.make_wall()
            col += 1
            if col == lenght + 1:
                break
        row = lenght + 1
        col = 0
        while True:
            i = 0
            spot = grid[row][col]
            spot.make_wall()
            col += 1
            if col == lenght + 1:
                break
        row = 0
        col = lenght + 1
        while True:
            i = 0
            spot = grid[row][col]
            spot.make_wall()
            row += 1
            if row == lenght + 1:
                break

        spot = grid[lenght + 1][lenght + 1]
        spot.make_wall()


        font = pygame.font.SysFont("arial", 24)
        text = font.render("Gidilen Adım", True, (0,0,0))
        WIN.blit(text, (50, 607))
        font = pygame.font.SysFont("arial", 24)
        text = font.render("Geçen Süre", True, (0,0,0))
        WIN.blit(text, (336, 607))
        font = pygame.font.SysFont("arial", 24)
        text = font.render(str(way_counter), True, (0,0,0))
        WIN.blit(text, (186, 607))
        font = pygame.font.SysFont("arial", 24)
        text = font.render(str(total_time), True, (0,0,0))
        WIN.blit(text, (476, 607))
        pygame.display.update()

    pygame.quit()
#başlatmak için
def do_everything():
    main(WIN, WIDTH)

do_everything()


