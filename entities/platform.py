import pygame
import math
from settings import *

class Platform:
    def __init__(self, x, y, width=None, height=None):
        self.x = x
        self.y = y
        self.width = width or PLATFORM_WIDTH
        self.height = height or PLATFORM_HEIGHT
        
        # Effets visuels
        self.glow_offset = 0
        self.crystal_points = self._generate_crystal_points()
        
        # Marqueur pour plateforme de fin
        self.is_end_platform = False
        
    def _generate_crystal_points(self):
        """Génère des points pour donner un aspect cristallin à la plateforme"""
        points = []
        num_points = 6
        for i in range(num_points):
            x_offset = (i / (num_points - 1)) * self.width
            y_offset = math.sin(i * 0.5) * 3  # Légère ondulation
            points.append((x_offset, y_offset))
        return points
        
    def update(self):
        # Animation de lueur
        self.glow_offset += 0.1
        
    def draw(self, screen, camera_x):
        draw_x = self.x - camera_x
        
        # Ne dessiner que si visible à l'écran
        if draw_x + self.width >= 0 and draw_x <= SCREEN_WIDTH:
            # Couleur spéciale pour plateforme de fin
            platform_color = COLORS['star_fragment'] if self.is_end_platform else COLORS['platform']
            
            # Dessiner l'aura de la plateforme
            glow_surface = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
            glow_intensity = 30 + math.sin(self.glow_offset) * 15 if self.is_end_platform else 20 + math.sin(self.glow_offset) * 10
            
            for i in range(3):
                glow_color = (*platform_color, int(glow_intensity - i * 5))
                pygame.draw.rect(glow_surface, glow_color, 
                               (10 - i * 2, 10 - i * 2, self.width + i * 4, self.height + i * 4))
            
            screen.blit(glow_surface, (draw_x - 10, self.y - 10))
            
            # Dessiner la plateforme principale
            pygame.draw.rect(screen, platform_color, 
                           (draw_x, self.y, self.width, self.height))
            
            # Dessiner les détails cristallins
            for i, (point_x, point_y) in enumerate(self.crystal_points):
                crystal_x = draw_x + point_x
                crystal_y = self.y + point_y
                
                # Petits cristaux scintillants
                crystal_color = (
                    min(255, platform_color[0] + 50),
                    min(255, platform_color[1] + 50),
                    min(255, platform_color[2] + 50)
                )
                
                if math.sin(self.glow_offset + i * 0.5) > 0.5:
                    pygame.draw.circle(screen, crystal_color, 
                                     (int(crystal_x), int(crystal_y)), 2)
            
            # Bordure lumineuse
            border_color = (
                min(255, platform_color[0] + 30),
                min(255, platform_color[1] + 30),
                min(255, platform_color[2] + 30)
            )
            pygame.draw.rect(screen, border_color, 
                           (draw_x, self.y, self.width, self.height), 2) 