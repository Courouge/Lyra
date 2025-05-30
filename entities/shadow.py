import pygame
import math
import random
from settings import *

class Shadow:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = SHADOW_SIZE
        self.active = True
        
        # Mouvement et comportement
        self.vel_y = random.uniform(-1, 1)
        self.float_speed = random.uniform(0.02, 0.05)
        self.float_offset = random.uniform(0, 2 * math.pi)
        
        # Effets visuels
        self.pulse = 0
        self.tentacles = []
        self.darkness_radius = self.size * 2
        
        # Générer des tentacules d'ombre
        num_tentacles = random.randint(4, 7)
        for i in range(num_tentacles):
            self.tentacles.append({
                'angle': (i / num_tentacles) * 2 * math.pi,
                'length': random.uniform(15, 25),
                'speed': random.uniform(0.03, 0.08),
                'thickness': random.uniform(2, 5)
            })
    
    def update(self):
        if not self.active:
            return
            
        # Mouvement flottant
        self.y += self.vel_y
        self.float_offset += self.float_speed
        
        # Pulsation sinistre
        self.pulse += 0.1
        
        # Mise à jour des tentacules
        for tentacle in self.tentacles:
            tentacle['angle'] += tentacle['speed']
            tentacle['length'] += math.sin(tentacle['angle'] * 3) * 0.5
    
    def check_collision(self, lyra):
        """Vérifie la collision avec Lyra"""
        if not self.active or lyra.invincible:
            return False
            
        distance = math.sqrt((self.x - lyra.x)**2 + (self.y - lyra.y)**2)
        return distance < (self.size + lyra.radius - 5)
    
    def destroy(self):
        """Détruit l'ombre"""
        self.active = False
    
    def draw_tentacle(self, screen, start_x, start_y, angle, length, thickness, camera_x):
        """Dessine un tentacule d'ombre"""
        end_x = start_x + math.cos(angle) * length
        end_y = start_y + math.sin(angle) * length
        
        # Convertir en coordonnées écran
        screen_start_x = start_x - camera_x
        screen_end_x = end_x - camera_x
        
        if -50 <= screen_start_x <= SCREEN_WIDTH + 50 or -50 <= screen_end_x <= SCREEN_WIDTH + 50:
            # Dessiner le tentacule avec un dégradé
            segments = 5
            for i in range(segments):
                t = i / segments
                seg_x = start_x + (end_x - start_x) * t - camera_x
                seg_y = start_y + (end_y - start_y) * t
                
                # Épaisseur qui diminue vers l'extrémité
                seg_thickness = thickness * (1 - t * 0.7)
                
                # Couleur qui s'estompe
                alpha = int(100 * (1 - t * 0.5))
                shadow_color = (*COLORS['shadow'], alpha)
                
                if seg_thickness > 0:
                    # Créer une surface avec alpha pour le tentacule
                    tent_surface = pygame.Surface((seg_thickness * 2, seg_thickness * 2), pygame.SRCALPHA)
                    pygame.draw.circle(tent_surface, shadow_color, 
                                     (seg_thickness, seg_thickness), seg_thickness)
                    screen.blit(tent_surface, (seg_x - seg_thickness, seg_y - seg_thickness))
    
    def draw(self, screen, camera_x):
        if not self.active:
            return
            
        draw_x = self.x - camera_x
        
        # Ne dessiner que si visible à l'écran
        if draw_x + self.darkness_radius >= 0 and draw_x - self.darkness_radius <= SCREEN_WIDTH:
            # Position avec flottement
            float_y = self.y + math.sin(self.float_offset) * 8
            
            # Dessiner l'aura de ténèbres
            darkness_size = self.darkness_radius + math.sin(self.pulse) * 5
            darkness_surface = pygame.Surface((darkness_size * 2, darkness_size * 2), pygame.SRCALPHA)
            
            # Gradient de ténèbres
            for r in range(int(darkness_size), 0, -3):
                alpha = max(0, 60 - (darkness_size - r) * 1.5)
                darkness_color = (*COLORS['shadow'], int(alpha))
                pygame.draw.circle(darkness_surface, darkness_color, 
                                 (darkness_size, darkness_size), r)
            
            screen.blit(darkness_surface, (draw_x - darkness_size, float_y - darkness_size))
            
            # Dessiner les tentacules
            for tentacle in self.tentacles:
                self.draw_tentacle(screen, self.x, float_y, 
                                 tentacle['angle'], tentacle['length'], 
                                 tentacle['thickness'], camera_x)
            
            # Dessiner le corps principal de l'ombre
            shadow_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            
            # Corps principal avec effet de flou
            for i in range(3):
                shadow_alpha = 120 - i * 30
                shadow_radius = self.size - i * 2
                if shadow_radius > 0:
                    pygame.draw.circle(shadow_surface, (*COLORS['shadow'], shadow_alpha), 
                                     (self.size, self.size), shadow_radius)
            
            screen.blit(shadow_surface, (draw_x - self.size, float_y - self.size))
            
            # Yeux sinistres (points rouges)
            eye_color = (150, 0, 50)
            eye_glow = math.sin(self.pulse * 2) * 0.3 + 0.7
            
            eye1_x = draw_x - 6
            eye1_y = float_y - 4
            eye2_x = draw_x + 6
            eye2_y = float_y - 4
            
            pygame.draw.circle(screen, eye_color, (int(eye1_x), int(eye1_y)), 
                             int(3 * eye_glow))
            pygame.draw.circle(screen, eye_color, (int(eye2_x), int(eye2_y)), 
                             int(3 * eye_glow)) 