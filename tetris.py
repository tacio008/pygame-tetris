import pygame
import random
import sys

# Inicializar
pygame.init()
#musica
pygame.init()

try:
    pygame.mixer.music.load("audio/tetrismusic.mp3")
    pygame.mixer.music.play(-1)  #bucle
except pygame.error:
    print("no music lol")

# Colores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
WHITE = (255, 255, 255)

# Configuración
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 25

# Posición del tablero
BOARD_X = 250
BOARD_Y = 50

# Formas
TETROMINOES = [
    
    [['.....',
      '..#..',
      '..#..',
      '..#..',
      '..#..'],
     ['.....',
      '.....',
      '####.',
      '.....',
      '.....']],
    
    
    [['.....',
      '.....',
      '.##..',
      '.##..',
      '.....']],
    
    
    [['.....',
      '.....',
      '.#...',
      '###..',
      '.....'],
     ['.....',
      '.....',
      '.#...',
      '.##..',
      '.#...'],
     ['.....',
      '.....',
      '.....',
      '###..',
      '.#...'],
     ['.....',
      '.....',
      '.#...',
      '##...',
      '.#...']],
    
    
    [['.....',
      '.....',
      '.##..',
      '##...',
      '.....'],
     ['.....',
      '.....',
      '.#...',
      '.##..',
      '..#..']],
    
    
    [['.....',
      '.....',
      '##...',
      '.##..',
      '.....'],
     ['.....',
      '.....',
      '..#..',
      '.##..',
      '.#...']],
    
    
    [['.....',
      '.....',
      '.#...',
      '.#...',
      '##...'],
     ['.....',
      '.....',
      '.....',
      '#....',
      '###..'],
     ['.....',
      '.....',
      '.##..',
      '.#...',
      '.#...'],
     ['.....',
      '.....',
      '.....',
      '###..',
      '..#..']],
    
    
    [['.....',
      '.....',
      '.#...',
      '.#...',
      '.##..'],
     ['.....',
      '.....',
      '.....',
      '###..',
      '#....'],
     ['.....',
      '.....',
      '##...',
      '.#...',
      '.#...'],
     ['.....',
      '.....',
      '.....',
      '..#..',
      '###..']]
]

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.current_rotation = 0
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500  # ms
        self.spawn_new_piece()
        
        # pantalla
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("TETRIS")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def spawn_new_piece(self):
        self.current_piece = random.choice(TETROMINOES)
        self.current_rotation = 0
        self.current_x = GRID_WIDTH // 2 - 2
        self.current_y = 0

        
        # game over
        if self.check_collision():
            return False
        return True
        
    def check_collision(self, dx=0, dy=0, rotation=None):
        if rotation is None:
            rotation = self.current_rotation
            
        piece = self.current_piece[rotation % len(self.current_piece)]
        
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell == '#':
                    new_x = self.current_x + x + dx
                    new_y = self.current_y + y + dy
                    
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return True
        return False
        
    def place_piece(self):
        piece = self.current_piece[self.current_rotation % len(self.current_piece)]
        
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell == '#':
                    grid_x = self.current_x + x
                    grid_y = self.current_y + y
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = 1
                        
        self.clear_lines()
        
    def clear_lines(self):
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                lines_to_clear.append(y)
                
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            
        lines_cleared = len(lines_to_clear)
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            self.score += lines_cleared * 100 * self.level
            self.level = min(10, self.lines_cleared // 10 + 1)
            self.fall_speed = max(50, 500 - (self.level - 1) * 50)
            
    def move_piece(self, dx, dy):
        if not self.check_collision(dx, dy):
            self.current_x += dx
            self.current_y += dy
            return True
        return False
        
    def rotate_piece(self):
        new_rotation = (self.current_rotation + 1) % len(self.current_piece)
        if not self.check_collision(rotation=new_rotation):
            self.current_rotation = new_rotation
            
    def draw_grid(self):
        # borde
        border_rect = pygame.Rect(BOARD_X - 2, BOARD_Y - 2, 
                                 GRID_WIDTH * CELL_SIZE + 4, 
                                 GRID_HEIGHT * CELL_SIZE + 4)
        pygame.draw.rect(self.screen, GREEN, border_rect, 2)
        
        # líneas de la cuadrícula
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, DARK_GREEN,
                           (BOARD_X + x * CELL_SIZE, BOARD_Y),
                           (BOARD_X + x * CELL_SIZE, BOARD_Y + GRID_HEIGHT * CELL_SIZE))
                           
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, DARK_GREEN,
                           (BOARD_X, BOARD_Y + y * CELL_SIZE),
                           (BOARD_X + GRID_WIDTH * CELL_SIZE, BOARD_Y + y * CELL_SIZE))
        
        # piezas ya colocadas
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    rect = pygame.Rect(BOARD_X + x * CELL_SIZE, 
                                     BOARD_Y + y * CELL_SIZE,
                                     CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, GREEN, rect)
                    
    def draw_current_piece(self):
        if self.current_piece:
            piece = self.current_piece[self.current_rotation % len(self.current_piece)]
            
            for y, row in enumerate(piece):
                for x, cell in enumerate(row):
                    if cell == '#':
                        rect = pygame.Rect(BOARD_X + (self.current_x + x) * CELL_SIZE,
                                         BOARD_Y + (self.current_y + y) * CELL_SIZE,
                                         CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, GREEN, rect)
                        
    def draw_ui(self):
        # Información del juego
        info_x = 50
        info_y = 50
        
        # Título
        title_text = self.font.render("TETRIS", True, GREEN)
        self.screen.blit(title_text, (info_x, info_y - 30))
        
        # LR
        lines_text = self.small_font.render(f"points: {self.lines_cleared}", True, GREEN)
        self.screen.blit(lines_text, (info_x, info_y))
        
        # Nivel
        level_text = self.small_font.render(f"@iblameportacio on ig: {self.level}", True, GREEN)
        self.screen.blit(level_text, (info_x, info_y + 30))
        
        # Puntuación
        score_text = self.small_font.render(f"2025: {self.score}", True, GREEN)
        self.screen.blit(score_text, (info_x, info_y + 60))
        
        # creditos no c
        creditos_x = BOARD_X + GRID_WIDTH * CELL_SIZE + 30
        creditos_y = BOARD_Y + 50
        
        creditos = [
            "created by - archtacio"
        ]
        
        for i, control in enumerate(creditos):
            control_text = self.small_font.render(control, True, GREEN)
            self.screen.blit(control_text, (creditos_x, creditos_y + i * 25))
            
    def run(self):
        running = True
        game_over = False
        
        while running:
            dt = self.clock.tick(60)
            self.fall_time += dt
            
            # eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.KEYDOWN:
                    if game_over:
                        if event.key == pygame.K_r:
                            # Reiniciar 
                            self.__init__()
                            game_over = False
                    else:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_7:
                            self.move_piece(-1, 0)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_9:
                            self.move_piece(1, 0)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_4:
                            self.move_piece(0, 1)
                        elif event.key == pygame.K_UP or event.key == pygame.K_8:
                            self.rotate_piece()
                        elif event.key == pygame.K_SPACE or event.key == pygame.K_5:
                            # Caída rápida
                            while self.move_piece(0, 1):
                                pass
                            
            # Lógica
            if not game_over:
                # Caída automática
                if self.fall_time >= self.fall_speed:
                    if not self.move_piece(0, 1):
                        self.place_piece()
                        if not self.spawn_new_piece():
                            game_over = True
                    self.fall_time = 0
                    

            # Dibujar
            self.screen.fill(BLACK)
            self.draw_grid()
            if not game_over:
                self.draw_current_piece()
            self.draw_ui()
            
            if game_over:
                game_over_text = self.font.render("Its Over", True, GREEN)
                restart_text = self.small_font.render("hi :)", True, GREEN)
                self.screen.blit(game_over_text, (BOARD_X + 20, BOARD_Y + 200))
                self.screen.blit(restart_text, (BOARD_X + 10, BOARD_Y + 240))
            
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Tetris()
    game.run()