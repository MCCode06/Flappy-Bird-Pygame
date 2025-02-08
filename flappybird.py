import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(350, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(350, random_pipe_pos - 170))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 480:
        return False
    return True


def rotate_bird(bird):
    rotated_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return rotated_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f"High score: {int(high_score)}", True, (255, 255, 255)
        )
        high_score_rect = high_score_surface.get_rect(center=(144, 425))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.TTF", 20)

floor_x_pos = 0
gravity = 0.125
bird_movement = 0
score = 0
high_score = 0


bg_surface = pygame.image.load("background-day.png").convert()
floor_surface = pygame.image.load("base.png").convert()
bird_downflap = pygame.image.load("yellowbird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("yellowbird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("yellowbird-upflap.png").convert_alpha()
game_over_surface = pygame.image.load("gameover.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144, 256))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 256))
BİRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BİRDFLAP, 200)

pipe_surface = pygame.image.load("pipe-green.png")
pipe_list = []
pipe_height = [200, 300, 400]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
game_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 256)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BİRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    floor_x_pos -= 1
    draw_floor()

    if floor_x_pos <= -288:
        floor_x_pos = 0

    if game_active:
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        score += 0.008
        score_display("main_game")
    else:
        score_display("game_over")
        high_score = update_score(score, high_score)
        screen.blit(game_over_surface, game_over_rect)

    pygame.display.update()
    clock.tick(120)


if __name__ == "__main__":
    main()
