import pygame
import time
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load("bg2.png")

bird_img_0 = pygame.image.load("bird_0.png")
bird_img_0 = pygame.transform.scale(bird_img_0, (40, 40))

sound = pygame.mixer.Sound("bell.wav")


font = pygame.font.Font(None, 36)
score = 0
screen_width, screen_height = screen.get_size()
# Set up the colors
GRAY = (128, 128, 128)
GREEN = (0, 153, 76)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Set up boolean
running = True
clock = pygame.time.Clock()

# Set up tube
tube_vec = 3
tube_speed = 0.0005
tube_width = 50 
tube_space = 200
tube_gap = 150

tubes = [[750, 0, random.randint(200, 400)], [1000, 0, random.randint(200, 400)], [1250, 0, random.randint(200, 400)], [1500, 0, random.randint(200, 400)]]

tubes_under = [[750, tubes[0][2] + tube_gap, screen_height - tubes[0][2] - tube_gap], 
                [1000, tubes[1][2] + tube_gap, screen_height - tubes[1][2] - tube_gap],
                [1250, tubes[2][2] + tube_gap, screen_height - tubes[2][2] - tube_gap], 
                [1500, tubes[3][2] + tube_gap, screen_height - tubes[3][2] - tube_gap]]

passed_tubes = [False, False, False, False]

# Set up the bird
bird_x = 150
bird_y = 300
bird_W = 30
bird_H = 30
GRAVITY = 0.5
opacity = 0
# Run the game
check_live_bird = True
while running:
    clock.tick(65)
    screen.fill(GRAY)
    screen.blit(background, (0, 0))
    # Draw the bird
    # birtd_rect = pygame.draw.rect(screen, RED, (bird_x, bird_y, bird_W, bird_H))
    birtd_rect = screen.blit(bird_img_0, (bird_x, bird_y))

    bird_y += opacity
    opacity += GRAVITY
    # Check if the bird hit the tubes
    '''
    for tube in tubes:
        if bird_x >= tube[0] and bird_x <= tube[0] + tube_width:
            if bird_y >= 0 and bird_y <= tube[2]:
                running = False
    for tube in tubes_under:
        if bird_x >= tube[0] and bird_x <= tube[0] + tube_width:
            if bird_y >= tube[1] and bird_y <= screen_height:
                running = False
    if bird_y > screen_height or bird_y < 0:
            running = False
    '''
    for tube in tubes:
        if birtd_rect.colliderect(pygame.Rect(tube[0], tube[1], 50, tube[2])):
            tube_vec = 0
            tube_speed = 0
            GRAVITY = 0
            opacity = 0
            check_live_bird = False
    for tube in tubes_under:
        if birtd_rect.colliderect(pygame.Rect(tube[0], tube[1], 50, tube[2])):
            tube_vec = 0
            tube_speed = 0
            GRAVITY = 0
            opacity = 0
            check_live_bird = False
    if bird_y > screen_height or bird_y < 0:
        tube_vec = 0
        tube_speed = 0
        GRAVITY = 0
        opacity = 0
        check_live_bird = False
    '''You can create tube_rect = pygame.draw.rect(screen, GREEN, (tubes[i][0], tubes[i][1], 50, tubes[i][2])) to use birtd_rect.colliderect(tube_rect)'''
    # Draw the tubes
    for i in range(len(tubes)):
        pygame.draw.rect(screen, GREEN, (tubes[i][0], tubes[i][1], 50, tubes[i][2]))
        pygame.draw.rect(screen, GREEN, (tubes_under[i][0], tubes_under[i][1], 50, tubes_under[i][2]))
        tubes[i][0] -= tube_vec
        tubes_under[i][0] -= tube_vec
        if tube_vec < 6: tube_vec += tube_speed
        if tubes[i][0] <= -50:
            max_t = max(tube[0] for tube in tubes)
            tubes[i][0] = max_t + tube_space + tube_width
            tubes[i][2] = random.randint(200, 400)
            tubes_under[i][0] = tubes[i][0]
            tubes_under[i][2] = screen_height - tubes[i][2] - tube_gap
            tubes_under[i][1] = tubes[i][2] + tube_gap
            passed_tubes[i] = False # Reset the tube as not passed
        if bird_x > tubes[i][0] + tube_width and not passed_tubes[i]: # Check if the bird passed the tube was not passed
            score += 1
            passed_tubes[i] = True  # Mark the tube as passed
    # Draw the score
    text_score = font.render(f"Score: {score}", True, RED)
    screen.blit(text_score, (10, 10))
    if check_live_bird == False:
        text_game_over = font.render("Game over. Click space to continue", True, BLACK)
        pygame.draw.rect(screen, BLACK, (149, 199, 502, 202))
        pygame.draw.rect(screen, WHITE, (150, 200, 500, 200))
        screen.blit(text_game_over, (190, 250))
        screen.blit(text_score, (350, 300))
    # Or you can use this code
    """
    for tube in tubes:
        pygame.draw.rect(screen, GREEN, (tube[0], tube[1], 50, tube[2]))
        tube[0] -= tube_vec
        if tube[0] <= -50:
            max_t = max(tube[0] for tube in tubes)
            tube[0] = max_t + tube_space + tube_width
            tube[2] = random.randint(100, 400)
    for tube, index in enumerate(tubes_under):
        pygame.draw.rect(screen, GREEN, (tube[0], tube[1], 50, tube[2]))
        tube[0] -= tube_vec
        if tube[0] <= -50:
            max_t = tubes[index][0]
            tube[0] = max_t + tube_space + tube_width
            tube[1] = tubes[index][2] + tube_gap
            tube[2] = screen_height - tubes[index][2] - tube_gap
            
    # FIXME: This code is not correct
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if check_live_bird:
                    sound.play()
                    opacity = 0
                    opacity -= 7
                else:
                    # Reset the game
                    tube_vec = 3
                    tube_speed = 0.0005
                    tube_width = 50
                    tube_space = 200
                    tube_gap = 150
                    tubes = [[750, 0, random.randint(200, 400)], [1000, 0, random.randint(200, 400)], [1250, 0, random.randint(200, 400)], [1500, 0, random.randint(200, 400)]]
                    tubes_under = [[750, tubes[0][2] + tube_gap, screen_height - tubes[0][2] - tube_gap],
                                    [1000, tubes[1][2] + tube_gap, screen_height - tubes[1][2] - tube_gap],
                                    [1250, tubes[2][2] + tube_gap, screen_height - tubes[2][2] - tube_gap],
                                    [1500, tubes[3][2] + tube_gap, screen_height - tubes[3][2] - tube_gap]]
                    passed_tubes = [False, False, False, False]
                    bird_x = 150
                    bird_y = 300
                    GRAVITY = 0.5
                    score = 0
                    check_live_bird = True

  
    pygame.display.flip()


pygame.quit()
    