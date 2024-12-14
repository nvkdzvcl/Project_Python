import pygame
import sys
import random

# Lớp GameEntity cơ sở
class GameEntity:
    def __init__(self, screen):
        self.screen = screen  # Lưu trữ đối tượng màn hình nơi các thực thể sẽ được vẽ

    def load_image(self, path, scale=None):
        """
        Tải và tùy chọn thay đổi kích thước một hình ảnh.
        
        Args:
            path (str): Đường dẫn tới tệp hình ảnh
            scale (tuple, optional): Kích thước mong muốn của hình ảnh
        
        Returns:
            pygame.Surface: Hình ảnh đã tải và có thể thay đổi kích thước
        """
        try:
            image = pygame.image.load(path).convert_alpha()  # Tải hình ảnh và xử lý độ trong suốt
            if scale:  # Nếu có kích thước scale được chỉ định, thay đổi kích thước của hình ảnh
                image = pygame.transform.scale(image, scale)
            return image
        except Exception as e:
            print(f"Error loading image {path}: {e}")  # In ra lỗi nếu không thể tải hình ảnh
            return None

# Lớp Game kế thừa từ GameEntity
class Game(GameEntity):
    def __init__(self):
        # Khởi tạo Pygame và các thành phần của nó
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init()

        # Cài đặt màn hình
        self.screen = pygame.display.set_mode((864, 768))  # Màn hình có kích thước 864x768
        pygame.display.set_caption('Flappy Bird')  # Đặt tiêu đề cho cửa sổ trò chơi
        
        # Gọi constructor của lớp cha (GameEntity) để khởi tạo màn hình
        super().__init__(self.screen)

        # Các biến trạng thái của trò chơi
        self.clock = pygame.time.Clock()  # Đồng hồ trò chơi để điều khiển tốc độ khung hình
        self.game_font = pygame.font.Font('04B_19.ttf', 40)  # Tạo font chữ cho điểm số
        self.game_active = False  # Trạng thái trò chơi (hoạt động hay không)
        self.score = 0  # Điểm hiện tại
        self.high_score = 0  # Điểm cao nhất

        # Tải tài nguyên trò chơi (hình ảnh và âm thanh)
        self.bg_day = self.load_image(r'assets\background-day.png', (864, 768))  # Hình nền
        self.floor = self.load_image(r'assets\ground.png', (950, 100))  # Hình nền dưới đất
        self.game_over_surface = pygame.transform.scale2x(self.load_image('assets\message.png'))  # Hình ảnh game over
        
        # Vị trí cuộn của nền dưới đất
        self.floor_x_pos = 0

        # Các đối tượng của trò chơi
        self.bird = Bird(self.screen)  # Khởi tạo đối tượng chim
        self.pipe = Pipe(self.screen)  # Khởi tạo đối tượng ống

        # Vị trí của màn hình game over
        self.game_over_rect = self.game_over_surface.get_rect(center=(432, 384))

        # Tải âm thanh
        self.flap_sound = pygame.mixer.Sound('sound\sfx_wing.wav')  # Âm thanh vỗ cánh
        self.hit_sound = pygame.mixer.Sound('sound\sfx_hit.wav')  # Âm thanh va chạm
        self.score_sound = pygame.mixer.Sound('sound\sfx_point.wav')  # Âm thanh ghi điểm

        # Thiết lập các sự kiện
        self.birdflap = pygame.USEREVENT  # Sự kiện cho hoạt động vỗ cánh của chim
        pygame.time.set_timer(self.birdflap, 100)  # Cập nhật mỗi 100ms

        self.spawnpipe = pygame.USEREVENT  # Sự kiện cho việc tạo ống
        pygame.time.set_timer(self.spawnpipe, 1000)  # Cập nhật mỗi giây

    def score_display(self, game_state):
        """Hiển thị điểm số hiện tại và điểm cao nhất"""
        if game_state == 'main game':
            score_surface = self.game_font.render(str(int(self.score)), True, (255, 255, 255))  # Hiển thị điểm
            score_rect = score_surface.get_rect(center=(432, 70))
            self.screen.blit(score_surface, score_rect)  # Vẽ điểm lên màn hình
        
        if game_state == 'game_over':
            # Điểm hiện tại
            score_surface = self.game_font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(432, 70))
            self.screen.blit(score_surface, score_rect)
            
            # Điểm cao nhất
            high_score_surface = self.game_font.render(f'Highscore: {int(self.high_score)}', True, (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(center=(432, 670))
            self.screen.blit(high_score_surface, high_score_rect)

    def update_score(self):
        """Cập nhật và trả về điểm cao nhất"""
        if self.score > self.high_score:
            self.high_score = self.score
        return self.high_score

    def check_collision(self, bird_rect):
        """Kiểm tra va chạm với ống và biên của màn hình"""
        for pipe, passed in self.pipe.pipe_list:
            if bird_rect.colliderect(pipe):  # Nếu chim va chạm với ống
                self.hit_sound.play()  # Phát âm thanh va chạm
                if bird_rect.centery > 700:  # Nếu chim quá gần đáy, giảm vị trí
                    bird_rect.centery -= 9
                return False  # Dừng trò chơi (chim chết)
        
        if bird_rect.top <= -75 or bird_rect.bottom >= 700:  # Kiểm tra va chạm với biên trên và dưới màn hình
            self.hit_sound.play()  # Phát âm thanh va chạm
            bird_rect.centery = 700  # Đặt lại vị trí chim
            pygame.transform.flip(self.bird.bird, True, False)  # Lật chim khi chết
            return False  # Dừng trò chơi (chim chết)
        
        return True  # Không va chạm, trò chơi tiếp tục

    def run(self):
        """Vòng lặp chính của trò chơi"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  # Thoát trò chơi

                if event.type == pygame.KEYDOWN:
                    # Khi nhấn phím cách, chim vỗ cánh
                    if event.key == pygame.K_SPACE and self.game_active:
                        self.bird.bird_movement = 0  # Đặt lại chuyển động của chim
                        self.bird.bird_movement = -8  # Vỗ cánh (di chuyển lên)
                        self.flap_sound.play()  # Phát âm thanh vỗ cánh
                    
                    # Khi nhấn phím cách trong trạng thái game over, khởi động lại trò chơi
                    if event.key == pygame.K_SPACE and not self.game_active:
                        self.game_active = True
                        self.pipe.pipe_list.clear()  # Xóa các ống
                        self.bird.rect.center = (100, 200)  # Đặt lại vị trí chim
                        self.bird.bird_movement = 0
                        self.score = 0

                # Tạo ống mới
                if event.type == self.spawnpipe and self.game_active:
                    self.pipe.pipe_list.extend(self.pipe.create_pipe())

                # Hoạt động vỗ cánh của chim
                if event.type == self.birdflap:
                    if self.bird.bird_index < 2:
                        self.bird.bird_index += 1
                    else:
                        self.bird.bird_index = 0
                    self.bird.bird, self.bird.rect = self.bird.bird_animation()

            # Vẽ nền
            self.screen.blit(self.bg_day, (0, 0))

            # Trạng thái game đang hoạt động
            if self.game_active:
                rotated_bird, bird_rect = self.bird.update(self.bird.bird_movement, self.flap_sound)
                self.screen.blit(rotated_bird, bird_rect)
                
                self.pipe.pipe_list = self.pipe.move_pipe()
                self.pipe.draw_pipe(self.screen)
                
                self.game_active = self.check_collision(bird_rect)  # Kiểm tra va chạm
                self.score += self.pipe.count_score(bird_rect)  # Cập nhật điểm
                self.score_display('main game')

            # Trạng thái game over
            else:
                self.high_score = self.update_score()  # Cập nhật điểm cao nhất
                self.score_display('game_over')
                self.screen.blit(self.game_over_surface, self.game_over_rect)

            # Cuộn nền dưới đất
            self.screen.blit(self.floor, (self.floor_x_pos, 700))
            self.floor_x_pos -= 5  # Di chuyển nền sang trái
            if abs(self.floor_x_pos) > 40:  # Nếu nền đã di chuyển quá xa, đặt lại vị trí
                self.floor_x_pos = 0

            # Cập nhật màn hình
            pygame.display.update()
            self.clock.tick(60)  # Điều khiển tốc độ khung hình

# Lớp Bird kế thừa từ GameEntity
class Bird(GameEntity):
    def __init__(self, screen):
        super().__init__(screen)
        
        # Tải hình ảnh chim
        self.bird_down = self.load_image(r'assets\yellowbird-downflap.png', (35, 30))
        self.bird_mid = self.load_image(r'assets\yellowbird-midflap.png', (35, 30))
        self.bird_up = self.load_image(r'assets\yellowbird-upflap.png', (35, 30))
        
        self.bird_list = [self.bird_down, self.bird_mid, self.bird_up]
        self.bird_index = 0  # Chỉ số của hình ảnh chim hiện tại
        self.bird = self.bird_list[self.bird_index]  # Chim hiện tại
        self.rect = self.bird.get_rect(center=(100, 200))  # Tạo hình chữ nhật cho chim
        self.bird_movement = 0  # Chuyển động của chim (vị trí dọc)

    def bird_animation(self):
        """Hoạt động vỗ cánh của chim"""
        new_bird = self.bird_list[self.bird_index]  # Chọn hình ảnh chim hiện tại
        new_bird_rect = new_bird.get_rect(center=(100, self.rect.centery))  # Tạo hình chữ nhật cho chim
        return new_bird, new_bird_rect

    def rotate_bird(self):
        """Xoay chim dựa trên chuyển động"""
        return pygame.transform.rotozoom(self.bird, -self.bird_movement * 3, 1)

    def update(self, bird_movement, flap_sound):
        """Cập nhật vị trí và xoay chim"""
        self.bird_movement += 0.7  # Hằng số trọng lực
        rotated_bird = self.rotate_bird()
        self.rect.centery += self.bird_movement  # Cập nhật vị trí chim
        return rotated_bird, self.rect

# Lớp Pipe kế thừa từ GameEntity
class Pipe(GameEntity):
    def __init__(self, screen):
        super().__init__(screen)
        
        # Tải hình ảnh ống
        self.pipe_surface = self.load_image(r'assets\pipe-green.png', (50, 500))
        
        self.pipe_list = []  # Danh sách các ống
        self.pipe_height = [200, 250, 300, 350, 400]  # Các độ cao ngẫu nhiên cho ống

    def create_pipe(self):
        """Tạo một cặp ống"""
        random_pipe_pos = random.choice(self.pipe_height)  # Chọn vị trí ngẫu nhiên cho ống
        bottom_pipe = self.pipe_surface.get_rect(midtop=(900, random_pipe_pos))  # Ống dưới
        top_pipe = self.pipe_surface.get_rect(midtop=(900, random_pipe_pos - 650))  # Ống trên
        return (bottom_pipe, False), (top_pipe, False)

    def move_pipe(self):
        """Di chuyển các ống trên màn hình"""
        for pipe, passed in self.pipe_list:
            pipe.x -= 7  # Di chuyển ống sang trái
            if pipe.x < -600:  # Nếu ống ra khỏi màn hình, xóa ống
                self.pipe_list.remove((pipe, passed))
        return self.pipe_list

    def draw_pipe(self, screen):
        """Vẽ các ống trên màn hình"""
        for pipe, passed in self.pipe_list:
            if pipe.bottom >= 500:  # Vẽ ống dưới
                screen.blit(self.pipe_surface, pipe)
            else:  # Lật ống trên
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                screen.blit(flip_pipe, pipe)

    def count_score(self, bird_rect):
        """Đếm điểm khi chim vượt qua ống"""
        score = 0
        for i, (pipe, passed) in enumerate(self.pipe_list):
            if not passed and pipe.right < bird_rect.left:  # Nếu chim vượt qua ống
                self.pipe_list[i] = (pipe, True)
                score += 0.5  # Cộng thêm 0.5 điểm
                pygame.mixer.Sound('sound\sfx_point.wav').play()  # Phát âm thanh ghi điểm
        return score

# Chạy trò chơi
if __name__ == '__main__':
    game = Game()
    game.run()
