import pygame
import random
import math
from settings import *

class StarryBackground:
    def __init__(self):
        # Fond simple avec moins d'éléments pour éviter les traînées
        
        # Couche 1 : Étoiles de fond simples
        self.stars = []
        for _ in range(50):  # Réduit de 150 à 50
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH * 2),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.uniform(1, 2),
                'brightness': random.uniform(0.5, 1.0),
                'speed': 0.3
            })
        
        # Couche 2 : Quelques nébuleuses simples
        self.nebulae = []
        for _ in range(10):  # Réduit de 50 à 10
            self.nebulae.append({
                'x': random.randint(0, SCREEN_WIDTH * 2),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.uniform(20, 40),
                'alpha': random.randint(20, 40),
                'speed': 0.1
            })
    
    def update(self, camera_x):
        """Met à jour le fond simplifié"""
        # Mettre à jour les étoiles
        for star in self.stars:
            star['x'] -= star['speed']
            if star['x'] < camera_x - 50:
                star['x'] = camera_x + SCREEN_WIDTH + random.randint(0, 100)
                star['y'] = random.randint(0, SCREEN_HEIGHT)
        
        # Mettre à jour les nébuleuses
        for nebula in self.nebulae:
            nebula['x'] -= nebula['speed']
            if nebula['x'] < camera_x - 100:
                nebula['x'] = camera_x + SCREEN_WIDTH + random.randint(0, 200)
                nebula['y'] = random.randint(0, SCREEN_HEIGHT)
    
    def draw(self, screen, camera_x):
        """Dessine le fond simplifié"""
        # Dessiner les nébuleuses
        for nebula in self.nebulae:
            draw_x = nebula['x'] - camera_x
            if -50 <= draw_x <= SCREEN_WIDTH + 50:
                nebula_surface = pygame.Surface((nebula['size'] * 2, nebula['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(nebula_surface, (100, 50, 150, nebula['alpha']),
                                 (nebula['size'], nebula['size']), nebula['size'])
                screen.blit(nebula_surface, (draw_x - nebula['size'], nebula['y'] - nebula['size']))
        
        # Dessiner les étoiles
        for star in self.stars:
            draw_x = star['x'] - camera_x
            if -10 <= draw_x <= SCREEN_WIDTH + 10:
                star_color = tuple(int(c * star['brightness']) for c in COLORS['star_bg'])
                pygame.draw.circle(screen, star_color, 
                                 (int(draw_x), int(star['y'])), int(star['size'])) 