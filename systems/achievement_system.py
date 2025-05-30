import pygame
from settings import *

class AchievementSystem:
    """Système de succès et défis"""
    
    def __init__(self):
        self.achievements = {
            'perfect_landing': {
                'name': "Atterrissage Parfait",
                'description': "10 atterrissages parfaits d'affilée",
                'progress': 0,
                'target': 10,
                'unlocked': False,
                'reward': "Aura dorée permanente"
            },
            'shadow_master': {
                'name': "Maître des Ombres",
                'description': "Terminer un niveau sans toucher d'ombre",
                'progress': 0,
                'target': 1,
                'unlocked': False,
                'reward': "Bouclier de lumière permanent"
            },
            'fragment_collector': {
                'name': "Collectionneur Parfait",
                'description': "Ramasser 100% des fragments d'un niveau",
                'progress': 0,
                'target': 1,
                'unlocked': False,
                'reward': "Vision des fragments cachés"
            },
            'speed_runner': {
                'name': "Coureur Astral",
                'description': "Terminer un niveau en moins de 2 minutes",
                'progress': 0,
                'target': 1,
                'unlocked': False,
                'reward': "Vitesse de base augmentée"
            },
            'explorer': {
                'name': "Explorateur Mystique",
                'description': "Découvrir 5 zones secrètes",
                'progress': 0,
                'target': 5,
                'unlocked': False,
                'reward': "Compagnon esprit guide"
            },
            'combo_master': {
                'name': "Maître des Combos",
                'description': "Enchaîner 20 sauts sans toucher le sol",
                'progress': 0,
                'target': 20,
                'unlocked': False,
                'reward': "Saut triple permanent"
            }
        }
        
        self.current_streak = {
            'perfect_landings': 0,
            'no_shadow_hits': True,
            'air_time': 0,
            'level_start_time': 0
        }
        
        self.notifications = []
    
    def track_perfect_landing(self):
        """Enregistre un atterrissage parfait"""
        self.current_streak['perfect_landings'] += 1
        if self.current_streak['perfect_landings'] >= 10:
            self.unlock_achievement('perfect_landing')
    
    def track_shadow_hit(self):
        """Enregistre un contact avec une ombre"""
        self.current_streak['no_shadow_hits'] = False
        self.current_streak['perfect_landings'] = 0  # Reset du streak
    
    def track_level_completion(self, fragments_collected, total_fragments, completion_time):
        """Enregistre la completion d'un niveau"""
        # Vérifier le succès sans ombre
        if self.current_streak['no_shadow_hits']:
            self.unlock_achievement('shadow_master')
        
        # Vérifier la collection parfaite
        if fragments_collected == total_fragments and total_fragments > 0:
            self.unlock_achievement('fragment_collector')
        
        # Vérifier le speed run (2 minutes = 120 secondes)
        if completion_time < 120:
            self.unlock_achievement('speed_runner')
        
        # Reset pour le prochain niveau
        self.reset_level_tracking()
    
    def track_air_combo(self, consecutive_jumps):
        """Enregistre les combos aériens"""
        if consecutive_jumps >= 20:
            self.unlock_achievement('combo_master')
    
    def track_secret_zone(self):
        """Enregistre la découverte d'une zone secrète"""
        self.achievements['explorer']['progress'] += 1
        if self.achievements['explorer']['progress'] >= 5:
            self.unlock_achievement('explorer')
    
    def unlock_achievement(self, achievement_id):
        """Débloque un succès"""
        if not self.achievements[achievement_id]['unlocked']:
            self.achievements[achievement_id]['unlocked'] = True
            self.add_notification(f"Succès débloqué: {self.achievements[achievement_id]['name']}!")
    
    def add_notification(self, message):
        """Ajoute une notification"""
        self.notifications.append({
            'message': message,
            'timer': 180,  # 3 secondes
            'alpha': 255
        })
    
    def update(self):
        """Met à jour les notifications"""
        for notification in self.notifications[:]:
            notification['timer'] -= 1
            if notification['timer'] <= 0:
                self.notifications.remove(notification)
            elif notification['timer'] < 60:
                notification['alpha'] = int((notification['timer'] / 60) * 255)
    
    def reset_level_tracking(self):
        """Reset le tracking pour un nouveau niveau"""
        self.current_streak['no_shadow_hits'] = True
        self.current_streak['perfect_landings'] = 0
        self.current_streak['air_time'] = 0
        self.current_streak['level_start_time'] = pygame.time.get_ticks()
    
    def get_unlocked_achievements(self):
        """Retourne la liste des succès débloqués"""
        return [aid for aid, achievement in self.achievements.items() if achievement['unlocked']]
    
    def get_progress_summary(self):
        """Retourne un résumé des progrès"""
        total = len(self.achievements)
        unlocked = len(self.get_unlocked_achievements())
        return f"{unlocked}/{total} succès débloqués"
    
    def draw_notifications(self, screen):
        """Dessine les notifications de succès"""
        y_offset = 100
        for notification in self.notifications:
            font = pygame.font.Font(None, 28)
            text_surface = font.render(notification['message'], True, (255, 255, 255))
            text_surface.set_alpha(notification['alpha'])
            
            # Fond semi-transparent
            bg_surface = pygame.Surface((text_surface.get_width() + 20, text_surface.get_height() + 10))
            bg_surface.set_alpha(notification['alpha'] // 2)
            bg_surface.fill((50, 50, 100))
            
            screen.blit(bg_surface, (SCREEN_WIDTH - text_surface.get_width() - 30, y_offset))
            screen.blit(text_surface, (SCREEN_WIDTH - text_surface.get_width() - 20, y_offset + 5))
            
            y_offset += 40 