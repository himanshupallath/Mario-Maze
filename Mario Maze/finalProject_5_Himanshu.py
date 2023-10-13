########################################################################################################################
# Author: Himanshu Pallath                                                                                             #
# Purpose: This is the game that I designed my self called "Mario Run Course". The objective of the game is simple.4   #
#          All you need to do is get to to the end of the course or the finish line but there is a twist.              #
#          There are 2 different finish lines. One of the finish lines the correct and winning finish line.            #
#          The other finish line the losing finish line. There is a place in the course where it splits into 2         #
#          direction. You need to guess the correct path and go through it. Once you hit the checkered flag,           #
#          it will exit the board and display "You Won" or "You Lose" depending on which path you take. Good Luck!     #
# Class Description:                                                                                                   #
#          There are 5 classes in total. One classes is for the player and the players movements. Another 2 are for    #
#          both the finish lines. One class is for the Platform of the game and the last platform is used to control   #
#          the scrolling of the board depending on the player's position.                                              #
########################################################################################################################
import pygame, math
from math import ceil
from pygame import *
import sys

LIGHTGRAY = (225, 225, 225)
DARKGRAY = (160, 160, 160)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (153, 51, 255)
PINK = (255, 0, 255)
LIGHTBLUE = (0, 255, 255)
CYAN = (102, 255, 255)
DARKPURPLE = (153, 0, 76)
WIN_WIDTH = 300
WIN_HEIGHT = 250
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
BLOCK_WIDTH = 20
BLOCK_HEIGHT = 20
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
JUMP_VEL = 10
MOVE_VEL = 10
GRAVITY = 1
TERMINAL_VELOCITY = 10
PLATFORM_COLOR = {"P": BLACK, "Q": BLUE, "G": GREEN, "A": LIGHTGRAY, "Y": YELLOW, "O": ORANGE, "L": PURPLE,
                  "I": LIGHTBLUE, "B": WHITE, "W": PINK, "R": RED, "C": DARKPURPLE, "Z": LIGHTGRAY}
BACKGROUND_IMAGE = 'marioBackground.png'

pygame.display.set_caption('Mario Run Course')


