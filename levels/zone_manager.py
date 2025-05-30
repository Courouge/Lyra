import pygame
import random
from settings import *

class ZoneManager:
    """Gestionnaire des zones/environnements du jeu"""
    
    def __init__(self):
        self.current_zone = 0
        self.zone_transition_timer = 0
        self.zones = [
            {
                'name': "Royaume d'Orion",
                'score_threshold': 0,
                'background_color': (10, 5, 25),
                'platform_color': (80, 60, 120),
                'special_obstacles': [],
                'music': 'orion_theme.ogg',
                'description': "Les jardins stellaires d'Orion vous accueillent..."
            },
            {
                'name': "Nébuleuse de l'Oubli",
                'score_threshold': 1000,
                'background_color': (25, 5, 15),
                'platform_color': (120, 40, 80),
                'special_obstacles': ['void_crystal'],
                'music': 'nebula_theme.ogg',
                'description': "Les brumes pourpres murmurent d'anciens secrets..."
            },
            {
                'name': "Sanctuaire de Vega",
                'score_threshold': 2500,
                'background_color': (5, 15, 30),
                'platform_color': (60, 100, 140),
                'special_obstacles': ['void_crystal', 'time_rift'],
                'music': 'vega_theme.ogg',
                'description': "Les échos du temps résonnent dans le sanctuaire..."
            },
            {
                'name': "Cœur d'Andromède",
                'score_threshold': 5000,
                'background_color': (30, 10, 5),
                'platform_color': (140, 80, 40),
                'special_obstacles': ['void_crystal', 'time_rift', 'stellar_storm'],
                'music': 'andromeda_theme.ogg',
                'description': "Le cœur de la galaxie pulse d'une énergie primordiale..."
            }
        ]
        
    def update(self, score):
        """Met à jour la zone actuelle basée sur le score"""
        new_zone = 0
        for i, zone in enumerate(self.zones):
            if score >= zone['score_threshold']:
                new_zone = i
        
        if new_zone != self.current_zone:
            self.current_zone = new_zone
            self.zone_transition_timer = 180  # 3 secondes de transition
            return True  # Transition déclenchée
        
        if self.zone_transition_timer > 0:
            self.zone_transition_timer -= 1
            
        return False
    
    def get_current_zone(self):
        """Retourne les informations de la zone actuelle"""
        return self.zones[self.current_zone]
    
    def is_transitioning(self):
        """Vérifie si une transition est en cours"""
        return self.zone_transition_timer > 0
    
    def get_transition_alpha(self):
        """Retourne l'alpha pour l'effet de transition"""
        if self.zone_transition_timer > 90:
            return (180 - self.zone_transition_timer) * 2.8  # Fade in
        else:
            return self.zone_transition_timer * 2.8  # Fade out

