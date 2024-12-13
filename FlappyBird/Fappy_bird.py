import pygame, sys, random  # Import các thư viện pygame, sys, và random
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)  # Khởi tạo bộ trộn âm thanh của pygame trước
pygame.init()  # Khởi tạo pygame

# Khai báo các hàm
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)  # Chọn ngẫu nhiên một chiều cao ống
    bottom_pipe = pipe_surface.get_rect(midtop=(900, random_pipe_pos))  # Tạo ống dưới
    top_pipe = pipe_surface.get_rect(midtop=(900, random_pipe_pos - 650))  # Tạo ống trên
    return (bottom_pipe, False), (top_pipe, False)  # Trả về 2 ống, với trạng thái 'scored' là False

def move_pipe(pipes):
    for pipe, passed in pipes:
        pipe.x -= 7  # Di chuyển ống sang trái (7 pixels mỗi lần)
        if pipe.x < -864:  # Nếu ống ra khỏi màn hình (vị trí x < -864)
            pipes.remove((pipe, passed))  # Xóa ống ra khỏi danh sách
    return pipes

def draw_pipe(pipes):
    for pipe, passed in pipes:
        if pipe.bottom >= 500:  # Nếu ống dưới thì vẽ ống bình thường
            screen.blit(pipe_surface, pipe)
        else:  # Nếu ống trên thì cần phải lật ống lại
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe, passed in pipes:
        if bird_rect.colliderect(pipe):  # Nếu chim va chạm với ống
            hit_sound.play()  # Phát âm thanh va chạm
            if bird_rect.centery > 700:  # Nếu chim dưới mặt đất
                bird_rect.centery -= 9  # Dịch chim lên để tạo cảm giác đập đất
            return False  # Kết thúc trò chơi
    if bird_rect.top <= -75 or bird_rect.bottom >= 700:  # Nếu chim va chạm với biên trên hoặc dưới
        hit_sound.play()  # Phát âm thanh va chạm
        bird_rect.centery = 700  # Đặt chim về vị trí ban đầu
        pygame.transform.flip(bird, True, False)  # Lật chim
        return False  # Kết thúc trò chơi
    return True  # Nếu không va chạm thì tiếp tục trò chơi

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)  # Xoay chim với tốc độ thay đổi
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]  # Chọn hoạt ảnh chim
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))  # Lấy vị trí chim
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main game':  # Khi đang chơi
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))  # Hiển thị điểm
        score_rect = score_surface.get_rect(center=(432, 70))  # Vị trí của điểm
        screen.blit(score_surface, score_rect)  # Vẽ điểm lên màn hình
    if game_state == 'game_over':  # Khi game over
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))  # Hiển thị điểm
        score_rect = score_surface.get_rect(center=(432, 70))  # Vị trí của điểm
        screen.blit(score_surface, score_rect)  # Vẽ điểm lên màn hình
        high_score_surface = game_font.render(f'Highscore: {int(high_score)}', True, (255, 255, 255))  # Hiển thị điểm cao
        high_score_rect = high_score_surface.get_rect(center=(432, 670))  # Vị trí của điểm cao
        screen.blit(high_score_surface, high_score_rect)  # Vẽ điểm cao lên màn hình

def update_score(score, high_score):
    if score > high_score:  # Nếu điểm hiện tại lớn hơn điểm cao
        high_score = score  # Cập nhật điểm cao
    return high_score  # Trả về điểm cao mới

def count_score(pipes):
    global score  # Để cập nhật điểm toàn cục
    for pipe, passed in pipes:
        if pipe.x <= 100 and not passed:  # Kiểm tra nếu chim đã vượt qua ống
            pipes[pipes.index((pipe, passed))] = (pipe, True)  # Đánh dấu ống đã được qua
            score += 2  # Tăng điểm khi chim vượt qua ống
            score_sound.play()  # Phát âm thanh khi vượt qua ống
    return score

# Khởi tạo màn hình và các biến trò chơi
screen_width = 864  # Chiều rộng màn hình
screen_height = 768  # Chiều cao màn hình
screen = pygame.display.set_mode((screen_width, screen_height))  # Thiết lập màn hình với kích thước đã định
pygame.display.set_caption('Flappy Bird')  # Đặt tiêu đề cho cửa sổ game
clock = pygame.time.Clock()  # Khởi tạo đồng hồ để điều khiển tốc độ khung hình
game_font = pygame.font.Font('04B_19.ttf', 40)  # Khởi tạo font chữ

gravity = 0.7  # Lực hấp dẫn tác động lên chim
bird_movement = 0  # Tốc độ di chuyển theo phương thẳng đứng của chim
game_active = False  # Trạng thái game (có đang chơi hay không)
score = 0  # Điểm hiện tại
high_score = 0  # Điểm cao nhất

# Tải các hình ảnh nền và vật phẩm
bg_day = pygame.image.load(r'assets\background-day.png')  # Tải hình nền
bg_day = pygame.transform.scale(bg_day, (screen_width, screen_height))  # Thay đổi kích thước hình nền

