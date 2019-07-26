import pygame as pg, pygame
from time import sleep
import copy
from random import randint, randrange, choice
from os import system
import sys
from threading import Thread
import math

#colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
bgColor = (0, 160, 250)
orange = (228, 106, 107)
orange2 = (200, 90, 140)
invincibleColor = (60,206,209)
slowmotionColor = (238,169,144)

#variables
pygame.init()
GAME_TITLE = "ArcadeJump"
VERSION = "[BETA]"

won = False

FPS = 75

won_message = ["Level Succesfully Completed", "You Won!", "Well Done Soldier"]
lost_message = ["Oops! Try Again!", "There is always a next time"]

NORMAL_PERIOD = FPS - 20
UPDATE_PERIOD = NORMAL_PERIOD #increasing this would induce slow motion
SLOWMOTION_PERIOD = FPS + 20

display_info = pygame.display.Info()
monitor_res = (display_info.current_w, display_info.current_h)

w = monitor_res[0]
h = monitor_res[1]

ballOffset = 50
res = (w, h)

clock = pygame.time.Clock()

rotationSpeed = -50  #negative = clockwise

friction = 2
drag = 1.5

currentAngle = 0

obs = '@'
surface = "#"

view = 0

block_size = (5, 20) #pixels
ball_size = (30, 30) #has to be square

size = res[0] // block_size[0]
acc = 1500 #pixels per second squared downwards taken positive

pos = [size/2, 0]
vel = 0
currentDisc = 0
game_complete = False

gap = 150 #pixels b/w 2 consecutive discs
max_vel = math.sqrt(2 * (gap - 20) * acc) - 50

move_view_speed = int(max_vel / 3)

level_len = 25 #number of discs total (including blanks)

pre = ball_size[0] // block_size[0] * 3
hole_sizes = [pre+10, pre+14, pre+15, pre+16]

pre *= 1.5
pre = int(pre)
obs_sizes = [pre+1, pre+3, pre+4, pre+5]
powerup_sizes = obs_sizes

l = [] #main game array
disc_positions = []


#init stuff
disp = pygame.display.set_mode((w, h), flags=pygame.FULLSCREEN, depth=16)

pygame.display.set_caption(GAME_TITLE+VERSION)

disp.fill(bgColor)

running = True

viewMoverThreads = []
popperThreads = []

powerups = []
icons = []

viewMoved = 0

multiplier = 1
max_multiplier = 5
bounces = 1 #bounces since crossing last disc

score= 0
scorePerBounce = 100

filename ="savedata/game_save_data.ARCADEJUMP"


#highscore
highscores = []
highscore_mode = "EASY"

file_invalid_or_not_created = False
try:
    scorefile = open(filename, "r")
    try:
        string=scorefile.read().split("\n")
        for sc in string:
            highscores.append(int(sc))
    except:
        file_invalid_or_not_created=True
        print("Warning: Something wrong with the scorefile.")
        highscores = [0,0,0]
except:
    file_invalid_or_not_created=True
    highscores = [0,0,0]

score_string = str(score)
disp_added = None
added = 0

mode = 0 #of difficulty
mode_name = "EASY"

"""Trails list contains tuples for a coordinate which has to be rendered as a trail"""
trail_l = []  #experimental
trail_r = []
trail_len = 12 #pixels
trail_color = orange
trail_size = 5 #pixels
trail_thickness = (4, trail_size) #Dont modify
render_trail = False

for i in range(trail_len):
    trail_l.append([0,0])
    trail_r.append([0,0])

#some funcs


#Classes

class images:
    pass


class fonts:
    score = "resources/6809 chargen.ttf"
    winorlose = "resources/ARCADECLASSIC.ttf"


class Ball:
    global acc
    global w
    def __init__(self):
        self.x = w/2
        self.y = ballOffset
        self.v = 0
        self.vx = 0
        self.a = acc


class origImages:
    pass


class Powerup:
    """ duration: Time for which this powerup will be active
        chance: chance that this will be found on a disc. Out of hundred (%age)"""
    global powerups

    def __init__(self, icon, duration, chance, block):
        self.active = False
        self.icon = icon
        self.blockImage = block #an image reference
        self.duration = duration
        self.chance = chance
        self.range = list(range(chance))

        powerups.append(self)

        self.threadlist = []

    def start(self):
        self.threadlist.append(Thread(target=self.timeout, args=()))
        self.threadlist[-1].start()
        print("EVENT: POWERUP_BEGUN")

    def timeout(self):
        self.active = True
        sleep(self.duration)
        self.active = False