class VoidCrystal:
    """Cristal du vide - obstacle spécial de la Nébuleuse"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 25
        self.pulse = 0
        self.active = True
        self.energy_rings = []
        
        # Générer des anneaux d'énergie
        for i in range(3):
            self.energy_rings.append({
                'radius': 30 + i * 15,
                'speed': 0.05 + i * 0.02,
                'offset': i * 2
            })
    
    def update(self):
        self.pulse += 0.1
        for ring in self.energy_rings:
            ring['offset'] += ring['speed']
    
    def check_collision(self, lyra):
        distance = ((self.x - lyra.x)**2 + (self.y - lyra.y)**2)**0.5
        return distance < self.size + lyra.radius
    
    def draw(self, screen, camera_x):
        draw_x = self.x - camera_x
        if -50 <= draw_x <= SCREEN_WIDTH + 50:
            # Dessiner les anneaux d'énergie
            for ring in self.energy_rings:
                ring_alpha = 100 + 50 * math.sin(ring['offset'])
                ring_surface = pygame.Surface((ring['radius'] * 2, ring['radius'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(ring_surface, (150, 50, 200, int(ring_alpha)),
                                 (ring['radius'], ring['radius']), ring['radius'], 2)
                screen.blit(ring_surface, (draw_x - ring['radius'], self.y - ring['radius']))
            
            # Cristal central
            crystal_color = (200, 100, 255)
            pulse_size = self.size + math.sin(self.pulse) * 3
            pygame.draw.polygon(screen, crystal_color, [
                (draw_x, self.y - pulse_size),
                (draw_x - pulse_size//2, self.y),
                (draw_x, self.y + pulse_size),
                (draw_x + pulse_size//2, self.y)
            ])

class TimeRift:
    """Faille temporelle - obstacle du Sanctuaire de Vega"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 80
        self.active = True
        self.distortion = 0
        self.particles = []
        
        # Générer des particules temporelles
        for _ in range(10):
            self.particles.append({
                'x': x + random.uniform(-20, 20),
                'y': y + random.uniform(-40, 40),
                'vel_y': random.uniform(-1, 1),
                'life': random.randint(60, 120)
            })
    
    def update(self):
        self.distortion += 0.15
        
        # Mettre à jour les particules
        for particle in self.particles[:]:
            particle['y'] += particle['vel_y']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
                # Régénérer
                self.particles.append({
                    'x': self.x + random.uniform(-20, 20),
                    'y': self.y + random.uniform(-40, 40),
                    'vel_y': random.uniform(-1, 1),
                    'life': random.randint(60, 120)
                })
    
    def check_collision(self, lyra):
        return (self.x - self.width//2 < lyra.x < self.x + self.width//2 and
                self.y - self.height//2 < lyra.y < self.y + self.height//2)
    
    def draw(self, screen, camera_x):
        draw_x = self.x - camera_x
        if -50 <= draw_x <= SCREEN_WIDTH + 50:
            # Effet de distorsion
            distortion_offset = math.sin(self.distortion) * 5
            
            # Faille principale
            rift_color = (100, 200, 255)
            pygame.draw.ellipse(screen, rift_color,
                              (draw_x - self.width//2 + distortion_offset, 
                               self.y - self.height//2,
                               self.width, self.height))
            
            # Particules temporelles
            for particle in self.particles:
                part_draw_x = particle['x'] - camera_x
                alpha = (particle['life'] / 120) * 255
                part_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
                pygame.draw.circle(part_surface, (150, 255, 200, int(alpha)), (2, 2), 2)
                screen.blit(part_surface, (part_draw_x - 2, particle['y'] - 2))

class StellarStorm:
    """Tempête stellaire - obstacle du Cœur d'Andromède"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 60
        self.active = True
        self.rotation = 0
        self.energy_bolts = []
        
        # Générer des éclairs d'énergie
        for i in range(6):
            angle = (i / 6) * 2 * math.pi
            self.energy_bolts.append({
                'angle': angle,
                'length': random.uniform(40, 80),
                'intensity': random.uniform(0.5, 1.0)
            })
    
    def update(self):
        self.rotation += 0.08
        
        # Mettre à jour les éclairs
        for bolt in self.energy_bolts:
            bolt['angle'] += 0.05
            bolt['intensity'] = 0.5 + 0.5 * math.sin(bolt['angle'] * 3)
    
    def check_collision(self, lyra):
        distance = ((self.x - lyra.x)**2 + (self.y - lyra.y)**2)**0.5
        return distance < self.radius
    
    def draw(self, screen, camera_x):
        draw_x = self.x - camera_x
        if -100 <= draw_x <= SCREEN_WIDTH + 100:
            # Cœur de la tempête
            core_color = (255, 150, 50)
            pygame.draw.circle(screen, core_color, (int(draw_x), int(self.y)), 20)
            
            # Éclairs d'énergie
            for bolt in self.energy_bolts:
                end_x = draw_x + math.cos(bolt['angle'] + self.rotation) * bolt['length']
                end_y = self.y + math.sin(bolt['angle'] + self.rotation) * bolt['length']
                
                bolt_color = tuple(int(c * bolt['intensity']) for c in (255, 200, 100))
                pygame.draw.line(screen, bolt_color,
                               (int(draw_x), int(self.y)),
                               (int(end_x), int(end_y)), 3)
            
            # Aura de tempête
            storm_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            for r in range(self.radius, 0, -5):
                alpha = 30 * (r / self.radius)
                pygame.draw.circle(storm_surface, (255, 100, 50, int(alpha)),
                                 (self.radius, self.radius), r)
            screen.blit(storm_surface, (draw_x - self.radius, self.y - self.radius)) 