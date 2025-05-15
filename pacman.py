import pygame
import random

# --- Initialisation de Pygame ---
pygame.init()

# --- Constantes de couleurs ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0) # Pour les power pellets (non implémenté en détail ici)

# --- Paramètres de l'écran ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 680 # Un peu plus haut pour le score
BLOCK_SIZE = 30 # Taille de chaque case du labyrinthe
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Simplifié")

# --- Horloge pour contrôler le FPS ---
clock = pygame.time.Clock()
FPS = 10 # Contrôle la vitesse du jeu

# --- Police pour le score ---
font = pygame.font.SysFont('Arial', 24)

# --- Définition du Labyrinthe ---
# 0: Mur, 1: Passage libre (pac-gomme), 2: Espace vide (déjà mangé), 3: Power Pellet (non utilisé ici)
# Le labyrinthe doit avoir des dimensions qui correspondent à SCREEN_WIDTH / BLOCK_SIZE
# et (SCREEN_HEIGHT - EspaceScore) / BLOCK_SIZE
maze_layout = [
    "00000000000000000000",
    "01111111111111111110",
    "01001001000100100110",
    "01111111100111111110",
    "01001001111110010010",
    "01111001000100111110",
    "00011111100111111000",
    "00010010000001001000",
    "01111011100111011110",
    "01001001000100100110",
    "01111111111111111110",
    "00000000000000000000"
]
# Adapter le labyrinthe pour qu'il y ait plus de lignes pour le jeu
maze_rows = len(maze_layout)
maze_cols = len(maze_layout[0])
GAME_AREA_HEIGHT = maze_rows * BLOCK_SIZE

# --- Classe PacMan ---
class PacMan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([BLOCK_SIZE - 4, BLOCK_SIZE - 4]) # Un peu plus petit que le bloc
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * BLOCK_SIZE + 2, y * BLOCK_SIZE + 2)
        self.speed_x = 0
        self.speed_y = 0
        self.current_direction = None # Pour l'animation de la bouche (non implémenté)
        self.next_direction = None
        self.next_direction_x = None
        self.next_direction_y = None
        self.next_direction_code = None

    def update_direction(self, dx, dy, next_dir):
        self.next_direction_x = dx
        self.next_direction_y = dy
        self.next_direction_code = next_dir


    def update(self, walls, maze):
        # Essayer de bouger dans la nouvelle direction demandée
        if self.next_direction_x is not None:
            old_x, old_y = self.rect.x, self.rect.y
            self.rect.x += self.next_direction_x * BLOCK_SIZE
            self.rect.y += self.next_direction_y * BLOCK_SIZE

            # Vérifier les collisions avec les murs dans la nouvelle direction
            if pygame.sprite.spritecollide(self, walls, False):
                self.rect.x, self.rect.y = old_x, old_y # Revenir en arrière
            else: # Si pas de collision, la nouvelle direction devient la direction actuelle
                self.speed_x = self.next_direction_x
                self.speed_y = self.next_direction_y
                self.current_direction = self.next_direction_code
                self.next_direction_x = None # Réinitialiser la direction demandée
                self.next_direction_y = None
                return # Mouvement effectué

        # Si aucune nouvelle direction n'a été validée, continuer dans la direction actuelle
        old_x, old_y = self.rect.x, self.rect.y
        self.rect.x += self.speed_x * BLOCK_SIZE
        self.rect.y += self.speed_y * BLOCK_SIZE

        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x, self.rect.y = old_x, old_y
            self.speed_x = 0 # Arrêter le mouvement si on touche un mur
            self.speed_y = 0