class Powerups:
    pass


class rarities:
    slowmotion = 10
    invincible = 10


class durations:
    slowmotion = 6
    invincible = 3

#functions:
def selectDifficultyScreen():
    global disp
    global w, h
    global bgColor
    global clock

    start = h // 10
    butsize = (w//3, h//3)
    gap = butsize[1]
    disp.fill(bgColor)

    easy1 = pg.transform.scale(images.easy1, butsize)
    easy2 = pg.transform.scale(images.easy2, butsize)
    medium1 = pg.transform.scale(images.medium1, butsize)
    medium2 = pg.transform.scale(images.medium2, butsize)
    veteran1 = pg.transform.scale(images.veteran1, butsize)
    veteran2 = pg.transform.scale(images.veteran2, butsize)

    run = True

    curr = [easy1, medium1, veteran1]
    normal = [easy1, medium1, veteran1]
    hover = [easy2, medium2, veteran2]

    rects = []

    j = 0
    for but in curr:
        rect = but.get_rect()
        rect.center = (w//2, start + gap * j)
        rects.append(rect)
        j += 1

    hov = 0
    while run:
        disp.fill(bgColor)
        curr[hov] = hover[hov]
        for i in range(3):
            disp.blit(curr[i], rects[i])

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    setDifficulty(hov)
                    run = False
                    break
                elif pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
                    hov = (hov + 1) % 3
                    continue
                elif pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
                    hov = (hov - 1) % 3
                    continue

        clock.tick(FPS)
        curr = copy.copy(normal)
        pygame.display.update()


def setDifficulty(n):
    """Set's the difficulty of the game according to n, which is 0, 1 ,2"""
    global NORMAL_PERIOD
    global SLOWMOTION_PERIOD
    global hole_sizes
    global mode
    global mode_name
    global friction
    global drag
    global level_len

    if n:
        if n == 1:
            mode = 1
            mode_name = "MEDIUM"
            NORMAL_PERIOD -= 15
            SLOWMOTION_PERIOD -= 20
            durations.slowmotion -= 2
            durations.invincible -= 2
            level_len = 30

        else:
            mode = 2
            mode_name = "VETERAN"
            NORMAL_PERIOD -= 25
            SLOWMOTION_PERIOD -= 40
            rarities.slowmotion, rarities.invincible = 0, 0
            durations.slowmotion -= 3
            durations.invincible -= 3

            level_len = 40
            drag = 2
            friction = 1.3
    else:
        mode = 0
        mode_name = "EASY"


def genscorestring():
    global score
    global score_string
    global added
    global highscores
    global highscore_mode
    global mode_name
    global mode
    score_string = "Score: {}  ".format(score)
    if added != None:
        score_string += " +{}".format(added)

    score_string += "   AllTime: {}   Current Mode: {}".format(highscores[mode], mode_name)


def waviness():
    global trail_l, trail_r

    for i in range(trail_size):
        lx = trail_l[i][0]
        rx = trail_r[i][0]

        lx += randint(0, 10)
        rx += randint(0, 10)


def setFPS():
    """Function to set FPS according to resolution. Currently not being used, and is trash."""
    global FPS
    global w, h
    global NORMAL_PERIOD
    global SLOWMOTION_PERIOD

    samples = w * h

    res = [640 * 360, 720 * 405, 1280 * 720, 1366 * 768, 1920 * 1080, 2560 * 1440, 3840 * 2160, 7680 * 4320]
    avg = []

    for i in range(len(res) - 1):
        val = (res[i] + res[i+1]) / 2
        avg.append(val)

    index = 0
    while samples < avg[index]:
        index += 1

    fps = [75 ,75 ,75 ,75 ,75 ,75 ,75 ,75]

    FPS = fps[index]

    NORMAL_PERIOD = FPS - 40
    SLOWMOTION_PERIOD = NORMAL_PERIOD + 40


def initpowerups():
    Powerups.invincible = Powerup("&",durations.invincible,rarities.invincible,images.invincible)
    Powerups.slowmotion = Powerup("$",durations.slowmotion,rarities.slowmotion,images.slowmotion)

    global icons
    for powerup in powerups:
        icons.append(powerup.icon)


def loadImages():
    global block_size
    global ball_size
    global disp
    global trail_thickness

    blockImage = pygame.image.load("resources/block.png").convert_alpha()
    blockImage = pygame.transform.scale(blockImage, block_size)
    images.block = blockImage

    ballImage = pygame.image.load("resources/ball.png").convert_alpha()
    ballImage = pygame.transform.scale(ballImage,ball_size)
    images.ball = ballImage
    origImages.ball = ballImage

    obsImage=pygame.image.load("resources/obs.png").convert_alpha()
    obsImage=pygame.transform.scale(obsImage,block_size)
    images.obs=obsImage

    #They use the same variable to load because your boi samarth is lazy.
    blockImage=pygame.image.load("resources/invincible.png").convert_alpha()
    blockImage=pygame.transform.scale(blockImage,block_size)
    images.invincible=blockImage

    blockImage=pygame.image.load("resources/slowmotion.png").convert_alpha()
    blockImage=pygame.transform.scale(blockImage,block_size)
    images.slowmotion=blockImage

    blockImage=pygame.image.load("resources/trail.png")
    blockImage=pygame.Surface.convert_alpha(blockImage)
    blockImage=pygame.transform.scale(blockImage,(200,200))
    images.trail=blockImage

    #buttons

    #easy
    but1 = pygame.image.load("resources/buttons/goeasy1.png")
    but2 = pygame.image.load("resources/buttons/goeasy2.png")
    but1 = blockImage=pygame.Surface.convert_alpha(but1)
    but2 = blockImage=pygame.Surface.convert_alpha(but2)
    images.easy1, images.easy2 = but1, but2

    #medium
    but1=pygame.image.load("resources/buttons/medium1.png")
    but2=pygame.image.load("resources/buttons/medium2.png")
    but1=blockImage=pygame.Surface.convert_alpha(but1)
    but2=blockImage=pygame.Surface.convert_alpha(but2)
    images.medium1,images.medium2=but1,but2

    #veteran
    but1=pygame.image.load("resources/buttons/veteran1.png")
    but2=pygame.image.load("resources/buttons/veteran2.png")
    but1=blockImage=pygame.Surface.convert_alpha(but1)
    but2=blockImage=pygame.Surface.convert_alpha(but2)
    images.veteran1,images.veteran2=but1,but2


def removeAdded(delay):
    "Removes the 'added' portion of the score string after sometime"
    global disp_added
    global added

    while 1:
        if not added is None:
            sleep(delay)
            disp_added = None
        sleep(1)

addedRemoverThread = Thread(target=removeAdded, args=(2,))
addedRemoverThread.start()

def stringify(array):
    string = ""
    for i in range(len(array) - 1):
        string += str(array[i]) + "\n"

    string += str(array[-1])

    return string


def saveGame():
    global score
    global highscore
    global GAME_TITLE
    global filename
    global mode_name
    global mode
    global highscore_mode
    global file_invalid_or_not_created
    global highscores

    highscores[mode] = score if score > highscores[mode] else highscores[mode]

    file = open(filename,"w")

    file.write(stringify(highscores))

    file.close()


def cap(x, u, l):
    if x < l:
        return l
    elif x > u:
        return u
    else:
        return x


def addObstacles():
    global l
    global obs_sizes
    global size
    global obs
    global ball
    global surface
    global w, h
    for each in discs:
        n=choice([1,2])
        for i in range(n):
            obsize = choice(obs_sizes)
            start = randrange(0, size)
            r = list(range(start, start + obsize))
            for j in range(len(each)):
                if j in r and each[j] != " ":
                    each[j] = "@"
                elif each[j] == " ":
                    r.append(r[-1] % len(r))

    disc = discs[0]
    indices = [(int(w/2)) % size,(int(w/2)) % size + 1, (int(w/2)) % size - 1]
    for index in indices:
        disc[index] = surface


def addPowerups():
    global l
    global power
    global powerup_sizes
    global size

    for powerup in powerups:
        for disc in discs:
            if randint(0, 100) in powerup.range:
                psize = choice(powerup_sizes)

                start = randint(0,size - psize - 1)
                end = start + psize

                indices = list(range(start, end))
                for index in indices:
                    if disc[index] == "#":
                        disc[index] = powerup.icon


def makeLevel():
    global l
    global hole_sizes
    global gap
    global level_len
    global disc_positions
    global ballOffset

    pos = gap + ballOffset
    #Make discs
    for i in range(level_len):
        row=[]

        holeSize=choice(hole_sizes)

        start=randint(0,size - holeSize)

        for i in range(size):
            if not (i in range(start,start + holeSize)):
                row.append(surface)
            else:
                row.append(" ")

        discs.append(row)
        disc_positions.append(pos)
        pos += gap

    addObstacles()

    addPowerups()


def updateBall():
    global ball
    global disp
    global max_vel
    global currentDisc
    global ball_size
    global rotationSpeed
    global currentAngle
    global UPDATE_PERIOD
    global SLOWMOTION_PERIOD
    global NORMAL_PERIOD
    global trail_l, trail_r

    x = ball.x
    y = ball.y

    l = (x - ball_size[0]/2, y)
    r = (x + ball_size[0]/2, y)

    trail_l.pop(0)
    trail_r.pop(0)

    trail_l.append(l)
    trail_r.append(r)

    waviness()

    if Powerups.slowmotion.active:
        UPDATE_PERIOD = SLOWMOTION_PERIOD
    else:
        UPDATE_PERIOD = NORMAL_PERIOD

    delta =1 / UPDATE_PERIOD

    currentAngle += rotationSpeed * delta

    new = pygame.transform.rotate(origImages.ball, currentAngle)
    images.ball = new

    offset = 0
    if collision():
        ball.v -= 2 * ball.v

    minus = max_vel * -1

    if ball.v > max_vel:
        ball.v = max_vel

    if ball.v < minus:
        ball.v = minus

    ball.y += ball.v * delta + offset
    ball.v += ball.a * delta

    ball.x += ball.vx * delta
    disp.blit(images.ball, (ball.x, ball.y))


def weight(x):
    return abs(x // 6)


def pre_init():
    "init before difficulty selection"
    loadImages()
    pygame.mouse.set_visible(False)


def initialize():
    "init after difficulty selection"
    #setFPS()
    initpowerups()
    makeLevel()


def scroll(move):
    """this function scrolls the whole thing one unit to the right or to the left
    move is a boolean value, true means to the right"""
    global size
    global l
    global movement

    if move:
        #move to right
        for i in range(len(discs)):
            row = discs[i]
            prev = row[-1]
            for i in range(len(row)):
                prev,row[i] = row[i], prev

    else:
        #move to left
        for i in range(len(discs)):
            row = list(reversed(discs[i]))
            prev = row[-1]
            for j in range(len(row)):
                prev, row[j] = row[j], prev
            discs[i] = list(reversed(row))


def renderDiscs():
    global l
    global disc_positions
    global block_size
    global disp
    global currentDisc
    global view
    global obs
    global icons

    block_image = images.block
    obs_image = images.obs
    count = 0


    for powerup in powerups:
        icons.append(powerup.icon)

    for disc in discs:
        x = 0
        for block in disc:
            if block == "#":
                disp.blit(block_image, (x,disc_positions[count] + view))
            elif block == "@":
                disp.blit(obs_image, (x,disc_positions[count] + view))
            elif block != " ":
                disp.blit(powerups[icons.index(block)].blockImage,(x,disc_positions[count] + view))

            x += block_size[0]
        count += 1


def generateText(s, font, size):
    global orange
    global orange2

    "Generates text of the string passed as parameter"
    im = pygame.font.Font(font, size).render(s, True, orange2)
    return im


def renderTrail():
    global trail_l, trail_r
    global trail_len
    global disp
    global trail_color
    global view
    global ball_size

    delta = 0
    offset_ = 10
    for i in range(trail_len - 1):
        start, end = (trail_l[i][0], trail_l[i][1] + view),(trail_l[i + 1][0] + delta * (i - trail_len/2), trail_l[i + 1][1] + view)
        pg.draw.aaline(disp,trail_color, start, end)

        start, end = (trail_r[i][0], trail_r[i][1] + view),(trail_r[i + 1][0] + delta * (i - trail_len/2), trail_r[i + 1][1] + view)
        pg.draw.aaline(disp,trail_color,start,end)

        start, end = (trail_r[i][0] - (ball_size[0]/2),trail_r[i][1] + view + offset_ - (ball_size[0]/2)),(trail_r[i + 1][0] + delta * (i - trail_len / 2) - (ball_size[0]/2),trail_r[i + 1][1] + offset_+ view - (ball_size[0]/2))
        pg.draw.aaline(disp,trail_color,start,end)

def isSlowmotion():
    return Powerups.slowmotion.active


def render():
    global disp
    global ball
    global view
    global bgColor
    global view
    global h
    global score_string
    global invincibleColor
    global powerups
    if ball.y + view > h - h/2:
        addMoverThread()
        viewMoverThreads[-1].start()
        print("EVENT: VIEW_STABILIZER INSTANTIATED")

    if isInvincible():
        disp.fill(invincibleColor)
    elif isSlowmotion():
        disp.fill(slowmotionColor)
    else:
        disp.fill(bgColor)  #Clear screen

    rect = images.ball.get_rect()
    rect.center = (ball.x, int(ball.y) + view)
    disp.blit(images.ball, rect)

    renderDiscs()

    genscorestring()

    text = generateText(score_string,fonts.score, 50)

    for powerup in powerups:
        if powerup.active:
            renderTrail()
            break

    disp.blit(text, (0, 0))


def isInvincible():
    return Powerups.invincible.active


def addToScore():
    global bounces, added, scorePerBounce, multiplier, disp_added, score
    global max_multiplier
    """Add to the score, if the player is invincible or also when he is crossing a disc"""
    if not bounces and multiplier < max_multiplier:
        multiplier+=1

    bounces=0
    added = scorePerBounce * multiplier
    disp_added = added
    score += added


def collision():
    global disc_positions
    global currentDisc
    global ball
    global block_size
    global l
    global viewMover
    global move_view_speed
    global viewMoverThreads
    global won
    global popperThreads
    global running
    global multiplier
    global bounces
    global score
    global added
    global scorePerBounce
    global disp_added
    global rotationSpeed
    global icons

    block = block_size[0]
    prev = currentDisc
    offset = 10

    count = 0
    for each in disc_positions:
        if each - offset <= ball.y:
            count += 1
        else:
            break

    if count >= len(discs):
        won = True


    currentDisc = count
    if count > prev: #hit a disc level
        curr = discs[count - 1][int(ball.x / block) + 1]
        if  curr == " ":
            #Crossing a disc
            if not bounces:
                multiplier += 1

            bounces = 0
            added = scorePerBounce * multiplier
            disp_added = added
            score += added

            print(f"EVENT: DISC_{currentDisc - 1}_CROSSED")

            addMoverThread()
            viewMoverThreads[-1].start()

            return False
        elif curr == "@":
            #Hit an obstacle
            print("EVENT: HIT OBSTACLE")
            if not isInvincible():
                running = False

            if isInvincible():
                addToScore()

            return not isInvincible()

        elif curr in icons:
            index = icons.index(curr)
            powerups[index].start()

            if isInvincible():
                addToScore()

            return not isInvincible()
        else:
            #Bounced off a disc

            #move a little because of ball's spin
            ball.vx = rotationSpeed * -1 * friction / 20

            rotationSpeed /= friction


            if not isInvincible():
                bounces+=1
                multiplier = 1
            added = None

            if isInvincible():
                addToScore()

            return not isInvincible()
    else:
        #Just in air
        return False


def moveView(speed):
    global gap
    global view

    orig = view
    target = orig - gap

    while view > target:
        view -= 1
        sleep(1/speed)

    sys.exit()


def popper():
    pass


def addMoverThread():
    newThread = Thread(target=moveView, args=(move_view_speed, ))
    viewMoverThreads.append(newThread)
    print("NEW_THREAD_ADDED")


def addPopperThread():
    global popperThreads
    popperThreads.append(Thread(target=popper, args=()))


def renderText(txt):
    global w, h
    image=generateText(txt,fonts.winorlose,90)
    rect=image.get_rect()
    rect.center=(w / 2,h / 2)
    disp.blit(image,rect)
    pygame.display.update()


try:
    system("cls")

    pre_init()

    selectDifficultyScreen()

    initialize()
except:
    pygame.quit()
    print("""Something went wrong. Make sure that this app is running from its home directory. (As received), i.e. Don't move this application to another location.""")
    input()

ball = Ball()

system("cls")
print("This info is meant for debugging, as the game is still in BETA. Please ignore this info.\n")

try:
    while running and not won:
        updateBall()
        render()

        for event in pygame.event.get():
            if event == pygame.QUIT:
                running = False
            if event.type == pg.MOUSEMOTION:
                relx, rely = event.rel
                relx = cap(relx, 40, -40)

                rotationSpeed += relx * drag

                ball.x -= relx // 12
                if relx != 0:
                    wei = int(weight(relx) * 1.8)
                    relx += abs(relx)

                    for i in range(wei + 2):
                        scroll(relx)
                if rely != 0:
                    if ball.v > 0:
                        pass

        pygame.display.update()
        clock.tick(FPS)
    if won:
        renderText(choice(won_message))
        saveGame()
    else:
        renderText(choice(lost_message))

    sleep(3)
    pygame.quit()

    sys.exit()
except:
    #print("Something bad happened. If the problem persists, please try re-downloading the game and trying again.")
    sys.exit()