import pygame
import os
import joblib
from time import time

import neat
from classes import Bird, Pipe, Ground


HEIGHT = 800
WIDTH = 500

START_TIME = 0
END_TIME = 2 * 60

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "pipe.png")))

GROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "ground.png")))

BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("graphics", "background.png")))

SCORE = 0

nets = []
ge = []
birds = []
    

def draw_window(window, font, birds, pipes, ground):
    global SCORE
    
    window.blit(BACKGROUND_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(window)
        
    ground.draw(window)
        
    for bird in birds:
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

 
def animate(pipes, ground):
    global SCORE, nets, ge, birds
      
    ground.move()

    add_pipe = False
    
    for pipe in list(pipes):
        for x, bird in enumerate(birds):
            bird.move()
            
            if(pipe.collide(bird) or bird.y > 660 or bird.y < 0):
                ge[x].fitness -= 1
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
            
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            
        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
            pipes.remove(pipe)

        if(add_pipe):
            SCORE += 1
            pipes.append(Pipe(630))
            
            for g in ge:
                g.fitness += 5
                           
        pipe.move()
        
    
def evaluate(genomes, config):
    global WIDTH, HEIGHT, nets, ge, birds
    run = True
    
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 200))
        g.fitness = 0
        ge.append(g)
       
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
                pygame.quit()
                quit()
                break
      
        # info to look on the 1st or 2nd pipe on the screen
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  
                pipe_ind = 1
        else:
            run = False
            break
          
        for x, bird in enumerate(birds): 
            ge[x].fitness += 0.1
            bird.move()
            
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5: 
                bird.jump()
        
        animate(pipes, ground)
        draw_window(window, font, birds, pipes, ground)
        
        if(time() - START_TIME > END_TIME):
            print("Time run out")
            break
    

def run(config_file):
    global START_TIME
    
    START_TIME = time()
    
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(evaluate, 50)
    
    joblib.dump(winner, "Specimen100")
    print('\nBest genome:\n{!s}'.format(winner))
    print("Training time:", time() - START_TIME)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config")
    run(config_path)
