import pygame
import os

from classes import Bird, Pipe, Ground


HEIGHT = 800
WIDTH = 500


PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "pipe.png")))

GROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "ground.png")))

BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "background.png")))

SCORE = 0


def draw_window(window, font, bird, pipes, ground):
    global SCORE
    
    window.blit(BACKGROUND_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(window)
        
    ground.draw(window)
        
    bird.draw(window)
    
    score_label = font.render("Score: " + str(SCORE), 1, (255, 255, 255))
    window.blit(score_label, (WIDTH - score_label.get_width() - 15, 10))
    
    pygame.display.update()
    

def game_over(window, font):
     
    run = True
    
    while run:
        label = font.render("GAME OVER", 1, (255, 255, 255))
        window.blit(label, (round((WIDTH - label.get_width()) / 2), round((HEIGHT - label.get_height()) / 2)))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

 
def animate(bird, pipes, ground):
    global SCORE 
    
    bird.move()
    ground.move()
    
    add_pipe = False
    
    for pipe in list(pipes):
        
        if(pipe.collide(bird) or bird.y > 660):
            return False
        
        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
            pipes.remove(pipe)
            
        if not pipe.passed and pipe.x < bird.x:
            pipe.passed = True
            add_pipe = True
            
        if(add_pipe):
            SCORE += 1
            pipes.append(Pipe(630))
        pipe.move()
    return True
        
    
def main():
    global WIDTH, HEIGHT
    run = True
    
    bird = Bird(230, 350)
    ground = Ground(730)
    pipes = [Pipe(700)]
    
    pygame.font.init()
    font = pygame.font.Font('freesansbold.ttf', 40)
    
    pygame.init()  
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                bird.jump()
        
        run = animate(bird, pipes, ground)
        draw_window(window, font, bird, pipes, ground)
    
    game_over(window, font)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
