import random
import math
from settings import *
from entities.platform import Platform
from entities.star_fragment import StarFragment
from entities.shadow import Shadow

class Level2Generator:
    """Générateur pour le niveau 2 avec des mécaniques avancées"""
    
    def __init__(self):
        self.platforms = []
        self.star_fragments = []
        self.shadows = []
        self.moving_platforms = []
        self.gravity_wells = []
        self.checkpoints = []
        
        self.last_platform_x = 0
        self.last_platform_y = SCREEN_HEIGHT // 2
        self.difficulty = 2.0  # Niveau 2 plus difficile
        self.checkpoint_distance = 1000  # Distance entre checkpoints
        self.last_checkpoint = 0
        
        # Générer la plateforme de départ
        start_platform = Platform(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH // 2, 30)
        self.platforms.append(start_platform)
        self.last_platform_x = start_platform.x + start_platform.width
        self.last_platform_y = start_platform.y
        
    def generate_moving_platform(self, x, y):
        """Génère une plateforme mobile"""
        platform = MovingPlatform(x, y)
        self.moving_platforms.append(platform)
        return platform
        
    def generate_gravity_well(self, x, y):
        """Génère un puits de gravité"""
        well = GravityWell(x, y)
        self.gravity_wells.append(well)
        
    def generate_checkpoint(self, x):
        """Génère un checkpoint"""
        checkpoint = Checkpoint(x, SCREEN_HEIGHT // 2)
        self.checkpoints.append(checkpoint)
        
    def generate_advanced_chunk(self, camera_x):
        """Génère un chunk avec des mécaniques avancées"""
        chunk_start = camera_x + SCREEN_WIDTH
        chunk_end = chunk_start + SCREEN_WIDTH
        
        # Nettoyer les éléments hors de l'écran
        self.cleanup_offscreen_elements(camera_x)
        
        # Générer des plateformes normales et mobiles
        while self.last_platform_x < chunk_end:
            if random.random() < 0.3:  # 30% de chance de plateforme mobile
                self.generate_moving_platform(self.last_platform_x + 200, self.last_platform_y)
            else:
                self.generate_next_platform()
                
        # Générer des puits de gravité
        if random.random() < 0.2:
            well_x = random.randint(int(chunk_start), int(chunk_end))
            well_y = random.randint(200, SCREEN_HEIGHT - 200)
            self.generate_gravity_well(well_x, well_y)
            
        # Générer des checkpoints
        if camera_x - self.last_checkpoint > self.checkpoint_distance:
            self.generate_checkpoint(camera_x + SCREEN_WIDTH // 2)
            self.last_checkpoint = camera_x
            
        # Générer plus d'ombres et de fragments
        self.generate_star_fragments(chunk_start, chunk_end)
        self.generate_advanced_shadows(chunk_start, chunk_end)
        
    def generate_advanced_shadows(self, chunk_start, chunk_end):
        """Génère des ombres plus agressives pour le niveau 2"""
        num_shadows = int(self.difficulty * 3)  # Plus d'ombres
        
        for _ in range(num_shadows):
            if random.random() < SHADOW_SPAWN_CHANCE * 1.5:
                shadow_x = random.randint(int(chunk_start), int(chunk_end))
                shadow_y = random.randint(100, SCREEN_HEIGHT - 100)
                
                # Ombres qui suivent le joueur
                if random.random() < 0.3:
                    shadow = TrackingShadow(shadow_x, shadow_y)
                else:
                    shadow = Shadow(shadow_x, shadow_y)
                    
                self.shadows.append(shadow)

class MovingPlatform(Platform):
    """Plateforme qui bouge verticalement"""
    
    def __init__(self, x, y, width=None, height=None):
        super().__init__(x, y, width, height)
        self.start_y = y
        self.move_range = 100
        self.move_speed = 0.02
        self.move_offset = 0
        
    def update(self):
        super().update()
        self.move_offset += self.move_speed
        self.y = self.start_y + math.sin(self.move_offset) * self.move_range

class GravityWell:
    """Puits de gravité qui attire Lyra"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 80
        self.strength = 0.3
        self.pulse = 0
        
    def update(self):
        self.pulse += 0.1
        
    def apply_force(self, lyra):
        """Applique une force d'attraction sur Lyra"""
        distance = math.sqrt((self.x - lyra.x)**2 + (self.y - lyra.y)**2)
        
        if distance < self.radius and distance > 0:
            # Force d'attraction inversement proportionnelle à la distance
            force = self.strength * (1 - distance / self.radius)
            
            # Direction vers le puits
            dx = (self.x - lyra.x) / distance
            dy = (self.y - lyra.y) / distance
            
            # Appliquer la force
            lyra.vel_x += dx * force
            lyra.vel_y += dy * force
            
    def draw(self, screen, camera_x):
        draw_x = self.x - camera_x
        
        if -self.radius <= draw_x <= SCREEN_WIDTH + self.radius:
            # Dessiner l'effet de puits de gravité
            pulse_radius = self.radius + math.sin(self.pulse) * 10
            
            # Anneaux concentriques
            for i in range(3):
                ring_radius = pulse_radius - i * 20
                if ring_radius > 0:
                    alpha = 50 - i * 15
                    well_surface = pygame.Surface((ring_radius * 2, ring_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(well_surface, (100, 0, 200, alpha), 
                                     (ring_radius, ring_radius), ring_radius, 3)
                    screen.blit(well_surface, (draw_x - ring_radius, self.y - ring_radius))

class TrackingShadow(Shadow):
    """Ombre qui suit le joueur"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.tracking_speed = 0.5
        
    def update(self, lyra_x=None, lyra_y=None):
        super().update()
        
        if lyra_x is not None and lyra_y is not None:
            # Se diriger vers Lyra
            dx = lyra_x - self.x
            dy = lyra_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 0:
                self.x += (dx / distance) * self.tracking_speed
                self.y += (dy / distance) * self.tracking_speed

class Checkpoint:
    """Point de sauvegarde"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.activated = False
        self.pulse = 0
        self.particles = []
        
        # Générer des particules
        for _ in range(20):
            self.particles.append({
                'angle': random.random() * 2 * math.pi,
                'distance': random.uniform(30, 60),
                'speed': random.uniform(0.02, 0.05)
            })
            
    def update(self):
        self.pulse += 0.1
        
        for particle in self.particles:
            particle['angle'] += particle['speed']
            
    def activate(self):
        """Active le checkpoint"""
        self.activated = True
        
    def check_collision(self, lyra):
        """Vérifie si Lyra touche le checkpoint"""
        distance = math.sqrt((self.x - lyra.x)**2 + (self.y - lyra.y)**2)
        return distance < 40
        
    def draw(self, screen, camera_x):
        draw_x = self.x - camera_x
        
        if -100 <= draw_x <= SCREEN_WIDTH + 100:
            # Couleur selon l'état
            color = COLORS['star_fragment'] if self.activated else COLORS['lyra_glow']
            
            # Dessiner les particules
            for particle in self.particles:
                part_x = draw_x + math.cos(particle['angle']) * particle['distance']
                part_y = self.y + math.sin(particle['angle']) * particle['distance']
                
                if 0 <= part_x <= SCREEN_WIDTH:
                    pygame.draw.circle(screen, color, (int(part_x), int(part_y)), 2)
            
            # Dessiner le checkpoint principal
            pulse_size = 30 + math.sin(self.pulse) * 5
            pygame.draw.circle(screen, color, (int(draw_x), int(self.y)), int(pulse_size), 3)
            
            # Centre
            pygame.draw.circle(screen, color, (int(draw_x), int(self.y)), 10) 