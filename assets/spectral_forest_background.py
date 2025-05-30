import pygame
import math
import random
from settings import *

class SpectralForestBackground:
    """Fond spécialisé pour la Forêt Spectrale"""
    
    def __init__(self):
        # Couches de parallaxe
        self.distant_trees = []
        self.mist_layers = []
        self.fireflies = []
        self.aurora_particles = []
        
        # Générer les éléments de fond
        self.generate_distant_trees()
        self.generate_mist_layers()
        self.generate_fireflies()
        self.generate_aurora_particles()
        
        # Animation
        self.time_offset = 0
        self.mist_flow = 0
        
    def generate_distant_trees(self):
        """Génère des arbres distants pour la parallaxe"""
        for i in range(15):
            tree = {
                'x': i * 200 + random.randint(-50, 50),
                'y': SCREEN_HEIGHT - random.randint(150, 300),
                'height': random.randint(100, 200),
                'width': random.randint(15, 30),
                'sway_offset': random.random() * 2 * math.pi,
                'sway_speed': random.uniform(0.005, 0.015),
                'transparency': random.randint(20, 60)
            }
            self.distant_trees.append(tree)
    
    def generate_mist_layers(self):
        """Génère des couches de brume"""
        for i in range(3):
            layer = {
                'y': SCREEN_HEIGHT // 3 + i * 100,
                'thickness': random.randint(40, 80),
                'speed': random.uniform(0.2, 0.8),
                'opacity': random.randint(15, 35),
                'wave_offset': random.random() * 2 * math.pi
            }
            self.mist_layers.append(layer)
    
    def generate_fireflies(self):
        """Génère des lucioles mystiques"""
        for i in range(25):
            firefly = {
                'x': random.randint(0, SCREEN_WIDTH * 3),
                'y': random.randint(100, SCREEN_HEIGHT - 100),
                'start_x': 0,
                'start_y': 0,
                'orbit_radius': random.randint(30, 80),
                'orbit_speed': random.uniform(0.01, 0.03),
                'orbit_offset': random.random() * 2 * math.pi,
                'pulse_offset': random.random() * 2 * math.pi,
                'pulse_speed': random.uniform(0.05, 0.1),
                'size': random.randint(2, 5),
                'color_shift': random.random() * 2 * math.pi
            }
            firefly['start_x'] = firefly['x']
            firefly['start_y'] = firefly['y']
            self.fireflies.append(firefly)
    
    def generate_aurora_particles(self):
        """Génère des particules d'aurore mystique"""
        for i in range(40):
            particle = {
                'x': random.randint(0, SCREEN_WIDTH * 2),
                'y': random.randint(0, SCREEN_HEIGHT // 2),
                'drift_speed': random.uniform(0.1, 0.5),
                'float_range': random.randint(20, 50),
                'float_speed': random.uniform(0.01, 0.03),
                'float_offset': random.random() * 2 * math.pi,
                'start_y': 0,
                'size': random.randint(1, 3),
                'transparency': random.randint(30, 80)
            }
            particle['start_y'] = particle['y']
            self.aurora_particles.append(particle)
    
    def update(self, camera_x):
        """Met à jour l'animation du fond"""
        self.time_offset += 0.02
        self.mist_flow += 0.5
        
        # Mettre à jour les arbres distants
        for tree in self.distant_trees:
            tree['sway_offset'] += tree['sway_speed']
        
        # Mettre à jour les lucioles
        for firefly in self.fireflies:
            firefly['orbit_offset'] += firefly['orbit_speed']
            firefly['pulse_offset'] += firefly['pulse_speed']
            firefly['color_shift'] += 0.02
            
            # Mouvement orbital
            firefly['x'] = firefly['start_x'] + math.cos(firefly['orbit_offset']) * firefly['orbit_radius']
            firefly['y'] = firefly['start_y'] + math.sin(firefly['orbit_offset']) * firefly['orbit_radius'] * 0.5
        
        # Mettre à jour les particules d'aurore
        for particle in self.aurora_particles:
            particle['x'] -= particle['drift_speed']
            particle['float_offset'] += particle['float_speed']
            particle['y'] = particle['start_y'] + math.sin(particle['float_offset']) * particle['float_range']
            
            # Recycler les particules qui sortent de l'écran
            if particle['x'] < -50:
                particle['x'] = SCREEN_WIDTH + 50
                particle['y'] = random.randint(0, SCREEN_HEIGHT // 2)
                particle['start_y'] = particle['y']
    
    def draw(self, screen, camera_x):
        """Dessine le fond de forêt spectrale"""
        # Fond de base avec gradient mystique
        self.draw_base_gradient(screen)
        
        # Particules d'aurore en arrière-plan
        self.draw_aurora_particles(screen, camera_x)
        
        # Arbres distants avec parallaxe
        self.draw_distant_trees(screen, camera_x)
        
        # Couches de brume
        self.draw_mist_layers(screen, camera_x)
        
        # Lucioles mystiques
        self.draw_fireflies(screen, camera_x)
        
        # Effet de lumière ambiante
        self.draw_ambient_light(screen)
    
    def draw_base_gradient(self, screen):
        """Dessine le gradient de base"""
        for y in range(0, SCREEN_HEIGHT, 2):
            # Gradient du noir-vert vers le vert mystique
            progress = y / SCREEN_HEIGHT
            
            # Couleurs de base
            r = int(5 + progress * 15)
            g = int(15 + progress * 35)
            b = int(10 + progress * 20)
            
            # Variation temporelle
            r += int(math.sin(self.time_offset + progress) * 3)
            g += int(math.sin(self.time_offset * 1.2 + progress) * 8)
            b += int(math.sin(self.time_offset * 0.8 + progress) * 5)
            
            # Limiter les valeurs
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            pygame.draw.rect(screen, (r, g, b), (0, y, SCREEN_WIDTH, 2))
    
    def draw_aurora_particles(self, screen, camera_x):
        """Dessine les particules d'aurore"""
        for particle in self.aurora_particles:
            draw_x = particle['x'] - camera_x * 0.1  # Parallaxe lente
            
            if -10 <= draw_x <= SCREEN_WIDTH + 10:
                # Couleur changeante
                color_r = 80 + int(math.sin(self.time_offset + particle['x'] * 0.01) * 40)
                color_g = 200 + int(math.sin(self.time_offset * 1.3 + particle['x'] * 0.01) * 55)
                color_b = 120 + int(math.sin(self.time_offset * 0.7 + particle['x'] * 0.01) * 30)
                
                # Dessiner avec transparence
                particle_surface = pygame.Surface((particle['size'] * 4, particle['size'] * 4), pygame.SRCALPHA)
                particle_color = (color_r, color_g, color_b, particle['transparency'])
                pygame.draw.circle(particle_surface, particle_color, 
                                 (particle['size'] * 2, particle['size'] * 2), particle['size'])
                screen.blit(particle_surface, (draw_x - particle['size'] * 2, particle['y'] - particle['size'] * 2))
    
    def draw_distant_trees(self, screen, camera_x):
        """Dessine les arbres distants"""
        for tree in self.distant_trees:
            draw_x = tree['x'] - camera_x * 0.3  # Parallaxe moyenne
            
            if draw_x + tree['width'] >= 0 and draw_x <= SCREEN_WIDTH:
                # Balancement
                sway = math.sin(tree['sway_offset']) * 3
                
                # Surface avec transparence
                tree_surface = pygame.Surface((tree['width'], tree['height']), pygame.SRCALPHA)
                tree_color = (30, 60, 40, tree['transparency'])
                
                # Tronc
                pygame.draw.rect(tree_surface, tree_color, (0, 0, tree['width'], tree['height']))
                
                # Feuillage
                foliage_size = tree['width'] * 1.5
                foliage_surface = pygame.Surface((foliage_size, foliage_size), pygame.SRCALPHA)
                foliage_color = (50, 100, 60, tree['transparency'] // 2)
                pygame.draw.circle(foliage_surface, foliage_color, 
                                 (int(foliage_size // 2), int(foliage_size // 2)), int(foliage_size // 2))
                
                # Dessiner
                screen.blit(tree_surface, (draw_x + sway, tree['y']))
                screen.blit(foliage_surface, (draw_x - foliage_size // 4 + sway, 
                                            tree['y'] - foliage_size // 2))
    
    def draw_mist_layers(self, screen, camera_x):
        """Dessine les couches de brume"""
        for i, layer in enumerate(self.mist_layers):
            # Mouvement de la brume
            mist_x = (self.mist_flow * layer['speed']) % (SCREEN_WIDTH + 200)
            
            # Créer la surface de brume
            mist_surface = pygame.Surface((SCREEN_WIDTH + 200, layer['thickness']), pygame.SRCALPHA)
            
            # Forme ondulée
            for x in range(0, SCREEN_WIDTH + 200, 4):
                wave_height = math.sin((x + layer['wave_offset']) * 0.01) * 10
                mist_y = layer['y'] + wave_height
                mist_alpha = layer['opacity'] + int(math.sin(x * 0.02 + self.time_offset) * 10)
                mist_color = (100, 200, 150, max(0, mist_alpha))
                
                pygame.draw.rect(mist_surface, mist_color, (x, 0, 4, layer['thickness']))
            
            screen.blit(mist_surface, (-mist_x, layer['y']))
    
    def draw_fireflies(self, screen, camera_x):
        """Dessine les lucioles mystiques"""
        for firefly in self.fireflies:
            draw_x = firefly['x'] - camera_x * 0.7  # Parallaxe rapide
            
            if -20 <= draw_x <= SCREEN_WIDTH + 20:
                # Pulsation
                pulse = math.sin(firefly['pulse_offset']) * 0.5 + 0.5
                size = firefly['size'] + int(pulse * 3)
                
                # Couleur changeante
                color_r = 150 + int(math.sin(firefly['color_shift']) * 50)
                color_g = 255
                color_b = 180 + int(math.cos(firefly['color_shift']) * 40)
                alpha = int(100 + pulse * 100)
                
                # Aura
                aura_size = size * 3
                aura_surface = pygame.Surface((aura_size * 2, aura_size * 2), pygame.SRCALPHA)
                aura_color = (color_r, color_g, color_b, alpha // 3)
                pygame.draw.circle(aura_surface, aura_color, (aura_size, aura_size), aura_size)
                screen.blit(aura_surface, (draw_x - aura_size, firefly['y'] - aura_size))
                
                # Luciole centrale
                pygame.draw.circle(screen, (color_r, color_g, color_b), 
                                 (int(draw_x), int(firefly['y'])), size)
                pygame.draw.circle(screen, (255, 255, 255), 
                                 (int(draw_x), int(firefly['y'])), max(1, size // 2))
    
    def draw_ambient_light(self, screen):
        """Dessine l'éclairage ambiant"""
        # Effet de lumière douce en haut
        light_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT // 3), pygame.SRCALPHA)
        
        for y in range(SCREEN_HEIGHT // 3):
            alpha = int(20 * (1 - y / (SCREEN_HEIGHT // 3)))
            light_color = (120, 255, 180, alpha)
            pygame.draw.rect(light_surface, light_color, (0, y, SCREEN_WIDTH, 1))
        
        screen.blit(light_surface, (0, 0))
        
        # Rayons de lumière mystique
        for i in range(5):
            ray_x = (i * SCREEN_WIDTH // 5) + int(math.sin(self.time_offset + i) * 50)
            ray_width = 20 + int(math.sin(self.time_offset * 1.5 + i) * 10)
            ray_alpha = 15 + int(math.sin(self.time_offset * 2 + i) * 10)
            
            ray_surface = pygame.Surface((ray_width, SCREEN_HEIGHT), pygame.SRCALPHA)
            ray_color = (120, 255, 180, ray_alpha)
            ray_surface.fill(ray_color)
            screen.blit(ray_surface, (ray_x, 0)) 