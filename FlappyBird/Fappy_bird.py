import pygame , sys, random
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
#ham ve floor
# def draw_floor():
#     screen.blit(floor, (floor_x_pos, 700)) # nen dat 1 
#     screen.blit(floor, (floor_x_pos + 864, 700)) # nen dat 2
#ham tao pipe 
def create_pipe():
    random_pipe_pos= random.choice(pipe_height)
    bottom_pipe =pipe_surface.get_rect( midtop=(900,random_pipe_pos)) #tao hinh chu nhat quay pipe img de thuc  hien them va cham cho pipe
    top_pipe=pipe_surface.get_rect(midtop =(900, random_pipe_pos-650)) #nằm trên góc tọa độ x 
    return bottom_pipe, top_pipe
#ham di chuyen pipe
def move_pipe(pipes):      
    for pipe in pipes:
        pipe.centerx-=7 #pipe lui ve truc x sau moi 1,2s cu the la 5 moi 1,2s
    return pipes
# ve pipe vao screenscreen
def draw_pipe(pipes): #screen blit la de chen anh vao screen , screen_blit chi co the lay gia tri voi 1 phan tu co 1 gia tri thoi 
    for pipe in pipes:
        if pipe.bottom >=500: #so nay phai lon hon so pipe.bottom co 
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False, True)
            screen.blit(flip_pipe, pipe)
# xu ly va cham
def check_collision (pipes):
    for pipe in pipes:
        #va cham voi ong
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            if(bird_rect.centery>700):
                bird_rect.centery-=9
            return False
    # va cham voi bot border and bot border
    if bird_rect.top <=-75 or bird_rect.bottom >=700: #700 is the floor position
        hit_sound.play()
        bird_rect.centery=700
        pygame.transform.flip(bird,True, False)
        return False
    return True
#tao ham xoay chim
def rotate_bird(bird1):
    new_bird=pygame.transform.rotozoom(bird1,-bird_movement*3, 1) #tao chuyen dong khi chim nhay len hoac xuong
    return new_bird
#tao chuyen dong vay canh cho birdbird
def bird_animation():   
    new_bird=bird_list[bird_index]
    new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state== 'main game':
        score_surface=game_font.render(str(int(score)), True, (255,255,255))
        score_rect=score_surface.get_rect(center=(432,70))
        screen.blit(score_surface, score_rect)
    if game_state== 'game_over':
        score_surface=game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect=score_surface.get_rect(center=(432,70))
        screen.blit(score_surface, score_rect)

        high_score_surface=game_font.render(f'Highscore: {int(high_score)}', True, (255,255,255))
        high_score_rect=high_score_surface.get_rect(center=(432,670))
        screen.blit(high_score_surface, high_score_rect)
def update_score(score, high_score):
    if score> high_score:
        high_score=score
    return high_score
def count_score(pipes):
    score=0
    for pipe in pipes:
        if pipe.x <= 100:
            score+=0.5
    return score
#system variable 
screen_width=864
screen_height=768
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Flappy bird')
clock = pygame.time.Clock()
game_font=pygame.font.Font('04B_19.ttf',40)
#tao variable cho tro choi
gravity = 0.7
bird_movement = 0
game_active=False
score=0
high_score=0
game_run = False
# create bg
bg_day=pygame.image.load(r'assets\background-day.png')
bg_day=pygame.transform.scale(bg_day ,( screen_width,screen_height))

# create floor
floor = pygame.image.load(r'assets\ground.png').convert()  # convert for img to become smooth
floor = pygame.transform.scale( floor,( screen_width+200,100))
floor_x_pos = 0

# create bird
#tao wings cho bird
bird_down=pygame.transform.scale(pygame.image.load(r'assets\yellowbird-downflap.png'), (40,30)).convert_alpha()
bird_mid=pygame.transform.scale(pygame.image.load(r'assets\yellowbird-midflap.png'),(40,30)).convert_alpha()
bird_up=pygame.transform.scale(pygame.image.load(r'assets\yellowbird-upflap.png'),(40,30)).convert_alpha()
bird_list=[bird_down,bird_mid,bird_up]
bird_index=0
bird=bird_list[bird_index]

bird_rect = bird.get_rect(center=(100, 200))
#create bird wings timer
birdflap=pygame.USEREVENT
pygame.time.set_timer(birdflap, 100)
# bird = pygame.image.load(r'assets\yellowbird-midflap.png').convert_alpha()  # convert for img to become smooth
# bird = pygame.transform.scale2x(bird)  # bigger the img 

# create pipe
pipe_surface =pygame.image.load(r'assets\pipe-green.png').convert() #bien chen hinh pipe vao
pipe_surface= pygame.transform.scale(pipe_surface, ( 50,500))
pipe_list=[]
# create pipe timmer - spawm time
spawnpipe=pygame.USEREVENT #tao 1 eventevent
pygame.time.set_timer(spawnpipe,1000) # cua moi 1,2s thi event spawpipe se xuat hien
pipe_height=[200,250,300,350,400]
#tao man hinh game over 
game_over_surface=pygame.transform.scale2x( pygame.image.load('assets\message.png')).convert_alpha() 
game_over_rect=game_over_surface.get_rect(center=(432,384))
#insert sound 
flap_sound=pygame.mixer.Sound( 'sound\sfx_wing.wav')
hit_sound=pygame.mixer.Sound( 'sound\sfx_hit.wav')
score_sound=pygame.mixer.Sound( 'sound\sfx_point.wav')
#while loop cua game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -8
                flap_sound.play()
                
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 200)
                bird_movement = 0
                score = 0
                game_run = True

        if event.type == spawnpipe and game_active:
            pipe_list.extend(create_pipe())

        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    # Create background
    screen.blit(bg_day, (0, 0))
    
    if game_active:
        # Bird movement
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        # Pipe movement and collision
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        game_active = check_collision(pipe_list)
        
        # Increment score
        score = count_score(pipe_list)
        score_display('main game')

    else:
        # Game over screen
        screen.blit(bird, bird_rect)
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

        # Reset game_run after game over
        game_run = False

    # Move floor
    screen.blit(floor, (floor_x_pos, 700)) # nen dat 1 
    floor_x_pos -= 2
    
    if abs(floor_x_pos)>40:
        floor_x_pos = 0
 
    pygame.display.update()

    # Adjust the frame rate (Try 60 fps for smoother performance)
    clock.tick(60)  # Try using 60 instead of 140
pygame.quit()
