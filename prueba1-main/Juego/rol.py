import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla (aumentadas)
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survivor")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Clase base para el jugador
class Player:
    def __init__(self, role):
        self.role = role
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.health = 100 if role != "fighter" else 200  # Luchador tiene el doble de vida
        self.score = 0
        self.armor = 0
        self.life_steal = 0
        self.bullet_speed = 5  # Velocidad base de las balas

        # Ajustar atributos según el rol
        if role == "archer":
            self.damage = 5  # Aumentar daño
            self.bullet_speed += 5  # Balas más rápidas
        elif role == "fighter":
            self.damage = 10  # Alto daño, sin balas
            self.bullet_speed = 0
        elif role == "ninja":
            self.damage = 3
            self.bullet_speed = 5  # Balas más lentas
            self.dash_cooldown = 4  # Cooldown del dash
            self.last_dash_time = 0
            self.dashing = False

    def move(self, dx, dy):
        if self.role == "ninja" and self.dashing:
            return  # No mover si está en dash
        self.rect.x += dx
        self.rect.y += dy
        # Asegurarse de que el jugador no se salga de la pantalla
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def take_damage(self, amount):
        damage_taken = max(0, amount - self.armor)
        self.health -= damage_taken
        self.health = max(0, self.health)  # Asegurarse de que la salud no sea negativa

    def heal(self, amount):
        self.health = min(self.health + amount, 100 if self.role != "fighter" else 200)  # Luchador tiene hasta 200

    def dash(self):
        if pygame.time.get_ticks() - self.last_dash_time >= self.dash_cooldown * 1000:
            self.last_dash_time = pygame.time.get_ticks()
            return True
        return False

# Clase para los zombis
class Zombie:
    def __init__(self, wave):
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
        self.health = 10 + (wave * 2)
        self.attack = 1 + wave

    def move_towards_player(self, player):
        if player.rect.x < self.rect.x:
            self.rect.x -= 1
        elif player.rect.x > self.rect.x:
            self.rect.x += 1

        if player.rect.y < self.rect.y:
            self.rect.y -= 1
        elif player.rect.y > self.rect.y:
            self.rect.y += 1

# Clase para las balas
class Bullet:
    def __init__(self, x, y, direction, damage):
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.damage = damage

    def move(self):
        self.rect.x += self.direction[0] * self.damage
        self.rect.y += self.direction[1] * self.damage

# Función para mostrar texto
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Función para mostrar mejoras
def show_upgrades(screen, font):
    options = ["1. Aumentar daño", "2. Aumentar velocidad de balas", "3. Curar 20 salud", "4. Aumentar armadura", "5. Robo de vida"]
    for i, option in enumerate(options):
        draw_text(option, font, WHITE, screen, 200, 200 + i * 40)
    pygame.display.flip()

    selected_upgrade = None
    while selected_upgrade is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_upgrade = "damage"
                elif event.key == pygame.K_2:
                    selected_upgrade = "bullet_speed"
                elif event.key == pygame.K_3:
                    selected_upgrade = "heal"
                elif event.key == pygame.K_4:
                    selected_upgrade = "armor"
                elif event.key == pygame.K_5:
                    selected_upgrade = "life_steal"
    return selected_upgrade

# Función para mostrar el menú de pausa
def pause_menu():
    font = pygame.font.Font(None, 74)
    pause_text = font.render("PAUSE", True, WHITE)
    resume_text = font.render("Press P to Resume", True, WHITE)
    exit_text = font.render("Press ESC to Quit", True, WHITE)

    while True:
        screen.fill(BLACK)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Reanudar juego
                    return
                if event.key == pygame.K_ESCAPE:  # Salir del juego
                    pygame.quit()
                    exit()

# Función para la selección de personajes
def character_selection():
    font = pygame.font.Font(None, 74)
    archer_text = font.render("1. Archer", True, WHITE)
    fighter_text = font.render("2. Fighter", True, WHITE)
    ninja_text = font.render("3. Ninja", True, WHITE)
    select_text = font.render("Select your character (1, 2, 3):", True, WHITE)

    while True:
        screen.fill(BLACK)
        screen.blit(select_text, (WIDTH // 2 - select_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(archer_text, (WIDTH // 2 - archer_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(fighter_text, (WIDTH // 2 - fighter_text.get_width() // 2, HEIGHT // 2))
        screen.blit(ninja_text, (WIDTH // 2 - ninja_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "archer"
                elif event.key == pygame.K_2:
                    return "fighter"
                elif event.key == pygame.K_3:
                    return "ninja"

# Función principal
def main():
    clock = pygame.time.Clock()
    role = character_selection()  # Selección de personaje
    player = Player(role)
    zombies = [Zombie(1) for _ in range(5)]
    bullets = []
    font = pygame.font.Font(None, 36)
    wave = 1
    running = True

    while running:
        screen.fill(BLACK)

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pausar el juego
                    pause_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Disparar con el ratón
                if event.button == 1:  # Botón izquierdo del ratón
                    direction = pygame.mouse.get_pos()
                    direction = (direction[0] - player.rect.centerx, direction[1] - player.rect.centery)
                    distance = math.sqrt(direction[0]**2 + direction[1]**2)
                    if distance > 0:  # Evitar división por cero
                        direction = (direction[0] / distance, direction[1] / distance)  # Normalizar
                        bullets.append(Bullet(player.rect.centerx, player.rect.centery, direction, player.damage))

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]:  # Izquierda
            dx = -5
        if keys[pygame.K_d]:  # Derecha
            dx = 5
        if keys[pygame.K_w]:  # Arriba
            dy = -5
        if keys[pygame.K_s]:  # Abajo
            dy = 5
        
        player.move(dx, dy)

        # Mover zombis
        for zombie in zombies:
            zombie.move_towards_player(player)

        # Mover balas
        for bullet in bullets[:]:
            bullet.move()
            # Comprobar colisiones con zombis
            for zombie in zombies[:]:
                if bullet.rect.colliderect(zombie.rect):
                    zombie.health -= bullet.damage
                    bullets.remove(bullet)
                    if zombie.health <= 0:
                        player.score += 10  # Puntos por matar zombis
                        zombies.remove(zombie)
                    break  # Salir del bucle tras eliminar la bala

        # Generar nuevos zombis si quedan
        if len(zombies) == 0:
            wave += 1
            zombies = [Zombie(wave) for _ in range(wave * 2)]  # Incrementar dificultad

        # Dibujar personajes
        screen.blit(player.image, player.rect)
        for zombie in zombies:
            screen.blit(zombie.image, zombie.rect)
        for bullet in bullets:
            screen.blit(bullet.image, bullet.rect)

        # Mostrar puntuación
        draw_text(f'Score: {player.score}', font, WHITE, screen, 10, 10)
        draw_text(f'Health: {player.health}', font, WHITE, screen, 10, 40)

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