floor = pygame.image.load(r'assets\ground.png').convert()  # Tải hình ảnh nền đất
floor = pygame.transform.scale(floor, (screen_width + 200, 100))  # Thay đổi kích thước của đất
floor_x_pos = 0  # Tọa độ x của đất

# Tải và thay đổi kích thước các hình ảnh chim
bird_down = pygame.transform.scale(pygame.image.load(r'assets\yellowbird-downflap.png'), (40, 30)).convert_alpha()
bird_mid = pygame.transform.scale(pygame.image.load(r'assets\yellowbird-midflap.png'), (40, 30)).convert_alpha()
bird_up = pygame.transform.scale(pygame.image.load(r'assets\yellowbird-upflap.png'), (40, 30)).convert_alpha()
bird_list = [bird_down, bird_mid, bird_up]  # Danh sách các hình ảnh chim cho các trạng thái
bird_index = 0  # Chỉ số trạng thái hiện tại của chim
bird = bird_list[bird_index]  # Hình ảnh chim hiện tại
bird_rect = bird.get_rect(center=(100, 200))  # Lấy vị trí và kích thước của chim

birdflap = pygame.USEREVENT  # Sự kiện chim flap
pygame.time.set_timer(birdflap, 100)  # Cài đặt sự kiện flap mỗi 100ms

# Tải và thay đổi kích thước các hình ảnh ống
pipe_surface = pygame.image.load(r'assets\pipe-green.png').convert()
pipe_surface = pygame.transform.scale(pipe_surface, (50, 500))  # Kích thước của ống
pipe_height = [200, 250, 300, 350, 400]  # Các chiều cao của ống
pipe_list = []  # Danh sách các ống

spawnpipe = pygame.USEREVENT  # Sự kiện tạo ống mới
pygame.time.set_timer(spawnpipe, 1000)  # Cài đặt sự kiện tạo ống mỗi 1000ms

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets\message.png')).convert_alpha()  # Hình ảnh game over
game_over_rect = game_over_surface.get_rect(center=(432, 384))  # Vị trí của game over

# Tải các âm thanh
flap_sound = pygame.mixer.Sound('sound\sfx_wing.wav')  # Âm thanh khi chim flap
hit_sound = pygame.mixer.Sound('sound\sfx_hit.wav')  # Âm thanh khi chim va chạm
score_sound = pygame.mixer.Sound('sound\sfx_point.wav')  # Âm thanh khi qua ống

# Vòng lặp chính của game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Nếu người chơi thoát game
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:  # Nếu người chơi nhấn phím
            if event.key == pygame.K_SPACE and game_active:  # Nếu phím space được nhấn và trò chơi đang hoạt động
                bird_movement = 0
                bird_movement = -8  # Đẩy chim lên
                flap_sound.play()  # Phát âm thanh flap

            if event.key == pygame.K_SPACE and not game_active:  # Nếu phím space được nhấn khi game kết thúc
                game_active = True  # Bắt đầu lại trò chơi
                pipe_list.clear()  # Xóa tất cả các ống
                bird_rect.center = (100, 200)  # Đặt lại vị trí chim
                bird_movement = 0  # Đặt lại chuyển động của chim
                score = 0  # Đặt lại điểm

        if event.type == spawnpipe and game_active:  # Nếu đến thời gian spawn pipe và game đang hoạt động
            pipe_list.extend(create_pipe())  # Tạo thêm ống mới

        if event.type == birdflap:  # Sự kiện flap
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()  # Thay đổi hoạt ảnh chim

    screen.blit(bg_day, (0, 0))  # Vẽ hình nền

    if game_active:
        bird_movement += gravity  # Áp dụng lực hấp dẫn lên chim
        rotated_bird = rotate_bird(bird)  # Xoay chim theo chuyển động
        bird_rect.centery += bird_movement  # Cập nhật vị trí của chim
        screen.blit(rotated_bird, bird_rect)  # Vẽ chim lên màn hình

        pipe_list = move_pipe(pipe_list)  # Di chuyển các ống
        draw_pipe(pipe_list)  # Vẽ các ống lên màn hình
        game_active = check_collision(pipe_list)  # Kiểm tra va chạm

        score = count_score(pipe_list)  # Cập nhật điểm
        score_display('main game')  # Hiển thị điểm khi chơi

    else:
        high_score = update_score(score, high_score)  # Cập nhật điểm cao
        score_display('game_over')  # Hiển thị điểm và điểm cao khi game over
        screen.blit(game_over_surface, game_over_rect)  # Vẽ màn hình game over

    screen.blit(floor, (floor_x_pos, 700))  # Vẽ đất lên màn hình
    floor_x_pos -= 5  # Di chuyển đất sang trái
    if abs(floor_x_pos) > 40:  # Nếu đất ra khỏi màn hình, đưa về vị trí ban đầu
        floor_x_pos = 0

    pygame.display.update()  # Cập nhật màn hình
    clock.tick(60)  # Điều chỉnh tốc độ khung hình
