#pygame importálása
import pygame, sys

#inicializáció
pygame.init()
pygame.font.init()

#óra beállítása
clock = pygame.time.Clock()

#megjelenő ablak neve és ikonja
pygame.display.set_caption("Mandala készítés")
icon = pygame.image.load('mandala.png')
pygame.display.set_icon(icon)

#képernyő készítés
screen_width = 600
screen_lenght = 700
screen = pygame.display.set_mode((screen_width,screen_lenght))

#háttérhez használt kép
hatter = pygame.image.load('hattter.png')

#konstans megalkotása a szöveges megjelenéshez
font = pygame.font.SysFont("comicsansms", 30)
smallfont = pygame.font.SysFont("comicsansms", 14)

#színek megadása
sargas = (255,255,51)
kekes = (0,204,204)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,255,0)
green = (0,0,255)

#rajzoláshoz használt felület konstansai
ROWS = COLS = 150
toolbar_height = screen_lenght - screen_width
pixel_size = screen_width // COLS
bg_color = white
draw_grid_lines = False
alapkorImg = pygame.image.load('oval.png')

#a kör felhelyezése a rajzfelületre
def alapkor(x,y):
    screen.blit(alapkorImg, (x,y))

#szövegekhez használt függvény
def get_font_paint(size):
    return pygame.font.SysFont("comicsans", size)

