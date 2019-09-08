import pygame as pg, pygame
import math
from time import sleep
import neuralnetwork as nn
import csv
import os

abspath = os.path.dirname(os.path.abspath(__file__)) + '\\'
print(abspath)

class Colors:
    white=(255,255,255)
    red=(255,0,0)
    green=(0,255,0)
    blue=(0,0,255)
    bg=(45,45,45)
    orange=(246,114,128)
    orange2=(232,23,93)


class Images:
    pass


class Track():
    def __init__(self, properties):
        self.inner = properties[0]
        self.outer = properties[1]
        self.miles = properties[2]
        self.innerpoints = properties[3]
        self.outerpoints = properties[4]
        self.startpoint = ((self.outerpoints[0][0] + self.innerpoints[0][0]) / 2, (self.outerpoints[0][1] + self.innerpoints[0][1]) / 2)

    def display(self, disp):
        for i in range(len(self.innerpoints) - 1):
            pygame.draw.lines(disp, Colors.orange, True, self.innerpoints, 5)
            try:
                pygame.draw.lines(disp, Colors.orange, True, self.outerpoints, 5)
            except ValueError:
                pass

        for rect in self.outer:
            displayRect(rect, disp)

    def calc_slopes(self):
        self.slopes = []

    def saveTrack(self, name):
        v_out = []
        v_in = []
        trans_vect = (self.innerpoints[0][0] - self.outerpoints[0][0],self.innerpoints[0][1] - self.outerpoints[0][1])
        l = len(self.outerpoints)

        for i in range(l):
            v_out.append((self.outerpoints[(i+1)%l][0] - self.outerpoints[i][0],self.outerpoints[(i+1)%l][1] - self.outerpoints[i][1]))
            v_in.append((self.innerpoints[(i + 1) % l][0] - self.innerpoints[i][0],self.innerpoints[(i + 1) % l][1] - self.innerpoints[i][1]))

        file = open(abspath + "tracks\\{}.track".format(name), "w", newline='')
        writer = csv.writer(file)
        writer.writerow([str(l), str(trans_vect[0]), str(trans_vect[1])]) #First line: total vectors for each, trans vect x, trans vect y
        for v in v_out:
            writer.writerow([str(i) for i in v])
        for w in v_in:
            writer.writerow([str(int(i)) for i in w])
        file.close()


def displayRect(rect, disp):
    pygame.draw.lines(disp,Colors.white,True, [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft])


def load_images():
    global width

    pt_size=(5,5)
    pt_image=pygame.transform.scale(pygame.image.load(abspath + "resources\\point.png").convert_alpha(),pt_size)
    Images.point=pt_image

    #Load Purple Lamborghini
    orig = (615, 316)
    factor = 3
    new_h = int(width/factor)

    fac = new_h / orig[1]

    car_size = (int(orig[0] * fac), new_h)

    Images.car = pg.transform.scale(pg.image.load(abspath + "resources\\lambi2.png").convert_alpha(), car_size)


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


def renderText(text, pos, color, disp):
    nexa = pg.font.Font(abspath + "resources\\Nexa Bold.otf", 45)

    t = nexa.render(text,True, color)

    rect = t.get_rect()
    rect.center = pos
    disp.blit(t, pos)


def save():
    pass


width = 75 #width of the track


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

    disp = pygame.display.set_mode((w, h), flags = pg.FULLSCREEN,depth=16)

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
                if event.key == pg.K_g:
                    #generate inner track
                    l=len(path)
                    if l>3:
                        path_inner.clear()
                        for i in range(l):
                            path_inner.append(get_inner(path[i][0], path[i][1], [path[i-1], path[(i + 1) % l]]))
                if event.key == pg.K_ESCAPE:
                    pygame.quit()
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
                pass
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

        renderText("S: Save    G: Smooth     C: Render Closed     Esc: Exit", (70, 40), Colors.orange, disp)
        pygame.display.update()

        clock.tick(75)

track = Track(trackEditor())
track.saveTrack("First")

print("Bye ~nyan")