# --- Classe Ghost ---
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface([BLOCK_SIZE - 6, BLOCK_SIZE - 6])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * BLOCK_SIZE + 3, y * BLOCK_SIZE + 3)
        self.speed_x = random.choice([-1, 1]) # Déplacement initial aléatoire
        self.speed_y = 0
        if self.speed_x != 0: self.speed_y = 0
        else: self.speed_y = random.choice([-1,1])


    def update(self, walls):
        old_x, old_y = self.rect.x, self.rect.y
        self.rect.x += self.speed_x * BLOCK_SIZE
        self.rect.y += self.speed_y * BLOCK_SIZE

        if pygame.sprite.spritecollide(self, walls, False) or \
           self.rect.left < 0 or self.rect.right > SCREEN_WIDTH or \
           self.rect.top < 0 or self.rect.bottom > GAME_AREA_HEIGHT : # Collision ou hors limites
            self.rect.x, self.rect.y = old_x, old_y
            # Changer de direction aléatoirement (IA très basique)
            choices = []
            if self.speed_x != 0: # Si on bougeait horizontalement
                choices.extend([(0, 1), (0, -1)]) # Essayer vertical
            if self.speed_y != 0: # Si on bougeait verticalement
                choices.extend([(1, 0), (-1, 0)]) # Essayer horizontal
            if not choices or random.random() < 0.3: # Si bloqué ou aléatoirement
                 choices = [(0,1), (0,-1), (1,0), (-1,0)]


            new_dir = random.choice(choices)
            self.speed_x, self.speed_y = new_dir[0], new_dir[1]


