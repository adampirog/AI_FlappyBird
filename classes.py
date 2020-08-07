import pygame
import random
import os

HEIGHT = 800
WIDTH = 600

BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "bird1.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "bird2.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "bird3.png")))]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "pipe.png")))

GROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "ground.png")))

BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "background.png")))


class Bird:
    IMG = BIRD_IMG
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        
        self.img_count = 0
        self.img = self.IMG[0]
        
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
        
    def move(self):
        self.tick_count += 1
        
        disp = self.vel * self.tick_count + 1.5 * self.tick_count**2
        
        if(disp >= 16):
            disp = 16
            
        elif(disp < 0):
            disp -= 2    
        
        self.y += disp
        
        if disp < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, window):
        self.img_count += 1
        
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMG[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMG[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMG[2]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMG[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMG[1]
            self.img_count = self.ANIMATION_TIME * 2
            
        blitRotateCenter(window, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def blitRotateCenter(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect.topleft)


class Pipe:
    GAP = 200
    VEL = 5
    
    def __init__(self, x):
        self.x = x
        self.height = 0
        
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        
        self.passed = False
        self.set_height()
        
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
        
    def move(self):
        self.x -= self.VEL
        
    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        # points of collision
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        
        if(t_point or b_point):
            return True
        
        return False
        
        
class Ground:
    VEL = 5
    WIDTH = GROUND_IMG.get_width()
    IMG = GROUND_IMG
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
