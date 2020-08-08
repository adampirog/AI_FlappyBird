import pygame
import os
import sys
import neat
import joblib
from datetime import datetime
from classes import Bird, Pipe, Ground


HEIGHT = 800
WIDTH = 500


PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "pipe.png")))

GROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "ground.png")))

BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "background.png")))

SCORE = 0

ENGINE = False


def save_score(filename):
    if(SCORE > 0):
        with open(filename, 'a') as file:
            file.write("\n" + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ",   SCORE: " + str(SCORE))
            if(ENGINE):
                file.write(",    ENGINE")
            else:
                file.write(",    HUMAN")
                

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
    global ENGINE
    
    config_name = "config"
    if (len(sys.argv) == 2):
        ENGINE = True
    if (len(sys.argv) == 3):
        ENGINE = True  
        config_name = sys.argv[2] 
    elif(len(sys.argv) > 3):
        quit()
       
    global WIDTH, HEIGHT
    run = True
    net = None
    
    if(ENGINE):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, config_name)
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_path)
        
        genome = joblib.load(sys.argv[1])  
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        
    bird = Bird(230, 200)
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
                save_score("scoreboard")
                run = False
                pygame.quit()
                quit()
                break
            if event.type == pygame.KEYDOWN:
                if not ENGINE:
                    bird.jump()
        
        pipe_ind = 0
        if(ENGINE):
            if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  
                pipe_ind = 1
            output = net.activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5: 
                bird.jump()
            
        run = animate(bird, pipes, ground)
        draw_window(window, font, bird, pipes, ground)
    
    save_score("scoreboard")
    game_over(window, font)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