#rajzoló felülethez használt függvények
def draw_grid(screen, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(screen, pixel, (j * pixel_size, i* pixel_size, pixel_size, pixel_size ))

    if draw_grid_lines:
        for i in range(ROWS + 1):
            pygame.draw.line(screen, black, (0, i*pixel_size), (screen_width, i* pixel_size))

        for i in range(COLS + 1):
            pygame.draw.line(screen, black, ( i*pixel_size, 0 ), (i* pixel_size, screen_lenght - toolbar_height))

def draw(screen, grid, buttons):
    screen.fill(bg_color)
    draw_grid(screen, grid)

    for button in buttons:
        button.draw(screen)

def init_grid(rows, cols, color):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(cols):
            grid[i].append(color)
    
    return grid

def get_row_col_from_pos(pos):
    x, y = pos
    row = y // pixel_size
    col = x // pixel_size 

    if row >= ROWS:
        raise IndexError

    return row, col

def get_row_col_from_pos1(pos):
    x, y = pos
    row1 = y // pixel_size *(-1)
    col1 = x // pixel_size * (-1)

    if row1 >= ROWS:
        raise IndexError

    return row1, col1

def get_row_col_from_pos2(pos):
    x, y = pos
    row2 = (y // pixel_size) * (-1)
    col2 = (x // pixel_size)

    if row2 >= ROWS:
        raise IndexError

    return row2, col2

def get_row_col_from_pos3(pos):
    x, y = pos
    row3 = (y // pixel_size)
    col3 = (x // pixel_size) * (-1)

    if row3 >= ROWS:
        raise IndexError

    return row3, col3

#rajzolásnál használt színeket tartalmazó gombokhoz felhasznált osztály
class Button:
    def __init__(self, x,y, width, height, color, text = None, text_color=black):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color
    
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        if self.text:
            pygame.draw.rect(screen, black, (self.x, self.y, self.width, self.height), 2)
            button_font = get_font_paint(15)
            text_surface = button_font.render(self.text, 1, self.text_color)
            screen.blit(text_surface, (self.x + self.width/2 - text_surface.get_width()/2, self.y + self.height/2 - text_surface.get_height()/2))

    def clicked(self, pos):
        x, y = pos

        if not ( x>= self.x and x <= self.x + self.width):
            return False
        if not (y >= self.y and y <= self.y + self.height):
            return False

        return True

#egy tengelyes rajzoláshoz felhasznált függvény
def egytengelyes_rajzolas():
    startText = font.render("Mandala készítő", True, kekes)
    grid = init_grid(ROWS, COLS, bg_color)
    drawing_color = black

    button_y = screen_lenght - toolbar_height/2 -25
    buttons = [
        Button(10, button_y, 50, 50, black),
        Button(70, button_y, 50, 50, red),
        Button(130, button_y, 50, 50, green),
        Button(190, button_y, 50, 50, blue),
        Button(250, button_y, 50, 50, white, "Törlés", black),
        Button(310, button_y, 50, 50, white, "Újra", black)
    ]
    
    while True:
        screen.fill((0,0,0))
        screen.blit(startText, ((screen_width - startText.get_width())/2,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                try:
                    row, col = get_row_col_from_pos(pos)
                    grid[row][col] = drawing_color
                    row3, col3 = get_row_col_from_pos3(pos)
                    grid[row3][col3] = drawing_color
                except IndexError:
                    for button in buttons:
                        if not button.clicked(pos):
                            continue
                        drawing_color = button.color
                        
                        if button.text == "Újra":
                            grid = init_grid(ROWS, COLS, bg_color)
                            drawing_color = black
        
        draw(screen, grid, buttons)
        alapkor(screen_width/2 - alapkorImg.get_width()/2, (screen_lenght/2 - alapkorImg.get_height()/2) - 51)
        screen.blit(startText, ((screen_width - startText.get_width())/2,0))
        
        save_button = create_button( screen_width - 130, 600, 125, 26, sargas, (87,255,255))
        savebuttontext = smallfont.render("Mentés", True, (54,23,65))
        if save_button:
            fname = "mandala.png"
            pygame.image.save(screen, fname)
            print("Lementetted a képet".format(fname))
        screen.blit(savebuttontext, (screen_width - 125,602))
        
        pygame.display.update()
        clock.tick(15)
        
#kéttengelyes rajzoláshoz felhasznált függvény
def kettengelyes_rajzolas():
    startText = font.render("Mandala készítő", True, kekes)
    grid = init_grid(ROWS, COLS, bg_color)
    drawing_color = black

    button_y = screen_lenght - toolbar_height/2 -25
    buttons = [
        Button(10, button_y, 50, 50, black),
        Button(70, button_y, 50, 50, red),
        Button(130, button_y, 50, 50, green),
        Button(190, button_y, 50, 50, blue),
        Button(250, button_y, 50, 50, white, "Törlés", black),
        Button(310, button_y, 50, 50, white, "Újra", black)
    ]

    while True:
        screen.fill((0,0,0))
        screen.blit(startText, ((screen_width - startText.get_width())/2,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                try:
                    row, col = get_row_col_from_pos(pos)
                    grid[row][col] = drawing_color
                    row1, col1 = get_row_col_from_pos1(pos)
                    grid[row1][col1] = drawing_color
                    row2, col2 = get_row_col_from_pos2(pos)
                    grid[row2][col2] = drawing_color
                    row3, col3 = get_row_col_from_pos3(pos)
                    grid[row3][col3] = drawing_color
                except IndexError:
                    for button in buttons:
                        if not button.clicked(pos):
                            continue
                        drawing_color = button.color
                        
                        if button.text == "Újra":
                            grid = init_grid(ROWS, COLS, bg_color)
                            drawing_color = black
        
        draw(screen, grid, buttons)
        alapkor(screen_width/2 - alapkorImg.get_width()/2, (screen_lenght/2 - alapkorImg.get_height()/2) - 51)
        screen.blit(startText, ((screen_width - startText.get_width())/2,0))
        
        save_button = create_button( screen_width - 130, 600, 125, 26, sargas, (87,255,255))
        savebuttontext = smallfont.render("Mentés", True, (54,23,65))
        if save_button:
            fname = "mandala.png"
            pygame.image.save(screen, fname)
            print("Lementetted a képet".format(fname))
        screen.blit(savebuttontext, (screen_width - 125,602))

        pygame.display.update()
        clock.tick(15)
        
#a léptető gombokhoz létrehozott függvény
def create_button(x, y, width, heigh, hovercolor, defaultcolor):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)
    if x + width > mouse[0] and y + heigh > mouse[1] > y:
        pygame.draw.rect(screen, hovercolor, (x, y, width, heigh))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, defaultcolor, (x,y, width, heigh))
    
#kezdő oldalhoz felhasznát függvény
def start_menu():
    startText = font.render("Mandala készítő", True, kekes)
    
    while True:
        screen.fill((0,0,0))
        screen.blit(startText, ((screen_width - startText.get_width())/ 2, 0))
        screen.blit(hatter, (50,100))

        start_button = create_button( screen_width - 130, 7, 125, 26, sargas, (87,255,255))
        if start_button:
            first_level()
        startbuttontext = smallfont.render("Kezdődjön", True, (54,23,65))
        screen.blit(startbuttontext, (screen_width - 125,9))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()
        clock.tick(15)
        return True
    
#A tükrözési tengelyek számának kiválasztásához használt függvény
def first_level():
    startText = font.render("Mandala készítés", True, kekes)
    ketto_tengely_aktiv = False
    negy_tengely_aktiv = False
    valasztas = " "
    kerdes = font.render("Mennyi tükrözési tengellyel dolgoznál?", True, sargas)
    kettengely = pygame.image.load("egytengelyes2.png")
    negytengely = pygame.image.load("kettengelyes2.png")

    while True:
        screen.fill((0,0,0))
        screen.blit(startText, ((screen_width - startText.get_width())/2,0))

        keret_ketto = pygame.Rect((screen_width * 0.0325) - 4 , (screen_lenght * .45) -4, kettengely.get_width() + 8, kettengely.get_height() + 8)
        keret_negy = pygame.Rect((screen_width * 0.5325) - 4 , (screen_lenght * .45) - 4, negytengely.get_width() + 8, negytengely.get_height() + 8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if keret_ketto.collidepoint(event.pos):
                    ketto_tengely_aktiv = True    
                elif keret_negy.collidepoint(event.pos):
                    negy_tengely_aktiv = True   
                else:
                    ketto_tengely_aktiv = False
                    negy_tengely_aktiv = False

        if ketto_tengely_aktiv:
            ketto = font.render("Egy tengelyes",True, kekes)
            pygame.draw.rect(screen, (250,250,250), keret_ketto, 2)
            negy_tengely_aktiv = False       
        else:
            ketto = font.render("Egy tengelyes", True, kekes)
            pygame.draw.rect(screen, (0,0,0), keret_ketto, 2)

        if negy_tengely_aktiv:
            negy = font.render("Két tengelyes",True, kekes)
            pygame.draw.rect(screen, (250,250,250), keret_negy, 2)
            ket_tengely_aktiv = False    
        else:
            negy = font.render("Két tengelyes", True, kekes)
            pygame.draw.rect(screen, (0,0,0), keret_negy, 2)

        screen.blit(kerdes, ((screen_width - kerdes.get_width())/ 2 , screen_lenght * 0.35))
        
        screen.blit(negytengely, (screen_width * 0.5325, screen_lenght * 0.45))
        screen.blit(negy, (screen_width * 0.5325, screen_lenght * 0.80))
        
        screen.blit(kettengely, (screen_width * 0.0325, screen_lenght * 0.45))
        screen.blit(ketto, (screen_width *0.0325 , screen_lenght * 0.80))
    
        submitButton2 = create_button(screen_width - 130, 50, 125, 26, sargas, (87,255,255) )
        if submitButton2:
            egytengelyes_rajzolas()
        submitButtontext2 = smallfont.render("Egy", True, (54,23,65))
        screen.blit(submitButtontext2, (screen_width - 125,52))

        submitButton1 = create_button(screen_width - 130, 100, 125, 26, sargas, (87,255,255) )
        if submitButton1:
            kettengelyes_rajzolas()
        submitButtontext1 = smallfont.render("Kettő", True, (54,23,65))
        screen.blit(submitButtontext1, (screen_width - 125,102))
        
        pygame.display.update()
        clock.tick(15)

#A játék alapja
while True:
    
    start_menu()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(15)
