import pygame as pg, pygame
import math
from time import sleep


class Colors:
    white=(255,255,255)
    red=(255,0,0)
    green=(0,255,0)
    blue=(0,0,255)
    bg=(91,109,126)
    orange=(228,106,107)
    orange2=(200,90,140)


class Images:
    pass


class Car():
    def __init__(self):
        pass


class Track():
    def __init__(self, properties):
        self.inner = properties[0]
        self.outer = properties[1]
        self.miles = properties[2]
        self.innerpoints = properties[3]
        self.outerpoints = properties[4]

    def display(self, disp):
        for i in range(len(self.innerpoints) - 1):
            pygame.draw.lines(disp, Colors.orange, False, self.innerpoints, 5)
            try:
                pygame.draw.lines(disp, Colors.orange, False, self.outerpoints, 5)
            except ValueError:
                pass


def load_images():
    pt_size = (5,5)
    car_size = (50, 24.4)  #image ratio = 2.045045045045:1
    pt_image = pygame.transform.scale(pygame.image.load("resources/point.png").convert_alpha(),pt_size)
    Images.point=pt_image
    car = pg.transform.scale(pg.image.load("resources/lambi.png").convert_alpha(), car_size)


def dist(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def get_inner(px, py, prev):
    #prev contains prev and and this point (px py also)
    global width

    thet = theta(prev) + (math.pi / 2)

    inner = px + (width * math.cos(thet)), py + (width * math.sin(thet))

    return inner


def theta(points):
    p1 = points[0]
    p2 = points[1]

    """Return the angle made by line joining 2 points with x-axis"""
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def renderText(text, pos):
    nexa = pg.font.Font("resources/Nexa Bold.otf", 45)

    t = nexa.render(text,True, Colors.blue)

    rect = t.get_rect()
    rect.center = pos
    disp.blit(t, pos)


def save():
    file = open("track.csv", "w")
    global path, path_inner


width = 100 #width of the track

def trackEditor():
    global width, w, h, clock, disp
    pygame.init()
    pygame.font.init()

    display_info = pygame.display.Info()
    monitor_res = (display_info.current_w, display_info.current_h)

    path_res = 3000 # the more the worse

    w = monitor_res[0]
    h = monitor_res[1]

    clock = pygame.time.Clock()

    disp = pygame.display.set_mode((w, h), flags=pg.FULLSCREEN,depth=16)

    load_images()

    pygame.display.set_caption("Track Editor BETA")

    disp.fill(Colors.bg)

    running = True

    path = []
    path_inner = []

    path_closed = False

    while running:
        disp.fill(Colors.bg)
        keys=pg.key.get_pressed()
        if keys[pg.K_z]:
            try:
                path.pop(-1)
                path_inner.pop(-1)
                sleep(0.05)
            except IndexError:
                print("Already clear.")

        for event in pygame.event.get():
            if pygame.mouse.get_pressed()[0]:
                loc=pg.mouse.get_pos()
                try:
                    if dist(path[-1],loc) > path_res:
                        path.append(loc)
                        if len(path) > 1:
                            path_inner.clear()
                            for i in range(len(path)):
                                path_inner.append(get_inner(path[i][0],path[i][1],[path[i - 1],path[i]]))
                except IndexError:
                    path.append(loc)
                    #path_inner.append(get_inner(loc[0],loc[1], path[-2:]))

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_c:
                    path_closed = not path_closed
                    renderText("Hello", (200,200))
                if event.key == pg.K_g:
                    #generate inner track
                    l=len(path)
                    if l>3:
                        path_inner.clear()
                        for i in range(l):
                            path_inner.append(get_inner(path[i][0], path[i][1], [path[i-1], path[(i + 1) % l]]))
                if event.key == pg.K_ESCAPE:
                    pass
                    #1/0 #masterminds
                if event.key == pg.K_s:
                    #Save track
                    l = len(path)
                    inner, outer, milestones = [], [], []
                    try:
                        for i in range(len(path)):
                            milestones.append(pygame.draw.line(disp, Colors.white, path[i], path_inner[i]))
                            inner.append(pygame.draw.line(disp, Colors.white, path_inner[i], path_inner[(i+1)%l]))
                            outer.append(pygame.draw.line(disp, Colors.white, path[i], path[(i+1)%l]))

                        return inner, outer, milestones, path_inner, path
                    except:
                        inner.clear()
                        outer.clear()
                        milestones.clear()

        #RENDER

        for i in range(len(path) - 1):
            pygame.draw.lines(disp, Colors.orange,path_closed, path,5)
            try:
                pygame.draw.lines(disp,Colors.orange,path_closed,path_inner,5)
            except ValueError:
                pass

        for point in path:
            disp.blit(Images.point, point)

        try:
            for i in range(len(path)):
                pygame.draw.line(disp,Colors.white, path[i], path_inner[i])
                midp = ((path[i][0] + path_inner[i][0])//2, (path[i][1] + path_inner[i][1])//2)
        except:
            pass

        pygame.display.update()

        clock.tick(75)


track = Track(trackEditor())

while True:
    for e in pygame.event.get():
        pass
    disp.fill(Colors.bg)


    clock.tick(75)