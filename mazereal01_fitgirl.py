import pygame
import random
from random import choice


RES = WIDTH, HEIGHT = 600, 600              #çözünürlük
TILE_SIZE = 10                                 # her bir karenin ne kadar geniş olacağı pixel cinsinden
TILE = WIDTH // TILE_SIZE
cols, rows = WIDTH // TILE, HEIGHT // TILE  # sütün ve satır hesaplanıyor

pygame.init()                               # oyunu görüntülemek için birkaçç komut
sc = pygame.display.set_mode(RES)           # oyunun ekranını yukarıda belirlediğimiz çözünürlük ile ayarlıyoz
clock = pygame.time.Clock()                 # oyunun saatini oluşturuyoruz. bu her bir saniyede kaç defa çizim yapılacağı için


class Cell:                                 # o karelere hücre diyoruz ve onun sınıfı burada ve değerlerini giriyoruz
    def __init__(self, x, y):               # burada init dışarda oluştururken birkaç parameter ile oluşturmak için kullanıdğımız bi method
        self.x, self.y = x, y               # burada x ve y konumları için walls her bir hücrenin duvarı var onları başlangıçta true yapıyoruz ki heryer kpalı olsun
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True} 
        self.visited = False                # bu haritayı oluştururken aynı yerden birdaha geçmemek için yazılmış
        self.travelled = False              # bu cevabı ararken birdaha aynı yerden geçmemek için
        self.way = False                    # bu en kısa yolu belirtmek için
        self.wall = False

    def draw_current_cell(self):            # bu ve aşaıdaki draw fonksiyonları tamamen boyama işlemi bu harityaı oluşturan hücre için
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color(122,86,236), (x + 2, y + 2, TILE - 2, TILE - 2))

    def draw_start_cell(self):              # bu başlangıç hücresini boyamak için 
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color(90,156,255), (x + 2, y + 2, TILE - 2, TILE - 2))

    def draw_end_cell(self):                # bu bitiş hücresini boyamak için 
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color(5,74,150), (x + 2, y + 2, TILE - 2, TILE - 2))

    def draw_travelled_cell(self):          # bu cevabı gezen hücreyi boyamak için 
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color(238,162,104), (x + 2, y + 2, TILE - 2, TILE - 2))

    def draw_past_cell(self):               # bu cevabı gezen hücrenin gezdiği yerleri boyamak için 
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color(248,230,197), (x + 2, y + 2, TILE - 2, TILE - 2))

    def draw_way_cell(self):                # bu en kısa yolu boyamak için 
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color(241,194,105), (x + 2, y + 2, TILE - 2, TILE - 2))
        

    def draw(self):                         # burada duvarlar boyanıyor yani başlanıgçta ızgara daha sonra harita oluyor
        x, y = self.x * TILE, self.y * TILE
        if self.visited:                    
            pygame.draw.rect(sc, pygame.Color(184,215,237), (x, y, TILE, TILE))
        if self.walls['top']:
            pygame.draw. line(sc, pygame.Color(132,50,27), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(sc, pygame. Color(132,50,27), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']: 
            pygame.draw.line(sc, pygame.Color (132,50,27), (x + TILE, y + TILE), (x , y + TILE), 2) 
        if self.walls['left']:
            pygame.draw. line(sc, pygame.Color (132,50,27), (x, y + TILE), (x, y) , 2)

    def check_cell(self, x, y):             # burada hücrenin varlığı kontrolü yapılıyor bize verilen kordinatlarda hücre olup olmadığı sorglanıyor
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]
    
    def check_neighbors(self):              # burada komşu kontrolü yapılıyor 
        neighbors = []                       # komşu varsa buraya atıyoruz. aşağıda teker teker kontrol ediyoruz her yöne kontrol ediyoruz.
        top = self.check_cell(self.x, self.y - 1)   
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)

        if top and not top.visited:         # eğer üstümüzde komşu varsa ve daha önce ziyaret edilmemişse komşu septimize atıyoruz.
            neighbors.append(top)
        if right and not right.visited:     # aynı şeyi 3 yön için yapıyoruz. burası haritayı oluştururken daha önce geçip geçmediğimizi kontrol için
            neighbors.append(right)
        if bottom and not bottom.visited:   # bu koda çok benzeri aşağıda var o da cevabı aramak için karıştırma arada fark var
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
    
    def travel_neighbors(self):             # bu da komşuları seyehat ediyor seyehat kalıbı cevabı bulmak için ziyaret oluşturmak için
        neighbors = []                      # yukarıda yapılanların hemen hemen aynısı fark aşağıda
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)

        if top and not top.travelled and not self.walls['top']:
            neighbors.append(top)           # bunun farkı daha önce seyehat edilip edilmediği kontrolü ve o cihette duvarın olup olmadığı kontolü
        if right and not right.travelled and not self.walls['right']:
            neighbors.append(right)         # duvar olmadığı yerlerden hareket edeceğimiz için duvar kontrolü de yapıyoruz
        if bottom and not bottom.travelled and not self.walls['bottom']:
            neighbors.append(bottom)
        if left and not left.travelled and not self.walls['left']:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
    

