import pygame
import math
import random
from settings import *
from entities.lyra import Lyra
from levels.level_generator import LevelGenerator
from levels.spectral_forest_generator import SpectralForestGenerator
from levels.celestial_mirrors_generator import CelestialMirrorsGenerator
from levels.astral_core_generator import AstralCoreGenerator
from assets.background import StarryBackground
from assets.spectral_forest_background import SpectralForestBackground
from assets.celestial_mirrors_background import CelestialMirrorsBackground
from assets.astral_core_background import AstralCoreBackground
from levels.zone_manager import ZoneManager
from levels.level_manager import LevelManager
from entities.power_manager import PowerManager
from systems.achievement_system import AchievementSystem

class Game:
    def __init__(self):
        """Initialise le jeu"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Éclats d'Astralis ✨")
        self.clock = pygame.time.Clock()
        
        # État du jeu - COMMENCER PAR LA SÉLECTION DE NIVEAU
        self.game_state = "level_select"  # "level_select", "playing", "game_over", "paused", "level_complete"
        self.running = True
        
        # Polices
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
        # Systèmes de jeu
        self.level_manager = LevelManager()
        self.achievement_system = AchievementSystem()
        self.zone_manager = ZoneManager()
        self.power_manager = PowerManager()
        
        # Éléments de jeu (initialisés quand on démarre un niveau)
        self.lyra = None
        self.level_generator = None
        self.background = None
        
        # Variables de jeu
        self.camera_x = 0
        self.target_camera_x = 0
        self.score = 0
        self.distance_traveled = 0
        self.stars_collected = 0
        
        # Effets visuels
        self.screen_shake = 0
        self.flash_effect = 0
        
        # Système narratif
        self.narrative_messages = [
            "Les fragments d'Astralis résonnent avec votre essence...",
            "Chaque étoile collectée révèle un fragment de vérité...",
            "L'ancienne magie coule dans vos veines...",
            "Les ombres reculent devant votre lumière grandissante...",
            "Vous sentez la puissance d'Astralis s'éveiller en vous...",
            "Les secrets du cosmos se dévoilent peu à peu...",
            "Votre destinée stellaire prend forme...",
            "L'harmonie entre les mondes se rétablit..."
        ]
        self.current_narrative = ""
        self.narrative_timer = 0
        self.narrative_alpha = 0
        self.last_narrative_trigger = 0
        
        # Temps de début de niveau
        self.level_start_time = pygame.time.get_ticks()
        
        # Initialiser le fond étoilé pour l'écran de sélection
        self.background = StarryBackground()
        
        print("🎮 Jeu initialisé en mode sélection de niveau")
        
    def handle_events(self):
        """Gère les événements pygame - DEPRECATED: utilisé seulement en mode standalone"""
        for event in pygame.event.get():
            self.handle_single_event(event)
    
    def handle_single_event(self, event):
        """Gère un événement pygame individuel"""
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.game_state == "playing":
                    self.game_state = "paused"
                elif self.game_state == "paused":
                    self.game_state = "playing"
                elif self.game_state == "level_select":
                    self.running = False  # Retour au menu principal
                elif self.game_state in ["game_over", "level_complete"]:
                    self.running = False  # Retour au menu principal
            elif event.key == pygame.K_r and self.game_state == "game_over":
                self.restart_game()
            elif event.key == pygame.K_r and self.game_state == "level_complete":
                self.restart_game()
            elif event.key == pygame.K_m and self.game_state in ["game_over", "level_complete", "paused"]:
                self.running = False  # Retour au menu principal
            elif event.key == pygame.K_l and self.game_state in ["game_over", "level_complete", "paused"]:
                # Nouvelle option : retour à la sélection de niveau
                self.return_to_level_select()
            elif self.game_state == "level_select":
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.start_current_level()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.level_manager.current_level = max(0, self.level_manager.current_level - 1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    max_level = min(self.level_manager.levels_unlocked - 1, len(self.level_manager.levels) - 1)
                    self.level_manager.current_level = min(max_level, self.level_manager.current_level + 1)
    
    def update(self):
        """Met à jour la logique du jeu"""
        if self.game_state != "playing":
            # Mettre à jour seulement le fond pour l'écran de sélection
            if self.game_state == "level_select":
                self.background.update(0)
            return
            
        keys_pressed = pygame.key.get_pressed()
        
        # Mettre à jour Lyra
        lyra_alive = self.lyra.update(keys_pressed, self.level_generator.platforms, self.camera_x)
        
        if not lyra_alive:
            self.game_state = "game_over"
            return
        
        # Mettre à jour la caméra pour suivre Lyra
        self.target_camera_x = self.lyra.x - SCREEN_WIDTH // 3
        self.camera_x += (self.target_camera_x - self.camera_x) * 0.1
        
        # Scroll automatique
        self.camera_x += SCROLL_SPEED
        
        # Mettre à jour la distance parcourue
        self.distance_traveled = max(self.distance_traveled, self.camera_x)
        
        # Mettre à jour le niveau
        self.level_generator.update(self.camera_x)
        
        # Mettre à jour le fond
        self.background.update(self.camera_x)
        
        # Vérifier les collisions avec les fragments d'étoiles
        self.check_star_fragment_collisions()
        
        # Vérifier les collisions avec les ombres
        self.check_shadow_collisions()
        
        # Vérifier la fin de niveau
        if self.level_generator.check_level_completion(self.lyra):
            self.game_state = "level_complete"
            return
        
        # Vérifier les mécaniques spéciales selon le type de générateur
        if isinstance(self.level_generator, CelestialMirrorsGenerator):
            # Vérifier les collisions avec les portails miroirs
            if self.level_generator.check_portal_collisions(self.lyra):
                self.flash_effect = 20  # Effet visuel de téléportation
            
            # Vérifier les zones de gravité inversée
            if self.level_generator.check_gravity_zones(self.lyra):
                # Appliquer la gravité inversée à Lyra
                if hasattr(self.lyra, 'gravity'):
                    self.lyra.gravity = -abs(self.lyra.gravity)  # Inverser la gravité
            else:
                # Restaurer la gravité normale
                if hasattr(self.lyra, 'gravity'):
                    self.lyra.gravity = abs(self.lyra.gravity)
        
        # Mettre à jour les effets visuels
        self.update_visual_effects()
        
        # Mettre à jour le système de zones
        zone_changed = self.zone_manager.update(self.score)
        
        # Mettre à jour les nouveaux systèmes
        self.power_manager.update(self.lyra)
        self.achievement_system.update()
        
        # Générer des orbes de pouvoir occasionnellement - VERSION AMÉLIORÉE
        if random.random() < 0.001:  # Très rare
            power_types = ['astral_jump', 'levitation', 'light_shield', 'speed_burst']
            power_type = random.choice(power_types)
            
            # Trouver une plateforme proche pour placer l'orbe de manière accessible
            orb_x, orb_y = self.find_accessible_power_orb_position()
            if orb_x is not None:  # Position valide trouvée
                self.power_manager.add_power_orb(orb_x, orb_y, power_type)
        
        # Mettre à jour le système narratif
        self.update_narrative_system()
    
    def check_star_fragment_collisions(self):
        """Vérifie les collisions avec les fragments d'étoiles"""
        for star in self.level_generator.star_fragments:
            if star.check_collision(self.lyra):
                points = star.collect()
                self.score += points
                self.stars_collected += 1
                
                # Ajouter au gestionnaire de niveaux
                self.level_manager.add_fragments(1)
                
                # Effet visuel de collecte
                self.flash_effect = 10
                
                # Bonus spéciaux tous les 5 fragments - Double saut au lieu de gravité inversée
                if self.stars_collected % 5 == 0:
                    self.lyra.activate_double_jump()
                elif self.stars_collected % 3 == 0:
                    self.lyra.activate_invincibility()
    
    def check_shadow_collisions(self):
        """Vérifie les collisions avec les ombres astrales"""
        for shadow in self.level_generator.shadows:
            if shadow.check_collision(self.lyra):
                # Vérifier si protégé par un bouclier de lumière
                if self.power_manager.has_power('light_shield'):
                    # Traverser l'ombre sans dégâts
                    shadow.destroy()
                    continue
                    
                if not self.lyra.invincible:
                    # Tracking pour les succès
                    self.achievement_system.track_shadow_hit()
                    
                    # Effet de dégâts
                    self.screen_shake = 20
                    self.flash_effect = 15
                    
                    # Réduire le score
                    self.score = max(0, self.score - 50)
                    
                    # Activer l'invincibilité temporaire
                    self.lyra.activate_invincibility()
                
                # Détruire l'ombre
                shadow.destroy()
    
    def update_visual_effects(self):
        """Met à jour les effets visuels"""
        if self.screen_shake > 0:
            self.screen_shake -= 1
            
        if self.flash_effect > 0:
            self.flash_effect -= 1
    
    def update_narrative_system(self):
        """Met à jour le système narratif"""
        # Déclencher un message narratif tous les 7 fragments
        if self.stars_collected > 0 and self.stars_collected % 7 == 0 and self.stars_collected != self.last_narrative_trigger:
            self.trigger_narrative_message()
            self.last_narrative_trigger = self.stars_collected
        
        # Mettre à jour l'affichage du message narratif
        if self.narrative_timer > 0:
            self.narrative_timer -= 1
            
            # Calcul de l'alpha pour l'effet de fade
            if self.narrative_timer > 120:  # Fade in (2 secondes)
                self.narrative_alpha = min(255, (180 - self.narrative_timer) * 4.25)
            else:  # Fade out (2 secondes)
                self.narrative_alpha = max(0, self.narrative_timer * 2.125)
    
    def find_accessible_power_orb_position(self):
        """Trouve une position accessible pour un orbe de pouvoir près d'une plateforme"""
        # Chercher des plateformes dans la zone visible et à venir
        search_start = self.camera_x + SCREEN_WIDTH // 2
        search_end = self.camera_x + SCREEN_WIDTH * 2
        
        # Obtenir les plateformes dans cette zone
        candidate_platforms = []
        for platform in self.level_generator.platforms:
            if search_start <= platform.x <= search_end:
                candidate_platforms.append(platform)
        
        if not candidate_platforms:
            return None, None  # Aucune plateforme disponible
        
        # Choisir une plateforme aléatoire
        platform = random.choice(candidate_platforms)
        
        # Placer l'orbe au-dessus de la plateforme, dans une zone accessible
        orb_x = platform.x + platform.width // 2 + random.randint(-30, 30)
        orb_y = platform.y - 60 - random.randint(0, 20)  # Au-dessus mais atteignable
        
        # S'assurer que l'orbe est dans les limites de l'écran
        orb_y = max(50, min(SCREEN_HEIGHT - 50, orb_y))
        
        return orb_x, orb_y
    
    def trigger_narrative_message(self):
        """Déclenche un nouveau message narratif"""
        import random
        
        # Choisir un message selon la zone actuelle
        zone = self.zone_manager.get_current_zone()
        if zone['name'] == "Royaume d'Orion":
            messages = self.narrative_messages[:5]
        elif zone['name'] == "Nébuleuse de l'Oubli":
            messages = self.narrative_messages[3:8]
        elif zone['name'] == "Sanctuaire de Vega":
            messages = self.narrative_messages[6:11]
        else:  # Cœur d'Andromède
            messages = self.narrative_messages[9:]
        
        self.current_narrative = random.choice(messages)
        self.narrative_timer = 180  # 3 secondes d'affichage
        self.narrative_alpha = 0
    
    def draw_ui(self):
        """Dessine l'interface utilisateur"""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, COLORS['text'])
        self.screen.blit(score_text, (20, 20))
        
        # Fragments collectés
        stars_text = self.small_font.render(f"Fragments: {self.stars_collected}", True, COLORS['star_fragment'])
        self.screen.blit(stars_text, (20, 60))
        
        # Distance
        distance_text = self.small_font.render(f"Distance: {int(self.distance_traveled)}m", True, COLORS['text'])
        self.screen.blit(distance_text, (20, 85))
        
        # Niveau actuel
        level_info = self.level_manager.get_current_level()
        level_text = self.small_font.render(f"Niveau: {level_info['name']}", True, COLORS['star_fragment'])
        self.screen.blit(level_text, (20, 110))
        
        # Progression vers le prochain niveau
        progress = self.level_manager.get_progress_info()
        if not progress.get('final_level', False):
            progress_text = self.small_font.render(f"Prochain niveau: {progress['next_unlock']} fragments", True, COLORS['text'])
            self.screen.blit(progress_text, (20, 135))
        
        # Succès débloqués
        achievement_text = self.small_font.render(self.achievement_system.get_progress_summary(), True, COLORS['lyra_glow'])
        self.screen.blit(achievement_text, (20, 160))
        
        # Indicateurs d'état de Lyra
        y_offset = 20
        if self.lyra.can_double_jump:
            double_jump_text = self.small_font.render("DOUBLE SAUT", True, COLORS['star_fragment'])
            self.screen.blit(double_jump_text, (SCREEN_WIDTH - 200, y_offset))
            y_offset += 25
            
        if self.lyra.invincible:
            invincible_text = self.small_font.render("INVINCIBLE", True, COLORS['lyra_glow'])
            self.screen.blit(invincible_text, (SCREEN_WIDTH - 200, y_offset))
            y_offset += 25
        
        # Pouvoirs actifs
        for power_type, power_data in self.power_manager.active_powers.items():
            time_left = power_data['timer'] // 60  # Convertir en secondes
            power_text = self.small_font.render(f"{power_type.upper()}: {time_left}s", True, (255, 200, 100))
            self.screen.blit(power_text, (SCREEN_WIDTH - 200, y_offset))
            y_offset += 25
        
        # Message narratif
        if self.narrative_timer > 0:
            narrative_surface = pygame.Surface((SCREEN_WIDTH, 60), pygame.SRCALPHA)
            narrative_color = (*COLORS['star_fragment'], int(self.narrative_alpha))
            
            # Fond semi-transparent pour le message
            bg_surface = pygame.Surface((SCREEN_WIDTH - 40, 50), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 100))
            narrative_surface.blit(bg_surface, (20, 5))
            
            # Texte narratif
            narrative_text = self.font.render(self.current_narrative, True, narrative_color)
            text_rect = narrative_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
            narrative_surface.blit(narrative_text, text_rect)
            
            self.screen.blit(narrative_surface, (0, SCREEN_HEIGHT // 2 - 100))
        
        # Notifications de succès
        self.achievement_system.draw_notifications(self.screen)
        
        # Contrôles
        controls_text = self.small_font.render("Flèches: Mouvement | Espace: Saut | Échap: Pause", True, COLORS['text'])
        self.screen.blit(controls_text, (20, SCREEN_HEIGHT - 30))
    
    def draw_game_over_screen(self):
        """Dessine l'écran de game over"""
        # Fond semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Titre
        title_text = self.font.render("ÉCHEC DE LA MISSION", True, COLORS['shadow'])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(title_text, title_rect)
        
        # Score final
        score_text = self.small_font.render(f"Score final: {self.score}", True, COLORS['text'])
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(score_text, score_rect)
        
        # Distance parcourue
        distance_text = self.small_font.render(f"Distance: {int(self.distance_traveled)}m", True, COLORS['text'])
        distance_rect = distance_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(distance_text, distance_rect)
        
        # Fragments collectés
        fragments_text = self.small_font.render(f"Fragments collectés: {self.stars_collected}", True, COLORS['star_fragment'])
        fragments_rect = fragments_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(fragments_text, fragments_rect)
        
        # Message d'encouragement
        encouragement_text = self.small_font.render("Les ombres d'Astralis ne vous arrêteront pas...", True, COLORS['lyra_glow'])
        encouragement_rect = encouragement_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(encouragement_text, encouragement_rect)
        
        # Instructions
        restart_text = self.small_font.render("R : Recommencer", True, COLORS['star_fragment'])
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
        self.screen.blit(restart_text, restart_rect)
        
        level_select_text = self.small_font.render("L : Sélection de niveau", True, COLORS['text'])
        level_select_rect = level_select_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(level_select_text, level_select_rect)
        
        menu_text = self.small_font.render("M : Menu principal", True, COLORS['text'])
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        self.screen.blit(menu_text, menu_rect)
    
    def draw_pause_screen(self):
        """Dessine l'écran de pause"""
        # Fond semi-transparent
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Titre
        pause_text = self.font.render("JEU EN PAUSE", True, COLORS['text'])
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(pause_text, pause_rect)
        
        # Niveau actuel
        level_name = self.level_manager.get_current_level()['name']
        level_text = self.small_font.render(f"Niveau: {level_name}", True, COLORS['lyra_glow'])
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(level_text, level_rect)
        
        # Statistiques actuelles
        score_text = self.small_font.render(f"Score: {self.score}", True, COLORS['text'])
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
        self.screen.blit(score_text, score_rect)
        
        fragments_text = self.small_font.render(f"Fragments: {self.stars_collected}", True, COLORS['star_fragment'])
        fragments_rect = fragments_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(fragments_text, fragments_rect)
        
        # Instructions
        continue_text = self.small_font.render("Échap : Continuer", True, COLORS['lyra_glow'])
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(continue_text, continue_rect)
        
        level_select_text = self.small_font.render("L : Sélection de niveau", True, COLORS['text'])
        level_select_rect = level_select_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
        self.screen.blit(level_select_text, level_select_rect)
        
        menu_text = self.small_font.render("M : Menu principal", True, COLORS['text'])
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        self.screen.blit(menu_text, menu_rect)
    
    def draw_level_complete_screen(self):
        """Dessine l'écran de fin de niveau"""
        # Fond semi-transparent doré
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((20, 15, 5))
        self.screen.blit(overlay, (0, 0))
        
        # Titre de victoire
        victory_text = self.font.render("NIVEAU TERMINÉ !", True, COLORS['star_fragment'])
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        self.screen.blit(victory_text, victory_rect)
        
        # Nom du niveau
        level_name = self.level_manager.get_current_level()['name']
        level_text = self.small_font.render(f"Niveau: {level_name}", True, COLORS['lyra_glow'])
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 90))
        self.screen.blit(level_text, level_rect)
        
        # Score final
        score_text = self.small_font.render(f"Score: {self.score}", True, COLORS['text'])
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(score_text, score_rect)
        
        # Fragments collectés
        fragments_text = self.small_font.render(f"Fragments collectés: {self.stars_collected}", True, COLORS['star_fragment'])
        fragments_rect = fragments_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(fragments_text, fragments_rect)
        
        # Distance parcourue
        distance_text = self.small_font.render(f"Distance: {int(self.distance_traveled)}m", True, COLORS['text'])
        distance_rect = distance_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(distance_text, distance_rect)
        
        # Temps de niveau
        level_time = (pygame.time.get_ticks() - self.level_start_time) // 1000
        time_text = self.small_font.render(f"Temps: {level_time}s", True, COLORS['text'])
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(time_text, time_rect)
        
        # Message mystique de fin
        mystique_text = self.small_font.render("L'essence d'Astralis coule maintenant en vous...", True, COLORS['lyra_glow'])
        mystique_rect = mystique_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        self.screen.blit(mystique_text, mystique_rect)
        
        # Instructions
        restart_text = self.small_font.render("R : Recommencer", True, COLORS['star_fragment'])
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110))
        self.screen.blit(restart_text, restart_rect)
        
        level_select_text = self.small_font.render("L : Sélection de niveau", True, COLORS['text'])
        level_select_rect = level_select_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140))
        self.screen.blit(level_select_text, level_select_rect)
        
        menu_text = self.small_font.render("M : Menu principal", True, COLORS['text'])
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 170))
        self.screen.blit(menu_text, menu_rect)
    
    def draw_level_select_screen(self):
        """Dessine l'écran de sélection de niveau"""
        # Fond étoilé
        self.background.draw(self.screen, 0)
        
        # Titre
        title_text = self.font.render("ÉCLATS D'ASTRALIS", True, COLORS['star_fragment'])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.small_font.render("Sélection de Niveau", True, COLORS['text'])
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Niveaux disponibles
        y_start = 180
        for i, level in enumerate(self.level_manager.levels):
            y_pos = y_start + i * 80
            
            # Vérifier si le niveau est débloqué
            is_unlocked = i < self.level_manager.levels_unlocked
            is_current = i == self.level_manager.current_level
            
            # Couleur selon l'état
            if not is_unlocked:
                color = (100, 100, 100)  # Gris pour verrouillé
                name = f"🔒 {level['name']}"
            elif is_current:
                color = COLORS['star_fragment']  # Doré pour sélectionné
                name = f"▶ {level['name']}"
            else:
                color = COLORS['text']  # Blanc pour disponible
                name = level['name']
            
            # Nom du niveau
            level_text = self.font.render(name, True, color)
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            self.screen.blit(level_text, level_rect)
            
            # Description
            if is_unlocked:
                desc_text = self.small_font.render(level['description'], True, color)
                desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 25))
                self.screen.blit(desc_text, desc_rect)
                
                # Fragments requis
                if level['fragments_required'] > 0:
                    req_text = self.small_font.render(f"Fragments requis: {level['fragments_required']}", True, (150, 150, 150))
                    req_rect = req_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 45))
                    self.screen.blit(req_text, req_rect)
        
        # Statistiques globales
        stats_y = SCREEN_HEIGHT - 120
        progress = self.level_manager.get_progress_info()
        stats_text = self.small_font.render(f"Fragments totaux: {progress['fragments_total']}", True, COLORS['lyra_glow'])
        stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, stats_y))
        self.screen.blit(stats_text, stats_rect)
        
        achievement_text = self.small_font.render(self.achievement_system.get_progress_summary(), True, COLORS['lyra_glow'])
        achievement_rect = achievement_text.get_rect(center=(SCREEN_WIDTH // 2, stats_y + 25))
        self.screen.blit(achievement_text, achievement_rect)
        
        # Instructions
        controls_text = self.small_font.render("← → : Naviguer | Entrée/Espace : Jouer | Échap : Quitter", True, COLORS['text'])
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(controls_text, controls_rect)
    
    def draw(self):
        """Dessine tout le jeu"""
        # IMPORTANT : Effacer l'écran pour éviter les traînées
        self.screen.fill(COLORS['background'])
        
        # Si on est en mode sélection de niveau, dessiner seulement l'écran de sélection
        if self.game_state == "level_select":
            self.draw_level_select_screen()
            return
        
        # Pour les autres modes, on a besoin des éléments de jeu
        if self.lyra is None or self.level_generator is None:
            # Si les éléments ne sont pas initialisés, dessiner seulement les écrans d'état
            if self.game_state == "game_over":
                self.draw_game_over_screen()
            elif self.game_state == "paused":
                self.draw_pause_screen()
            elif self.game_state == "level_complete":
                self.draw_level_complete_screen()
            return
        
        # Calculer l'offset de tremblement d'écran
        shake_x = 0
        shake_y = 0
        if self.screen_shake > 0:
            import random
            shake_x = random.randint(-self.screen_shake, self.screen_shake)
            shake_y = random.randint(-self.screen_shake, self.screen_shake)
        
        # Dessiner le fond étoilé
        if self.background:
            self.background.draw(self.screen, self.camera_x + shake_x)
        
        # Dessiner le niveau
        if self.level_generator:
            self.level_generator.draw(self.screen, self.camera_x + shake_x)
        
        # Dessiner Lyra
        if self.lyra:
            self.lyra.draw(self.screen, self.camera_x + shake_x)
        
        # Dessiner les ombres
        if self.level_generator and hasattr(self.level_generator, 'shadows'):
            for shadow in self.level_generator.shadows:
                shadow.draw(self.screen, self.camera_x + shake_x)
                
        # Dessiner les orbes de pouvoir
        self.power_manager.draw(self.screen, self.camera_x + shake_x)
        
        # Effet de flash
        if self.flash_effect > 0:
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.set_alpha(self.flash_effect * 10)
            flash_surface.fill((255, 255, 255))
            self.screen.blit(flash_surface, (0, 0))
        
        # Dessiner l'interface utilisateur
        self.draw_ui()
        
        # Dessiner les écrans d'état
        if self.game_state == "game_over":
            self.draw_game_over_screen()
        elif self.game_state == "paused":
            self.draw_pause_screen()
        elif self.game_state == "level_complete":
            self.draw_level_complete_screen()
    
    def choose_level_generator(self, level):
        """Choisit le générateur approprié selon le niveau"""
        if level == 0:
            return LevelGenerator()
        elif level == 1:
            return SpectralForestGenerator()
        elif level == 2:
            return CelestialMirrorsGenerator()
        elif level == 3:
            return AstralCoreGenerator()
        else:
            return LevelGenerator()  # Fallback
    
    def choose_background(self, level):
        """Choisit le fond approprié selon le niveau"""
        if level == 0:
            return StarryBackground()
        elif level == 1:
            return SpectralForestBackground()
        elif level == 2:
            return CelestialMirrorsBackground()
        elif level == 3:
            return AstralCoreBackground()
        else:
            return StarryBackground()  # Fallback
    
    def restart_game(self):
        """Redémarre le jeu en préservant le niveau actuel"""
        current_level = self.level_manager.current_level
        print(f"Redémarrage du niveau {current_level}")
        
        # Choisir le bon générateur selon le niveau actuel
        self.level_generator = self.choose_level_generator(current_level)
        print(f"Générateur choisi: {type(self.level_generator).__name__}")
        
        # Choisir le bon fond selon le niveau actuel
        self.background = self.choose_background(current_level)
        print(f"Fond choisi: {type(self.background).__name__}")
        
        # Réinitialiser Lyra
        self.lyra = Lyra(100, SCREEN_HEIGHT - 150)
        
        # Réinitialiser la caméra
        self.camera_x = 0
        
        # Réinitialiser l'état du jeu
        self.game_state = "playing"
        
        print(f"Jeu redémarré au niveau {current_level}")
    
    def return_to_level_select(self):
        """Retourne à l'écran de sélection de niveau"""
        print("📋 Retour à la sélection de niveau...")
        
        # Nettoyer les éléments de jeu
        self.lyra = None
        self.level_generator = None
        
        # Réinitialiser le fond pour l'écran de sélection
        self.background = StarryBackground()
        
        # Réinitialiser les variables
        self.camera_x = 0
        self.target_camera_x = 0
        self.score = 0
        self.distance_traveled = 0
        self.stars_collected = 0
        self.screen_shake = 0
        self.flash_effect = 0
        
        # Changer d'état
        self.game_state = "level_select"
        print("✅ Écran de sélection de niveau activé")
    
    def start_current_level(self):
        """Démarre le niveau actuellement sélectionné"""
        current_level = self.level_manager.current_level
        print(f"Démarrage du niveau {current_level}")
        
        # Choisir le bon générateur selon le niveau
        self.level_generator = self.choose_level_generator(current_level)
        print(f"Générateur choisi: {type(self.level_generator).__name__}")
        
        # Choisir le bon fond selon le niveau
        self.background = self.choose_background(current_level)
        print(f"Fond choisi: {type(self.background).__name__}")
        
        # Créer Lyra
        self.lyra = Lyra(100, SCREEN_HEIGHT - 150)
        
        # Réinitialiser la caméra
        self.camera_x = 0
        
        # Changer l'état du jeu
        self.game_state = "playing"
        
        print(f"Niveau {current_level} démarré avec succès")
    
    def run(self):
        """Boucle principale du jeu"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit() 