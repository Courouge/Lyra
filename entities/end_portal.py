import pygame
import math
import random
from settings import *

class EndPortal:
    """Portail de fin de niveau"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 80
        self.animation_timer = 0
        self.glow_pulse = 0
        self.particles = []
        
        # Générer des particules de portail
        for _ in range(15):
            self.particles.append({
                'x': x + random.uniform(-30, 30),
                'y': y + random.uniform(-40, 40),
                'vel_x': random.uniform(-0.5, 0.5),
                'vel_y': random.uniform(-1, 1),
                'life': random.randint(60, 120),
                'max_life': 120,
                'size': random.uniform(2, 4)
            })
    
    def update(self):
        """Met à jour l'animation du portail"""
        self.animation_timer += 0.1
        self.glow_pulse += 0.15
        
        # Mettre à jour les particules
        for particle in self.particles[:]:
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                # Régénérer la particule
                particle['x'] = self.x + random.uniform(-30, 30)
                particle['y'] = self.y + random.uniform(-40, 40)
                particle['vel_x'] = random.uniform(-0.5, 0.5)
                particle['vel_y'] = random.uniform(-1, 1)
                particle['life'] = random.randint(60, 120)
    
    def check_collision(self, lyra):
        """Vérifie la collision avec Lyra"""
        return (self.x - self.width//2 < lyra.x < self.x + self.width//2 and
                self.y - self.height//2 < lyra.y < self.y + self.height//2)
    
    def draw(self, screen, camera_x):
        """Dessine le portail de fin"""
        draw_x = self.x - camera_x
        
        if -100 <= draw_x <= SCREEN_WIDTH + 100:
            # Dessiner les particules de fond
            for particle in self.particles:
                part_draw_x = particle['x'] - camera_x
                if 0 <= part_draw_x <= SCREEN_WIDTH:
                    alpha = int((particle['life'] / particle['max_life']) * 200)
                    particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, (255, 255, 255, alpha),
                                     (particle['size'], particle['size']), particle['size'])
                    screen.blit(particle_surface, (part_draw_x - particle['size'], particle['y'] - particle['size']))
            
            # Portail principal avec effet de pulsation
            glow_size = 40 + math.sin(self.glow_pulse) * 10
            
            # Aura externe
            aura_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            for r in range(int(glow_size), 0, -3):
                alpha = 50 * (r / glow_size)
                pygame.draw.circle(aura_surface, (100, 200, 255, int(alpha)),
                                 (glow_size, glow_size), r)
            screen.blit(aura_surface, (draw_x - glow_size, self.y - glow_size))
            
            # Portail central
            portal_color = (150, 220, 255)
            pygame.draw.ellipse(screen, portal_color,
                              (draw_x - self.width//2, self.y - self.height//2,
                               self.width, self.height))
            
            # Anneaux d'énergie
            for i in range(3):
                ring_radius = 25 + i * 8 + math.sin(self.animation_timer + i) * 3
                ring_alpha = 150 - i * 30
                ring_surface = pygame.Surface((ring_radius * 2, ring_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(ring_surface, (200, 240, 255, ring_alpha),
                                 (ring_radius, ring_radius), ring_radius, 2)
                screen.blit(ring_surface, (draw_x - ring_radius, self.y - ring_radius))
            
            # Texte indicatif
            font = pygame.font.Font(None, 24)
            text = font.render("PORTAIL", True, (255, 255, 255))
            text_rect = text.get_rect(center=(draw_x, self.y + 60))
            screen.blit(text, text_rect) 