def remove_walls(current, next):            # duvarlarım yıkılma faailyeti burada gerçekleştiriliyor efenim
    dx = current.x -next.x                  # bu duvar yıkımı fonksiyonunda parametre olarak iki fonksiyon alıyoruz okumaya devam et anlayacaksın sebebini
    if dx == 1:                             
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y -next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False
    
                                            # evrensel değişkenlerimiz burada oluşturduk aşağıda bütün hücrelerimizi tek boyutlu bir dizide saklıyoruz 10x10 için 0 dan 99 gibi
grid_cells = [Cell(col, row)for row in range(rows) for col in range(cols)]     
current_cell = grid_cells[0]                # haritayı oluşturacak olan hücremizi dünyaya salıyoruz
check_cell = grid_cells[0]                  # haritayı oluşturacak olan hücremiz bütün oluşturmayı tamamlanınca başladığı yere geri gelicek onun kontrolü için bunu oluşturdum
                                            # başlangıç ve bitiş için olabilecek konumları ayarlıyor dikkat edilen husus çapraz ve haritanın köşesi olmaları
spawn_point = [(0),((1 * cols) - 1),((rows * cols) - (cols)),((rows * cols) - 1)]
random_cell1 = random.choice(spawn_point)
start_cell = grid_cells[random_cell1]
traveller_cell = start_cell
spawn_point.remove(random_cell1)
random_cell2 = random.choice(spawn_point)
end_cell = grid_cells[random_cell2]         # bu while fonksiyonu başlangıcın çaprazına bitişi koymak için var
while ( abs(random_cell1 - random_cell2) == (cols*(rows-1)) or abs(random_cell1 - random_cell2) == (cols - 1)):
    random_cell2 = random.choice(spawn_point)
    end_cell = grid_cells[random_cell2] 

one_time = 1                                # başlangıçtaki haritayı oluşturan hücremizi yuvasından çıkarmak için bir kereliğine kullandığım değişken.
last_piece = 0                              # bu da seyehatçi hücrenin başlangıçtan çıkıp bitiş hücresine ulaştığını algılayıp en kısa yolu çizmeye başlatmak için oluşturdum

stack = []                                  # burada backtrace adlı bir teknik kullanıyoruz o da last in firt out mantığı ile çalışacak olan stackleri kullanıyor
stack2 = []                                 # bunlardan iki tane ihtiyacım vardı burada onları oluştudum. biri haritayı oluşturmak için ibri çözümü bulmak için

while True:                                 # işte sürekli döngüye giren çalışan yer burası
    [cell.draw() for cell in grid_cells]    # burada bütün hücreler teker teker çiziliyor evet bu bir satır bu büyük işi yapıyor aslında burası bir for döngüsü
    for event in pygame.event.get():        # quit klasik heryerde var önce quit hocam
        if event.type == pygame.QUIT:
            exit()

    
    for cell in grid_cells:                 # hücrelerden herhangi biri seyehar edildi ise çiziver diyorum burada. seyehatçimizin gezdiği yerleri görmek gerek dimi hocam
        if cell.travelled:
                cell.draw_past_cell()

    for cell in grid_cells:                 # burada da en kısa yolu çızdırıyorum
        if cell.way:
                cell.draw_way_cell()

    if one_time == 1:                       # dediğim gibi tek sefere mahsus bi harita oluşturuyorum evinden dışarı atıyorum
        current_cell.visited = True
        current_cell.draw_current_cell()

        next_cell = current_cell.check_neighbors()
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:current_cell = stack.pop()
        one_time += 1

    elif current_cell != check_cell:        # diyorum ki burada da eve gelene kadar dolaş tüm haritayı o yüzden bi seferliğe mahusus kovdum onu
        current_cell.visited = True
        current_cell.draw_current_cell()
        
        next_cell = current_cell.check_neighbors()
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:current_cell = stack.pop()


    
    if current_cell == check_cell:          # eve geldiğinde ise bizim seyehatçiyi yola salıyorum
            traveller_cell.travelled = True
            traveller_cell.draw_travelled_cell()

            next_cell = traveller_cell.travel_neighbors()
            if last_piece == 1:             # eğer bitişi bulduysa geldiğin yoldan geri gel emmi diyorum 
                traveller_cell.draw_way_cell()
                traveller_cell.way = True
                if stack2:traveller_cell = stack2.pop()
                if traveller_cell == end_cell:
                    break
                                            # eğer biitşe ulaşammadıysa seyehat etmeye devam ediyor
            elif traveller_cell != end_cell and next_cell:
                next_cell.travelled = True
                stack2.append(traveller_cell)
                traveller_cell = next_cell
                                            # eğer bitişe ulaştıysa bildiriyor
            elif traveller_cell == end_cell:
                print("yo mister white i made it")
                last_piece = 1
                                            # bitişi ararken arada geri dönmesi icap edebiliyor onun için
            elif stack2:traveller_cell = stack2.pop()

    start_cell.draw_start_cell()            # başlangıç hücremizi çızdır abi. bu iki kafadar en aşağıda çünkü en aşağıda olan çizimde en üstte olur.
    end_cell.draw_end_cell()                # bitişide aradan çıkar

    pygame.display.flip()
    clock.tick(30)