def main():
    global cameraX, cameraY, WIN_HEIGHT, WIN_WIDTH
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), FLAGS, DEPTH)
    timer = pygame.time.Clock()

    up = False
    down = False
    left = False
    right = False

    sprites = pygame.sprite.Group()
    platforms = []

    x = 0
    y = 0
    # The drawing of the level. P means "platform", M stands for "me" (or "PLAYER")
    #  You can add different things here
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PIII  YYYY       WWWBCCCCCCCCC                      P",
        "PII  YYYY   GGGG  WWBC       C                      P",
        "PI  YYYY   GGGGGG   BC CCCC  CLL   LLLL    IIIII    P",
        "P    YYYY GGGGGGGG  B  C    CCL   LLLLL    I   I IIIP",
        "P GG  YYY   GGGG    B CCCC   C  LLLLLL    I   I     P",
        "PGGGG  YYY  GGGGGGG B  C   CCC   LLLL    I   II     P",
        "PGGGGG Y   GGGGG    BC C     CL  L       IIIIIIIIII P",
        "PGGG      GGGGGG IIIB  Y YYYYY   L       I  I  I  I P",
        "PGG  WWWWWWYYYYY   IB CY     Y  LL GGGGGG   I     I P",
        "PG  WWWWWW YYYYYY  IB  Y Z Z Y        G           I P",
        "P  WWWWWW   YYYYY IIBC Y  Z  YL       G  G     G  I P",
        "PY  WWWW  I   YYY  IB  Y     Y   YYY  G  G  G  G    P",
        "PYY  WW  III  YYYY    CY ZZZ Y  YYRY GG  GGGGGGGGGGGP",
        "PYYY    IIIII  YYYY    Y         YRY  G  GGG        P",
        "PYYYY  IIIIIII  YYYY CCYYYYYYYYYYYRYY G  GG     G   P",
        "PBBBBBBBBBBBBBB  BBBBB            Y   G  G    G G   P",
        "PLLL     LLLLL L  LLBRRR       O     GG     G G G   P",
        "PLL   LL  LLL   L  LBRRRR    OOOOOOOOOOOOOOOOOOOO   P",
        "PL   LLLL  L  L  L  BRRR    R       O           O   P",
        "P   LLLLLL   LLL  L BRR    RO L    OO    W      O   P",
        "P  LLLLLLLLLLLLLL   BR    RO  L   OOO   WQW     O   P",
        "P LL     L      LLLLB    RO  LL  OOOO   WQW     O   P",
        "P  L  O     O       B   RO  LLL  OOO  WWWQWWW   O   P",
        "PL L  OOOOOOOOO     B  RRO  LLLL  O  WWQQQQQWW  O   P",
        "P  L  O       OO    B   RO  LLL     WWQQQQQQQWW     P",
        "P LL  O  OOO   O   OBR  RO  LLLLLLLLLLLLLLLLLLLLLLLLP",
        "P     O    O OOO    B   RO           KYYYYYYYYYYYYYYP",
        "POOOOOOOO  O   OOO  B  CCCCCCCCCCCCCCCYYYPPYYYYPPYYYP",
        "PMO   O    OOO OO   B    C       C   YYYYYYYPPYYYYYYP",
        "P O O O O OO   O  OOBR   C C   C C   YYYPPYYYYYYPPYYP",
        "P   O   O  O     OOOB      C   C     DYYYYPPPPPPYYYYP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"]
    # build the level
    marioIMG = pygame.image.load('marioPixel.png').convert_alpha()
    checkerIMG = pygame.image.load('checkeredFlag.png').convert_alpha()
    playerFlag = True
    finishFlag = True
    falseFlag = True
    for row in level:
        x = 0
        for col in row:
            if col == "P":
                p = Platform(x, y, PLATFORM_COLOR[col])
                platforms.append(p)
                sprites.add(p)
            elif col == "M":
                if playerFlag:
                    # Give the player an initial position (x and y) then width and height
                    player = Player(marioIMG, x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
                    sprites.add(player)
                    # Do not allow another player to be added
                    playerFlag = False
            elif col == "K":
                if finishFlag:
                    finish = Finish(checkerIMG, x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
                    sprites.add(finish)
                    finishFlag = False
            elif col == "D":
                if falseFlag:
                    falseEnding = FalseFinish(checkerIMG, x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
                    sprites.add(falseEnding)
                    falseFlag = False
            elif col != " ":
                tempPlatform = Platform(x, y, PLATFORM_COLOR[col])
                platforms.append(tempPlatform)  # Add platforms to a list
                sprites.add(tempPlatform)
            x += BLOCK_WIDTH
        y += BLOCK_HEIGHT

    if playerFlag:
        print("You didn't include a player!")
        pygame.quit()
    total_level_width = len(level[0]) * BLOCK_WIDTH
    total_level_height = len(level) * BLOCK_HEIGHT

    print("")
    print("Welcome to my Game: Mario Run Course")
    print("Objective: ")
    print("   You need to reach the finish line but there is a twist.")
    print("   There are two finish lines and you don't know which finish line you need to go to")
    print("   If you get the right finish line, YOU WIN!!!")
    print("   If you get the wrong finish line, YOU LOSE!!!")
    print("   Choose you path carefully and think twice before you move on.")
    print("Good Luck!")

    while 1:
        timer.tick(20)
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
        bgIMG = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
        repeatedImageWidth = int(WIN_WIDTH)
        myImage = pygame.transform.scale(bgIMG, (repeatedImageWidth, WIN_HEIGHT))

        # draw background. This is a repeated background
        for x in range(0, int(total_level_width / repeatedImageWidth) + 1):
            screen.blit(myImage, (x * repeatedImageWidth, 0))

        camera = Camera(total_level_width, total_level_height)

        camera.update(player)
        if pygame.sprite.collide_rect(player, falseEnding):
            You = '\033[2m'
            Won = '\033[2m'
            print("|-----------|")
            print("|  ", You, "You ", Won, "Won", "  |", sep="")
            print("|-----------|")
            break
        if pygame.sprite.collide_rect(player, finish):
            You = '\033[2m'
            Lose = '\033[2m'
            print("|------------|")
            print("|  ", You, "You ", Lose, "Lose", "  |", sep="")
            print("|------------|")
            break
        # update player, draw everything else
        player.update(up, down, left, right, platforms)
        for e in sprites:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()


# The Camera class takes care of the scrolling.
#   It allows us to have a small window and make the player scroll through the level
class Camera(object):
    def __init__(self, width, height):
        self.state = Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.shift_camera(target.rect)

    def shift_camera(self, target_rect):
        # Extract the position of the rectangle bring passed in
        (left, top, sizeX, sizeY) = target_rect

        # Adjust the left to be half of the screen minus the current left
        left = HALF_WIDTH - left
        # Adjust top similarly
        top = HALF_HEIGHT - top

        # Now, take care of issues with hitting an edge.
        left = min(0, left)  # stop scrolling at the left edge
        left = max(-(self.width - WIN_WIDTH), left)  # stop scrolling at the right edge
        top = max(-(self.height - WIN_HEIGHT), top)  # stop scrolling at the bottom
        top = min(0, top)  # stop scrolling at the top
        return Rect(left, top, self.width, self.height)


# This is the Class for the Player and it creates the Sprite for the player
class Player(pygame.sprite.Sprite):
    def __init__(self, imgFile, x, y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.hitTop = False
        self.image = pygame.transform.scale(imgFile, (width, height))
        # Set the rectangle's position that surrounds the image equal to what we passed in
        self.rect = self.image.get_rect(center=(x, y))
        self.rect = Rect(x, y, self.width, self.height)

    def update(self, up, down, left, right, platforms):
        # Start with no change in x-position... see what happened
        self.xvel = 0
        if up:
            # only jump if on the ground
            if self.onGround:
                self.yvel -= JUMP_VEL
        if down:
            pass
        if left:
            self.xvel = -MOVE_VEL
        if right:
            self.xvel = MOVE_VEL
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += GRAVITY
            # Make gravity work a little harder if they
            #  just hit the bottom of a platform (giving a little
            #  bit of a bounce effect)
            if self.hitTop == True:
                self.yvel += GRAVITY * 6
                self.hitTop = False
            # max falling speed
            if self.yvel > TERMINAL_VELOCITY:
                self.yvel = TERMINAL_VELOCITY

        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += int(self.yvel)
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                    # print ("collide right")
                if xvel < 0:
                    self.rect.left = p.rect.right
                    # print ("collide left")
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                    # print("collide bottom")
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.hitTop = True
                    # print("collide top")


# This is the sprite for the correct and winning finish line.
class Finish(pygame.sprite.Sprite):
    def __init__(self, imgFile, x, y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.hitTop = False
        self.image = pygame.transform.scale(imgFile, (width, height))
        # Set the rectangle's position that surrounds the image equal to what we passed in
        self.rect = self.image.get_rect(center=(x, y))
        self.rect = Rect(x, y, self.width, self.height)


# This is the class for the wrong finish and losing finish line
class FalseFinish(pygame.sprite.Sprite):
    def __init__(self, imgFile, x, y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.hitTop = False
        self.image = pygame.transform.scale(imgFile, (width, height))
        # Set the rectangle's position that surrounds the image equal to what we passed in
        self.rect = self.image.get_rect(center=(x, y))
        self.rect = Rect(x, y, self.width, self.height)


# This class creates the platform for the boarders and the surface
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.convert()
        self.image.fill(color)
        self.rect = Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

    def update(self):
        pass


if __name__ == "__main__":
    main()
    pygame.quit()
