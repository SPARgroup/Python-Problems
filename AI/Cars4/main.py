import track as vs
from track import Images, Colors
import neuralnetwork as nn
import pygame as pygame

""""Script 3000¹"""#Respect++ Mission passed (with flying colors)
class Car(nn.Brain):

    def __init__(self):
        nn.Brain.__init__(self) # also pass params
        self.s = 0
        self.w = 0
        self.a =0
        self.image = Images.car
        self.body = self.image.get_rect()
        self.theta = 0
        self.pos = [0, 0]

    def render(self):
        global disp
        self.body.center = self.pos
        rotated = pygame.transform.rotate(self.image, self.theta)
        disp.blit(rotated, self.body)



track = vs.Track(vs.trackEditor())
track.saveTrack("First")

pygame.init()

pygame.font.init()

display_info = pygame.display.Info()
monitor_res = (display_info.current_w, display_info.current_h)

path_res = 3000 # the more the worse

w = monitor_res[0]
h = monitor_res[1]

clock = pygame.time.Clock()

disp = pygame.display.set_mode((w, h),depth=16)

pygame.display.set_caption("Race4")

disp.fill(Colors.bg)

running = True

boi = Car()
boi.pos = track.startpoint
omega = 20
while running:
    disp.fill(Colors.bg)
    for e in pygame.event.get():
        pass
    boi.theta += omega * 0.013
    boi.render()
    track.display(disp)
    pygame.display.update()
    clock.tick(75)







