import pygame
import math
import random
from settings import *

class CelestialMirrorsBackground:
    """Fond spécialisé pour les Miroirs Célestes"""
    
    def __init__(self):
        # Couches de parallaxe
        self.crystal_formations = []
        self.mirror_shards = []
        self.portal_rifts = []
        self.cosmic_dust = []
        self.gravity_waves = []
        
        # Générer les éléments de fond
        self.generate_crystal_formations()
        self.generate_mirror_shards()
        self.generate_portal_rifts()
        self.generate_cosmic_dust()
        self.generate_gravity_waves()
        
        # Animation
        self.time_offset = 0
        self.portal_pulse = 0
        
    def generate_crystal_formations(self):
        """Génère des formations cristallines distantes"""
        for i in range(12):
            crystal = {
                'x': i * 250 + random.randint(-80, 80),
                'y': SCREEN_HEIGHT - random.randint(200, 400),
                'height': random.randint(150, 300),
                'width': random.randint(30, 60),
                'facets': random.randint(4, 8),
                'rotation': random.random() * 2 * math.pi,
                'rotation_speed': random.uniform(0.002, 0.008),
                'transparency': random.randint(30, 70),
                'color_shift': random.random() * 2 * math.pi
            }
            self.crystal_formations.append(crystal)
    
    def generate_mirror_shards(self):
        """Génère des éclats de miroir flottants"""
        for i in range(30):
            shard = {
                'x': random.randint(0, SCREEN_WIDTH * 4),
                'y': random.randint(50, SCREEN_HEIGHT - 50),
                'size': random.randint(5, 15),
                'rotation': random.random() * 2 * math.pi,
                'rotation_speed': random.uniform(0.01, 0.05),
                'drift_speed': random.uniform(0.1, 0.4),
                'float_range': random.randint(15, 30),
                'float_speed': random.uniform(0.008, 0.02),
                'float_offset': random.random() * 2 * math.pi,
                'start_y': 0,
                'reflection_intensity': random.uniform(0.3, 0.8)
            }
            shard['start_y'] = shard['y']
            self.mirror_shards.append(shard)
    
    def generate_portal_rifts(self):
        """Génère des failles portails en arrière-plan"""
        for i in range(5):
            rift = {
                'x': i * 400 + random.randint(-100, 100),
                'y': random.randint(100, SCREEN_HEIGHT - 200),
                'width': random.randint(80, 150),
                'height': random.randint(200, 350),
                'pulse_offset': random.random() * 2 * math.pi,
                'pulse_speed': random.uniform(0.02, 0.05),
                'distortion_offset': random.random() * 2 * math.pi,
                'energy_color': random.choice([(180, 120, 255), (120, 180, 255), (255, 120, 180)])
            }
            self.portal_rifts.append(rift)
    
    def generate_cosmic_dust(self):
        """Génère de la poussière cosmique"""
        for i in range(60):
            dust = {
                'x': random.randint(0, SCREEN_WIDTH * 3),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(1, 4),
                'drift_speed': random.uniform(0.05, 0.3),
                'twinkle_offset': random.random() * 2 * math.pi,
                'twinkle_speed': random.uniform(0.03, 0.08),
                'transparency': random.randint(40, 120)
            }
            self.cosmic_dust.append(dust)
    
    def generate_gravity_waves(self):
        """Génère des ondes de gravité visibles"""
        for i in range(4):
            wave = {
                'center_x': i * 500 + random.randint(-150, 150),
                'center_y': random.randint(200, SCREEN_HEIGHT - 200),
                'radius': 0,
                'max_radius': random.randint(200, 400),
                'speed': random.uniform(0.5, 1.2),
                'thickness': random.randint(3, 8),
                'reset_timer': 0,
                'reset_interval': random.randint(300, 600)
            }
            self.gravity_waves.append(wave)
    
    def update(self, camera_x):
        """Met à jour l'animation du fond"""
        self.time_offset += 0.015
        self.portal_pulse += 0.03
        
        # Mettre à jour les cristaux
        for crystal in self.crystal_formations:
            crystal['rotation'] += crystal['rotation_speed']
            crystal['color_shift'] += 0.01
        
        # Mettre à jour les éclats de miroir
        for shard in self.mirror_shards:
            shard['x'] -= shard['drift_speed']
            shard['rotation'] += shard['rotation_speed']
            shard['float_offset'] += shard['float_speed']
            shard['y'] = shard['start_y'] + math.sin(shard['float_offset']) * shard['float_range']
            
            # Recycler les éclats qui sortent de l'écran
            if shard['x'] < -50:
                shard['x'] = SCREEN_WIDTH + 50
                shard['y'] = random.randint(50, SCREEN_HEIGHT - 50)
                shard['start_y'] = shard['y']
        
        # Mettre à jour les failles portails
        for rift in self.portal_rifts:
            rift['pulse_offset'] += rift['pulse_speed']
            rift['distortion_offset'] += 0.02
        
        # Mettre à jour la poussière cosmique
        for dust in self.cosmic_dust:
            dust['x'] -= dust['drift_speed']
            dust['twinkle_offset'] += dust['twinkle_speed']
            
            if dust['x'] < -10:
                dust['x'] = SCREEN_WIDTH + 10
                dust['y'] = random.randint(0, SCREEN_HEIGHT)
        
        # Mettre à jour les ondes de gravité
        for wave in self.gravity_waves:
            wave['radius'] += wave['speed']
            wave['reset_timer'] += 1
            
            if wave['radius'] > wave['max_radius'] or wave['reset_timer'] > wave['reset_interval']:
                wave['radius'] = 0
                wave['reset_timer'] = 0
                wave['center_x'] = random.randint(-200, SCREEN_WIDTH + 200)
                wave['center_y'] = random.randint(100, SCREEN_HEIGHT - 100)
    
    def draw(self, screen, camera_x):
        """Dessine le fond des miroirs célestes"""
        # Fond de base avec gradient cristallin
        self.draw_base_gradient(screen)
        
        # Ondes de gravité en arrière-plan
        self.draw_gravity_waves(screen, camera_x)
        
        # Formations cristallines distantes
        self.draw_crystal_formations(screen, camera_x)
        
        # Failles portails
        self.draw_portal_rifts(screen, camera_x)
        
        # Poussière cosmique
        self.draw_cosmic_dust(screen, camera_x)
        
        # Éclats de miroir
        self.draw_mirror_shards(screen, camera_x)
        
        # Effet de réfraction
        self.draw_refraction_effect(screen)
    
    def draw_base_gradient(self, screen):
        """Dessine le gradient de base cristallin"""
        for y in range(0, SCREEN_HEIGHT, 3):
            # Gradient du violet sombre vers le bleu cristallin
            progress = y / SCREEN_HEIGHT
            
            # Couleurs de base
            r = int(15 + progress * 25)
            g = int(5 + progress * 20)
            b = int(30 + progress * 40)
            
            # Variation temporelle cristalline
            r += int(math.sin(self.time_offset + progress * 2) * 8)
            g += int(math.sin(self.time_offset * 1.3 + progress * 2) * 6)
            b += int(math.sin(self.time_offset * 0.7 + progress * 2) * 12)
            
            # Limiter les valeurs
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            
            pygame.draw.rect(screen, (r, g, b), (0, y, SCREEN_WIDTH, 3))
    
    def draw_gravity_waves(self, screen, camera_x):
        """Dessine les ondes de gravité"""
        for wave in self.gravity_waves:
            if wave['radius'] > 0:
                draw_x = wave['center_x'] - camera_x * 0.2
                
                if -wave['max_radius'] <= draw_x <= SCREEN_WIDTH + wave['max_radius']:
                    # Onde principale
                    wave_alpha = int(60 * (1 - wave['radius'] / wave['max_radius']))
                    if wave_alpha > 0:
                        wave_surface = pygame.Surface((wave['radius'] * 2, wave['radius'] * 2), pygame.SRCALPHA)
                        wave_color = (180, 120, 255, wave_alpha)
                        pygame.draw.circle(wave_surface, wave_color, 
                                         (int(wave['radius']), int(wave['radius'])), 
                                         int(wave['radius']), wave['thickness'])
                        screen.blit(wave_surface, (draw_x - wave['radius'], wave['center_y'] - wave['radius']))
    
    def draw_crystal_formations(self, screen, camera_x):
        """Dessine les formations cristallines"""
        for crystal in self.crystal_formations:
            draw_x = crystal['x'] - camera_x * 0.4  # Parallaxe moyenne
            
            if draw_x + crystal['width'] >= 0 and draw_x <= SCREEN_WIDTH:
                # Couleur changeante
                color_r = 120 + int(math.sin(crystal['color_shift']) * 60)
                color_g = 80 + int(math.sin(crystal['color_shift'] * 1.3) * 40)
                color_b = 140 + int(math.sin(crystal['color_shift'] * 0.7) * 80)
                
                # Surface avec transparence
                crystal_surface = pygame.Surface((crystal['width'], crystal['height']), pygame.SRCALPHA)
                crystal_color = (color_r, color_g, color_b, crystal['transparency'])
                
                # Forme cristalline (polygone)
                points = []
                for i in range(crystal['facets']):
                    angle = (i / crystal['facets']) * 2 * math.pi + crystal['rotation']
                    x = crystal['width'] // 2 + math.cos(angle) * (crystal['width'] // 3)
                    y = crystal['height'] // 2 + math.sin(angle) * (crystal['height'] // 3)
                    points.append((x, y))
                
                pygame.draw.polygon(crystal_surface, crystal_color, points)
                
                # Reflets cristallins
                for i in range(3):
                    highlight_color = (255, 255, 255, 30 - i * 8)
                    highlight_points = []
                    for point in points[:len(points)//2]:
                        highlight_points.append((point[0] + i, point[1] + i))
                    if len(highlight_points) >= 3:
                        pygame.draw.polygon(crystal_surface, highlight_color, highlight_points)
                
                screen.blit(crystal_surface, (draw_x, crystal['y']))
    
    def draw_portal_rifts(self, screen, camera_x):
        """Dessine les failles portails"""
        for rift in self.portal_rifts:
            draw_x = rift['x'] - camera_x * 0.6
            
            if draw_x + rift['width'] >= 0 and draw_x <= SCREEN_WIDTH:
                # Pulsation d'énergie
                pulse = math.sin(rift['pulse_offset']) * 0.5 + 0.5
                
                # Distorsion
                distortion = math.sin(rift['distortion_offset']) * 10
                
                # Surface de la faille
                rift_surface = pygame.Surface((rift['width'], rift['height']), pygame.SRCALPHA)
                
                # Énergie du portail
                energy_alpha = int(80 + pulse * 60)
                energy_color = (*rift['energy_color'], energy_alpha)
                
                # Forme de faille (ellipse déformée)
                for i in range(5):
                    ellipse_width = rift['width'] - i * 8
                    ellipse_height = rift['height'] - i * 12
                    alpha = energy_alpha - i * 15
                    if alpha > 0 and ellipse_width > 0 and ellipse_height > 0:
                        ellipse_color = (*rift['energy_color'], alpha)
                        ellipse_surface = pygame.Surface((ellipse_width, ellipse_height), pygame.SRCALPHA)
                        pygame.draw.ellipse(ellipse_surface, ellipse_color, 
                                          (0, 0, ellipse_width, ellipse_height))
                        rift_surface.blit(ellipse_surface, (i * 4, i * 6))
                
                screen.blit(rift_surface, (draw_x + distortion, rift['y']))
    
    def draw_cosmic_dust(self, screen, camera_x):
        """Dessine la poussière cosmique"""
        for dust in self.cosmic_dust:
            draw_x = dust['x'] - camera_x * 0.8
            
            if -10 <= draw_x <= SCREEN_WIDTH + 10:
                # Scintillement
                twinkle = math.sin(dust['twinkle_offset']) * 0.5 + 0.5
                alpha = int(dust['transparency'] * twinkle)
                
                if alpha > 0:
                    dust_color = (200, 180, 255, alpha)
                    dust_surface = pygame.Surface((dust['size'] * 2, dust['size'] * 2), pygame.SRCALPHA)
                    pygame.draw.circle(dust_surface, dust_color, 
                                     (dust['size'], dust['size']), dust['size'])
                    screen.blit(dust_surface, (draw_x - dust['size'], dust['y'] - dust['size']))
    
    def draw_mirror_shards(self, screen, camera_x):
        """Dessine les éclats de miroir"""
        for shard in self.mirror_shards:
            draw_x = shard['x'] - camera_x * 0.9
            
            if -20 <= draw_x <= SCREEN_WIDTH + 20:
                # Rotation et réflexion
                reflection = math.sin(self.time_offset + shard['x'] * 0.01) * shard['reflection_intensity']
                
                # Surface de l'éclat
                shard_surface = pygame.Surface((shard['size'] * 2, shard['size'] * 2), pygame.SRCALPHA)
                
                # Couleur réfléchissante
                reflect_intensity = int(150 + reflection * 100)
                shard_color = (reflect_intensity, reflect_intensity, 255, 180)
                
                # Forme d'éclat (triangle)
                points = [
                    (shard['size'], 0),
                    (shard['size'] * 2, shard['size'] * 2),
                    (0, shard['size'] * 2)
                ]
                
                # Rotation
                center = (shard['size'], shard['size'])
                rotated_points = []
                for point in points:
                    x = point[0] - center[0]
                    y = point[1] - center[1]
                    new_x = x * math.cos(shard['rotation']) - y * math.sin(shard['rotation'])
                    new_y = x * math.sin(shard['rotation']) + y * math.cos(shard['rotation'])
                    rotated_points.append((new_x + center[0], new_y + center[1]))
                
                pygame.draw.polygon(shard_surface, shard_color, rotated_points)
                
                # Reflet brillant
                highlight_color = (255, 255, 255, int(100 + reflection * 50))
                pygame.draw.polygon(shard_surface, highlight_color, rotated_points, 1)
                
                screen.blit(shard_surface, (draw_x - shard['size'], shard['y'] - shard['size']))
    
    def draw_refraction_effect(self, screen):
        """Dessine un effet de réfraction subtil"""
        # Lignes de réfraction
        for i in range(8):
            line_x = (i * SCREEN_WIDTH // 8) + int(math.sin(self.time_offset + i) * 30)
            line_alpha = 15 + int(math.sin(self.time_offset * 1.5 + i) * 10)
            
            line_surface = pygame.Surface((2, SCREEN_HEIGHT), pygame.SRCALPHA)
            line_color = (180, 200, 255, line_alpha)
            line_surface.fill(line_color)
            screen.blit(line_surface, (line_x, 0))
        
        # Effet de distorsion en haut
        distortion_surface = pygame.Surface((SCREEN_WIDTH, 60), pygame.SRCALPHA)
        for y in range(60):
            alpha = int(25 * (1 - y / 60))
            distortion_color = (200, 180, 255, alpha)
            pygame.draw.rect(distortion_surface, distortion_color, (0, y, SCREEN_WIDTH, 1))
        screen.blit(distortion_surface, (0, 0)) 