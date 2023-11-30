import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Configuración del juego
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bomberman")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)  # Marrón
ORANGE = (255, 165, 0)  # Naranja

# Parámetros ajustables
explosion_duration = 1000  # Duración de la explosión en milisegundos
bomb_damage = 1  # Daño de la bomba
player_health = 6  # Vida inicial del jugador

# Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, keys):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.keys = keys
        self.bombs = 1  # Cantidad de bombas que puede colocar
        self.explosion_range = 3  # Rango de explosión
        self.health = player_health  # Vida del jugador

# Bomba
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)  # Color blanco
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player
        self.explosion_time = pygame.time.get_ticks() + 1500  # 4 segundos (en milisegundos)

    def update(self):
        # Verificar si ha pasado el tiempo de explosión
        current_time = pygame.time.get_ticks()
        if current_time >= self.explosion_time:
            self.explode()

    def explode(self):
        # Crea una explosión en forma de cruz
        explosions.add(Explosion(self.rect.center, self.player.explosion_range))
        self.player.bombs += 1 
        self.kill()  # Elimina la bomba después de la explosión

# Explosión
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, range):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(ORANGE)  # Color naranja para la explosión
        self.rect = self.image.get_rect(center=center)
        self.range = range
        self.timer = pygame.time.get_ticks()  # Registrar el tiempo de creación

    def update(self):
        # La explosión se expande durante 15 fotogramas
        if self.timer < 15:
            self.rect.width += int(self.range * 1.66)  # 1.66 es un factor de ajuste para la proporción de la cruz
            self.rect.height += int(self.range * 1.66)
            self.rect.x -= int(self.range * 0.83)
            self.rect.y -= int(self.range * 0.83)
            self.timer += 1
        else:
            self.kill()  # Elimina la explosión después de expandirse

# Borde marrón
class BrownBorder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Grupo de jugadores
players = pygame.sprite.Group()
player1 = Player(50, 50, RED, {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "bomb": pygame.K_LCTRL})
player2 = Player(width - 80, height - 80, BLUE, {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "bomb": pygame.K_RCTRL})
players.add(player1, player2)

# Grupo de bombas
bombs = pygame.sprite.Group()

# Grupo de explosiones
explosions = pygame.sprite.Group()

# Grupo de bordes marrones
borders = pygame.sprite.Group()

# Grupo para el menú
menu = pygame.sprite.Group()

# Crear bordes marrones en los cuatro lados con espacios para pasar
border_width = 20
space_size = 10

# Arriba
for i in range(0, width, border_width + space_size):
    borders.add(BrownBorder(i, 0))
    borders.add(BrownBorder(i + space_size, 0))

# Abajo
for i in range(0, width, border_width + space_size):
    borders.add(BrownBorder(i, height - border_width))
    borders.add(BrownBorder(i + space_size, height - border_width))

# Izquierda
for i in range(border_width + space_size, height - border_width, border_width + space_size):
    borders.add(BrownBorder(0, i))
    borders.add(BrownBorder(0, i + space_size))

# Derecha
for i in range(border_width + space_size, height - border_width, border_width + space_size):
    borders.add(BrownBorder(width - border_width, i))
    borders.add(BrownBorder(width - border_width, i + space_size))

# Fuente para el texto
font = pygame.font.Font(None, 74)

# Función para mostrar el texto en la pantalla
def show_text(text, color, y_offset=0):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2 + y_offset))
    screen.blit(text_surface, text_rect)

# Estado del juego
game_running = True
game_over = False
in_menu = True

# Reloj para controlar los fotogramas por segundo
clock = pygame.time.Clock()

# Bucle principal
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                in_menu = not in_menu
            elif event.key == pygame.K_r and in_menu:
                # Reiniciar juego
                players = pygame.sprite.Group()
                player1 = Player(50, 50, RED, {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "bomb": pygame.K_LCTRL})
                player2 = Player(width - 80, height - 80, BLUE, {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "bomb": pygame.K_RCTRL})
                players.add(player1, player2)

                bombs = pygame.sprite.Group()
                explosions = pygame.sprite.Group()

                game_over = False

    if in_menu:
        # Mostrar menú
        screen.fill(BLACK)
        show_text("Bomberman", WHITE, -50)
        show_text("Presiona ESC para jugar", WHITE, 50)
    elif not game_over:
        # Juego en ejecución
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        # Capturar teclas presionadas
        keys = pygame.key.get_pressed()

        # Mover jugadores y permitir atravesar los bordes
        for player in players:
            if keys[player.keys["up"]]:
                player.rect.y -= 5
            if keys[player.keys["down"]]:
                player.rect.y += 5
            if keys[player.keys["left"]]:
                player.rect.x -= 5
            if keys[player.keys["right"]]:
                player.rect.x += 5

            # Permitir que los jugadores atraviesen los bordes
            if player.rect.y < 0:
                player.rect.y = height - player.rect.height
            elif player.rect.y > height - player.rect.height:
                player.rect.y = 0
            elif player.rect.x < 0:
                player.rect.x = width - player.rect.width
            elif player.rect.x > width - player.rect.width:
                player.rect.x = 0

            # Colocar bombas
            if keys[player.keys["bomb"]] and player.bombs > 0:
                bomb = Bomb(player.rect.x, player.rect.y, player)
                bombs.add(bomb)
                player.bombs -= 1

        # Actualizar bombas
        bombs.update()

        # Lógica del juego

        # Verificar colisiones con las explosiones
        for player in players:
            explosion_hit = pygame.sprite.spritecollide(player, explosions, False)
            if explosion_hit:
                player.health -= bomb_damage

        # Eliminar jugadores con vida <= 0
        players.remove([player for player in players if player.health <= 0])

        # Limpiar explosiones que han superado la duración de 1 segundo
        current_time = pygame.time.get_ticks()
        explosions.remove([explosion for explosion in explosions if current_time - explosion.timer >= explosion_duration])

        # Dibujar en la pantalla
        screen.fill(BLACK)
        borders.draw(screen)
        players.draw(screen)
        bombs.draw(screen)
        explosions.draw(screen)

        # Verificar si todos los jugadores han muerto
        if not players:
            game_over = True
            show_text("Game Over", WHITE)  # Mostrar "Game Over" en la pantalla de juego

    else:
        # Juego terminado
        screen.fill(BLACK)
        show_text("Game Over", WHITE)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar los fotogramas por segundo
    clock.tick(60)  # Puedes ajustar el número según sea necesario

# Salir del juego
pygame.quit()
sys.exit()