# --- Classe Wall (Mur) ---
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([BLOCK_SIZE, BLOCK_SIZE])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# --- Classe Pellet (Pac-gomme) ---
class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([BLOCK_SIZE // 4, BLOCK_SIZE // 4])
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, WHITE, (BLOCK_SIZE // 8, BLOCK_SIZE // 8), BLOCK_SIZE // 8)
        self.rect = self.image.get_rect()
        # Centrer la pac-gomme dans la case
        self.rect.center = (x + BLOCK_SIZE // 2, y + BLOCK_SIZE // 2)


# --- Groupes de Sprites ---
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
pellets = pygame.sprite.Group()
ghosts = pygame.sprite.Group()

# --- Création des objets du jeu à partir du layout ---
pacman_start_pos = None
ghost_start_positions = []

for r, row_data in enumerate(maze_layout):
    for c, char in enumerate(row_data):
        if char == '0':
            wall = Wall(c * BLOCK_SIZE, r * BLOCK_SIZE)
            walls.add(wall)
            all_sprites.add(wall)
        elif char == '1': # Passage libre avec une pac-gomme
            pellet = Pellet(c * BLOCK_SIZE, r * BLOCK_SIZE)
            pellets.add(pellet)
            all_sprites.add(pellet)
            if pacman_start_pos is None: # Première case libre pour PacMan
                pacman_start_pos = (c, r)
            elif len(ghost_start_positions) < 1: # Une position pour un fantôme
                 if (r > 3 and r < maze_rows -3) and (c > 3 and c < maze_cols -3): # Eviter bords pour fantome
                    ghost_start_positions.append((c,r))


# --- Création de PacMan et des Fantômes ---
if pacman_start_pos:
    player = PacMan(pacman_start_pos[0], pacman_start_pos[1])
else: # Fallback si aucune position n'est trouvée (ne devrait pas arriver avec ce layout)
    player = PacMan(1, 1)
all_sprites.add(player)

if not ghost_start_positions: ghost_start_positions.append((maze_cols // 2, maze_rows // 2)) # Fallback
ghost1 = Ghost(ghost_start_positions[0][0], ghost_start_positions[0][1], RED)
ghosts.add(ghost1)
all_sprites.add(ghost1)

# --- Variables du jeu ---
score = 0
running = True
game_over_flag = False
win_flag = False

# --- Boucle de jeu principale ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over_flag:
            if event.key == pygame.K_LEFT:
                player.update_direction(-1, 0, "LEFT")
            elif event.key == pygame.K_RIGHT:
                player.update_direction(1, 0, "RIGHT")
            elif event.key == pygame.K_UP:
                player.update_direction(0, -1, "UP")
            elif event.key == pygame.K_DOWN:
                player.update_direction(0, 1, "DOWN")
        elif event.type == pygame.KEYDOWN and game_over_flag:
             if event.key == pygame.K_r: # Permettre de redémarrer
                # Réinitialisation (simplifiée, pour un vrai jeu il faudrait une fonction)
                all_sprites.empty()
                walls.empty()
                pellets.empty()
                ghosts.empty()
                # Recréer les objets
                pacman_start_pos = None
                ghost_start_positions = []
                for r_idx, row_layout in enumerate(maze_layout):
                    for c_idx, char_val in enumerate(row_layout):
                        if char_val == '0':
                            wall = Wall(c_idx * BLOCK_SIZE, r_idx * BLOCK_SIZE)
                            walls.add(wall)
                            all_sprites.add(wall)
                        elif char_val == '1':
                            pellet = Pellet(c_idx * BLOCK_SIZE, r_idx * BLOCK_SIZE)
                            pellets.add(pellet)
                            all_sprites.add(pellet)
                            if pacman_start_pos is None: pacman_start_pos = (c_idx, r_idx)
                            elif len(ghost_start_positions) < 1 and (r_idx > 3 and r_idx < maze_rows -3) and (c_idx > 3 and c_idx < maze_cols -3):
                                ghost_start_positions.append((c_idx,r_idx))

                if pacman_start_pos: player = PacMan(pacman_start_pos[0], pacman_start_pos[1])
                else: player = PacMan(1,1)
                all_sprites.add(player)
                if not ghost_start_positions: ghost_start_positions.append((maze_cols // 2, maze_rows // 2))
                ghost1 = Ghost(ghost_start_positions[0][0], ghost_start_positions[0][1], RED)
                ghosts.add(ghost1)
                all_sprites.add(ghost1)
                score = 0
                game_over_flag = False
                win_flag = False


    if not game_over_flag:
        # --- Logique de mise à jour ---
        player.update(walls, maze_layout) # La grille est passée pour des vérifications futures
        ghosts.update(walls)

        # Collision PacMan avec Pac-gommes
        pellets_hit = pygame.sprite.spritecollide(player, pellets, True) # True pour supprimer la pac-gomme
        for pellet_hit in pellets_hit:
            score += 10
            # print(f"Score: {score}")
            if not pellets: # Si plus de pac-gommes
                win_flag = True
                game_over_flag = True


        # Collision PacMan avec Fantômes
        if pygame.sprite.spritecollide(player, ghosts, False):
            # Pour l'instant, simple game over. Pas de mode "frightened".
            game_over_flag = True
            win_flag = False # On n'a pas gagné si on touche un fantôme

    # --- Dessin ---
    screen.fill(BLACK)

    # Dessiner les murs (déjà dans all_sprites, mais on pourrait les dessiner séparément si besoin)
    # walls.draw(screen)
    # Dessiner les pac-gommes restantes
    pellets.draw(screen)

    # Dessiner PacMan et les Fantômes
    screen.blit(player.image, player.rect)
    for ghost_sprite in ghosts: # Pour dessiner chaque fantôme individuellement
        screen.blit(ghost_sprite.image, ghost_sprite.rect)

    # Dessiner les murs (par dessus les pellets potentiellement)
    walls.draw(screen)


    # Afficher le score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, GAME_AREA_HEIGHT + 10)) # En dessous du labyrinthe

    # Afficher message Game Over ou Victoire
    if game_over_flag:
        if win_flag:
            end_text_str = "VOUS AVEZ GAGNÉ !"
            end_color = GREEN
        else:
            end_text_str = "GAME OVER !"
            end_color = RED
        
        end_text = font.render(end_text_str, True, end_color)
        end_rect = end_text.get_rect(center=(SCREEN_WIDTH / 2, GAME_AREA_HEIGHT + 40))
        screen.blit(end_text, end_rect)
        
        restart_text = font.render("Appuyez sur 'R' pour rejouer", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH / 2, GAME_AREA_HEIGHT + 70))
        screen.blit(restart_text, restart_rect)


    pygame.display.flip() # Mettre à jour l'affichage complet
    clock.tick(FPS)

pygame.quit()