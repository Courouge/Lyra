import pygame
import math
import random
from settings import *

class StarFragment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = STAR_FRAGMENT_SIZE
        self.collected = False
        
        # Effets visuels
        self.rotation = 0
        self.pulse = 0
        self.float_offset = 0
        self.sparkles = []
        
        # Générer des particules de scintillement
        for _ in range(5):
            self.sparkles.append({
                'angle': random.random() * 2 * math.pi,
                'distance': 20 + random.random() * 10,
                'speed': 0.05 + random.random() * 0.1
            })
    
    def update(self):
        if not self.collected:
            # Rotation et pulsation
            self.rotation += 0.1
            self.pulse += 0.15
            self.float_offset += 0.08
            
            # Mise à jour des particules
            for sparkle in self.sparkles:
                sparkle['angle'] += sparkle['speed']
    
    def collect(self):
        """Marque le fragment comme collecté"""
        self.collected = True
        return 100  # Points gagnés
    
    def check_collision(self, lyra):
        """Vérifie la collision avec Lyra"""
        if self.collected:
            return False
            
        distance = math.sqrt((self.x - lyra.x)**2 + (self.y - lyra.y)**2)
        return distance < (self.size + lyra.radius - 5)
    
    def draw_star(self, surface, center_x, center_y, size, rotation=0):
        """Dessine une étoile à pointes"""
        points = []
        for i in range(STAR_POINTS * 2):
            angle = (i * math.pi / STAR_POINTS) + rotation
            if i % 2 == 0:
                # Pointe externe
                radius = size
            else:
                # Pointe interne
                radius = size * 0.4
                
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            points.append((x, y))
        
        if len(points) >= 3:
            pygame.draw.polygon(surface, COLORS['star_fragment'], points)
    
    def draw(self, screen, camera_x):
        if self.collected:
            return
            
        draw_x = self.x - camera_x
        
        # Ne dessiner que si visible à l'écran
        if draw_x + self.size >= 0 and draw_x - self.size <= SCREEN_WIDTH:
            # Position avec flottement
            float_y = self.y + math.sin(self.float_offset) * 3
            
            # Dessiner l'aura
            pulse_size = self.size + math.sin(self.pulse) * 5
            aura_surface = pygame.Surface((pulse_size * 3, pulse_size * 3), pygame.SRCALPHA)
            
            # Gradient d'aura
            for r in range(int(pulse_size * 1.5), 0, -2):
                alpha = max(0, 40 - (pulse_size * 1.5 - r) * 2)
                aura_color = (*COLORS['star_fragment'], alpha)
                pygame.draw.circle(aura_surface, aura_color, 
                                 (pulse_size * 1.5, pulse_size * 1.5), r)
            
            screen.blit(aura_surface, (draw_x - pulse_size * 1.5, float_y - pulse_size * 1.5))
            
            # Dessiner les particules de scintillement
            for sparkle in self.sparkles:
                sparkle_x = draw_x + math.cos(sparkle['angle']) * sparkle['distance']
                sparkle_y = float_y + math.sin(sparkle['angle']) * sparkle['distance']
                
                if 0 <= sparkle_x <= SCREEN_WIDTH:
                    sparkle_alpha = (math.sin(sparkle['angle'] * 3) + 1) * 0.5
                    if sparkle_alpha > 0.3:
                        pygame.draw.circle(screen, (255, 255, 255), 
                                         (int(sparkle_x), int(sparkle_y)), 1)
            
            # Dessiner l'étoile principale
            self.draw_star(screen, draw_x, float_y, self.size, self.rotation)
            
            # Dessiner une étoile plus petite au centre pour l'effet de profondeur
            center_color = (255, 255, 255)
            self.draw_star(screen, draw_x, float_y, self.size * 0.6, -self.rotation * 0.5)
            
            # Point central brillant
            pygame.draw.circle(screen, center_color, (int(draw_x), int(float_y)), 2) 