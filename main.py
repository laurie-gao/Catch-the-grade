import pygame
import random
import os
pygame.init()

screen_width = 570
screen_height = 640

win = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("First Game :D")

bg = pygame.transform.scale(pygame.image.load(os.path.join('pics', 'background.png')), (screen_width, screen_height))
walkRight = pygame.transform.scale(pygame.image.load(os.path.join('pics', 'me_right.png')), (46, 100))
walkLeft = pygame.transform.scale(pygame.image.load(os.path.join('pics', 'me_left.png')), (46, 100))
standing = pygame.transform.scale(pygame.image.load(os.path.join('pics', 'me.png')), (46, 100))
walkingRight = [walkRight, walkLeft, standing]
walkingLeft = [walkLeft, walkRight, standing]

yaysound = pygame.mixer.Sound(os.path.join('pics', 'Check.wav'))
ohnosound = pygame.mixer.Sound(os.path.join('pics', 'OhNo.wav'))

music = pygame.mixer.music.load(os.path.join('pics', 'backgroundmusic.mp3'))
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

class Me(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.left = False
        self.right = False
        self.walkCount = 0

    def draw(self, win):
        if self.walkCount >= 6:
            self.walkCount = 0
        if self.left:
            win.blit(walkingLeft[self.walkCount//2], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkingRight[self.walkCount//2], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(standing, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(standing)


class A(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, end):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('pics', 'Aplus.png')), (48, 34))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.vel = 10

    def draw(self, win):
        win.blit(self.image, (self.x, self.y, 28, 60))

    def collide(self, me):
        me_mask = me.get_mask()
        a_mask = pygame.mask.from_surface(self.image)

        a_offset = (round(self.x) - round(me.x), round(self.y) - round(me.y))

        b_point = me_mask.overlap(a_mask, a_offset)

        if b_point:
            return True

        return False


class F(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, end):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('pics', 'F.png')), (28, 43))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.vel = 15

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def collide(self, me):
        me_mask = me.get_mask()
        f_mask = pygame.mask.from_surface(self.image)

        f_offset = (round(self.x) - round(me.x), round(self.y) - round(me.y))

        b_point = me_mask.overlap(f_mask, f_offset)

        if b_point:
            return True

        return False


def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(win, ac, (x, y, w, h))

        if click[0] == 1:
            if action == "play":
                game_loop()
            elif action == "quit":
                exit()
    else:
        pygame.draw.rect(win, ic, (x, y, w, h))

    smallText = pygame.font.SysFont('comicsans', 30)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    win.blit(textSurf, textRect)

def draw_game_window(score):
    score_font = pygame.font.SysFont('comicsans', 30, True)
    win.blit(bg, (0, 0))
    text = score_font.render('Score: '+ str(score), 1, (255, 255, 255))
    win.blit(text, (450, 10))
    me.draw(win)
    for good in goods:
        good.draw(win)
    for bad in bads:
        bad.draw(win)
    pygame.display.update()


def game_intro():
    main_font = pygame.font.SysFont('comicsans', 40, True)
    intro = True
    while intro:

        win.blit(bg, (0, 0))
        title = main_font.render('Welcome to University', 1, (255, 255, 255))
        win.blit(title, (120, 30))
        button("Start", 150, 100, 100, 50, (0, 200, 0), (0, 255, 0), "play")
        button("Quit", 320, 100, 100, 50, (200, 0, 0), (255, 0, 0), "quit")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False


def game_loop():
    score = 0
    run = True
    pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
    pygame.time.set_timer(pygame.USEREVENT + 2, 2000)

    while run:
        clock.tick(30)

        if pygame.event.get(pygame.USEREVENT + 1):
            goods.append(A(random.randint(20, 550), 0, 48, 34, 480))
            pygame.display.update()

        if pygame.event.get(pygame.USEREVENT + 2):
            bads.append(F(random.randint(20, 550), 0, 28, 43, 480))
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()

        for good in goods:
            if good.y < 480:
                good.y += good.vel
            else:
                goods.pop(goods.index(good))

        for bad in bads:
            if bad.y < 480:
                bad.y += bad.vel
            else:
                bads.pop(bads.index(bad))

        for good in goods:
            if good.collide(me):
                goods.pop(goods.index(good))
                score += 1
                yaysound.play()

        for bad in bads:
            if bad.collide(me):
                ohnosound.play()
                bads.pop(bads.index(bad))
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and me.x > 0:
            me.x -= me.vel
            me.left = True
            me.right = False
        elif keys[pygame.K_RIGHT] and me.x < screen_width - me.width:
            me.x += me.vel
            me.right = True
            me.left = False
        else:
            me.right = False
            me.left = False
            me.walkCount = 0

        draw_game_window(score)

    return score

me = Me(0, 405, 46, 100)
goods = []
bads = []
game_intro()
pygame.quit()



