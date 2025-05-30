import pygame
from settings import *

class LevelManager:
    """Gestionnaire de progression multi-niveaux"""
    
    def __init__(self):
        self.current_level = 0
        self.levels_unlocked = 1
        self.total_fragments_collected = 0
        
        self.levels = [
            {
                'name': "Ruines Lunaires",
                'description': "Les vestiges d'une civilisation oubliée...",
                'fragments_required': 0,  # Premier niveau
                'background_theme': 'lunar',
                'music': 'lunar_ruins.ogg',
                'colors': {
                    'background': (5, 10, 25),
                    'platform': (80, 90, 120),
                    'ambient': (150, 160, 200)
                },
                'special_mechanics': ['low_gravity']
            },
            {
                'name': "Forêt Spectrale",
                'description': "Les arbres murmurent des secrets anciens...",
                'fragments_required': 15,
                'background_theme': 'spectral',
                'music': 'spectral_forest.ogg',
                'colors': {
                    'background': (10, 25, 15),
                    'platform': (60, 120, 80),
                    'ambient': (100, 200, 150)
                },
                'special_mechanics': ['moving_platforms', 'phantom_trees']
            },
            {
                'name': "Miroirs Célestes",
                'description': "La réalité se reflète à l'infini...",
                'fragments_required': 50,
                'background_theme': 'celestial',
                'music': 'celestial_mirrors.ogg',
                'colors': {
                    'background': (15, 5, 30),
                    'platform': (120, 80, 140),
                    'ambient': (200, 150, 220)
                },
                'special_mechanics': ['mirror_portals', 'gravity_shifts']
            },
            {
                'name': "Cœur d'Astralis",
                'description': "Le sanctuaire final où tout a commencé...",
                'fragments_required': 75,
                'background_theme': 'core',
                'music': 'astralis_core.ogg',
                'colors': {
                    'background': (25, 15, 5),
                    'platform': (140, 120, 80),
                    'ambient': (220, 200, 150)
                },
                'special_mechanics': ['all_powers', 'final_boss']
            }
        ]
    
    def get_current_level(self):
        """Retourne les informations du niveau actuel"""
        return self.levels[self.current_level]
    
    def can_unlock_next_level(self):
        """Vérifie si le niveau suivant peut être débloqué"""
        if self.current_level + 1 >= len(self.levels):
            return False
        next_level = self.levels[self.current_level + 1]
        return self.total_fragments_collected >= next_level['fragments_required']
    
    def unlock_next_level(self):
        """Débloque le niveau suivant"""
        if self.can_unlock_next_level():
            self.levels_unlocked += 1
            return True
        return False
    
    def advance_to_next_level(self):
        """Passe au niveau suivant"""
        if self.current_level + 1 < self.levels_unlocked:
            self.current_level += 1
            return True
        return False
    
    def add_fragments(self, count):
        """Ajoute des fragments collectés"""
        self.total_fragments_collected += count
        
    def get_progress_info(self):
        """Retourne les informations de progression"""
        current = self.get_current_level()
        if self.current_level + 1 < len(self.levels):
            next_level = self.levels[self.current_level + 1]
            fragments_needed = next_level['fragments_required'] - self.total_fragments_collected
            return {
                'current_level': current['name'],
                'fragments_total': self.total_fragments_collected,
                'next_unlock': max(0, fragments_needed),
                'can_advance': self.can_unlock_next_level()
            }
        else:
            return {
                'current_level': current['name'],
                'fragments_total': self.total_fragments_collected,
                'next_unlock': 0,
                'can_advance': False,
                'final_level': True
            } 