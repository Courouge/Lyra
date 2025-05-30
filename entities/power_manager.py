import pygame
import math
import random
from settings import *

class PowerManager:
    """Gestionnaire des pouvoirs temporaires"""
    
    def __init__(self):
        self.active_powers = {}
        self.power_orbs = []
        
    def add_power_orb(self, x, y, power_type):
        """Ajoute un orbe de pouvoir"""
        orb = PowerOrb(x, y, power_type)
        self.power_orbs.append(orb)
    
    def activate_power(self, power_type, duration=300):
        """Active un pouvoir temporaire"""
        self.active_powers[power_type] = {
            'timer': duration,
            'max_duration': duration
        }
    
    def update(self, lyra):
        """Met à jour les pouvoirs actifs et les orbes"""
        # Mettre à jour les pouvoirs actifs
        for power_type in list(self.active_powers.keys()):
            self.active_powers[power_type]['timer'] -= 1
            if self.active_powers[power_type]['timer'] <= 0:
                del self.active_powers[power_type]
        
        # Mettre à jour les orbes
        for orb in self.power_orbs[:]:
            orb.update()
            if orb.check_collision(lyra):
                self.activate_power(orb.power_type)
                self.power_orbs.remove(orb)
    
    def has_power(self, power_type):
        """Vérifie si un pouvoir est actif"""
        return power_type in self.active_powers
    
    def get_power_time_left(self, power_type):
        """Retourne le temps restant d'un pouvoir"""
        if power_type in self.active_powers:
            return self.active_powers[power_type]['timer']
        return 0
    
    def draw(self, screen, camera_x):
        """Dessine les orbes de pouvoir"""
        for orb in self.power_orbs:
            orb.draw(screen, camera_x)

class PowerOrb:
    """Orbe de pouvoir collectible"""
    
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.power_type = power_type
        self.float_offset = 0
        self.glow_pulse = 0
        self.collected = False
        
        # Définir les propriétés selon le type
        self.power_info = {
            'astral_jump': {
                'color': (100, 200, 255),
                'name': "Saut Astral",
                'description': "Double saut amélioré"
            },
            'levitation': {
                'color': (255, 200, 100),
                'name': "Lévitation",
                'description': "Flotte pendant 2 secondes"
            },
            'light_shield': {
                'color': (255, 255, 150),
                'name': "Bouclier Lumineux",
                'description': "Traverse les ombres"
            },
            'speed_burst': {
                'color': (200, 100, 255),
                'name': "Éclat de Vitesse",
                'description': "Mouvement accéléré"
            }
        }
    
    def update(self):
        """Met à jour l'animation de l'orbe"""
        self.float_offset += 0.1
        self.glow_pulse += 0.15
    
    def check_collision(self, lyra):
        """Vérifie la collision avec Lyra"""
        if self.collected:
            return False
        distance = math.sqrt((self.x - lyra.x)**2 + (self.y - lyra.y)**2)
        if distance < 25:
            self.collected = True
            return True
        return False
    
    def draw(self, screen, camera_x):
        """Dessine l'orbe de pouvoir"""
        if self.collected:
            return
            
        draw_x = self.x - camera_x
        if -50 <= draw_x <= SCREEN_WIDTH + 50:
            # Position flottante
            float_y = self.y + math.sin(self.float_offset) * 5
            
            # Couleur du pouvoir
            power_color = self.power_info[self.power_type]['color']
            
            # Aura pulsante
            glow_size = 20 + math.sin(self.glow_pulse) * 5
            aura_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            for r in range(int(glow_size), 0, -2):
                alpha = 100 * (r / glow_size)
                pygame.draw.circle(aura_surface, (*power_color, int(alpha)),
                                 (glow_size, glow_size), r)
            screen.blit(aura_surface, (draw_x - glow_size, float_y - glow_size))
            
            # Orbe principal
            pygame.draw.circle(screen, power_color, (int(draw_x), int(float_y)), 12)
            
            # Noyau brillant
            core_color = tuple(min(255, c + 100) for c in power_color)
            pygame.draw.circle(screen, core_color, (int(draw_x), int(float_y)), 6)
            
            # Particules orbitales
            for i in range(4):
                angle = self.glow_pulse + i * (math.pi / 2)
                orbit_x = draw_x + math.cos(angle) * 18
                orbit_y = float_y + math.sin(angle) * 18
                pygame.draw.circle(screen, core_color, (int(orbit_x), int(orbit_y)), 2) 