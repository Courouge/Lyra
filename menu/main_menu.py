import pygame
import math
import random
from settings import *
from assets.background import StarryBackground

class MainMenu:
    """Menu principal du jeu avec navigation complète"""
    
    def __init__(self, screen):
        self.screen = screen
        self.background = StarryBackground()
        
        # États du menu
        self.current_screen = "main"  # "main", "level_select", "options", "credits"
        self.selected_option = 0
        self.transition_timer = 0
        self.transition_alpha = 0
        
        # Polices
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.tiny_font = pygame.font.Font(None, 24)
        
        # Options du menu principal
        self.main_options = [
            {"text": "Nouvelle Partie", "action": "new_game"},
            {"text": "Continuer", "action": "continue"},
            {"text": "Sélection de Niveau", "action": "level_select"},
            {"text": "Options", "action": "options"},
            {"text": "Crédits", "action": "credits"},
            {"text": "Quitter", "action": "quit"}
        ]
        
        # Options du menu options
        self.options_menu = [
            {"text": "Volume Musique: 70%", "action": "music_volume"},
            {"text": "Volume Effets: 80%", "action": "sound_volume"},
            {"text": "Plein Écran: Non", "action": "fullscreen"},
            {"text": "Difficulté: Normal", "action": "difficulty"},
            {"text": "Retour", "action": "back"}
        ]
        
        # Effets visuels
        self.star_particles = []
        self.title_glow = 0
        self.menu_hover_effect = {}
        
        # Générer des particules d'étoiles pour le menu
        for _ in range(30):
            self.star_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'vel_x': random.uniform(-0.5, 0.5),
                'vel_y': random.uniform(-0.5, 0.5),
                'size': random.randint(1, 3),
                'brightness': random.uniform(0.3, 1.0),
                'pulse_speed': random.uniform(0.02, 0.05)
            })
        
        # Initialiser les effets de survol
        for i in range(len(self.main_options)):
            self.menu_hover_effect[i] = 0
    
    def handle_event(self, event):
        """Gère les événements du menu"""
        if event.type == pygame.KEYDOWN:
            if self.current_screen == "main":
                return self.handle_main_menu_input(event)
            elif self.current_screen == "level_select":
                return self.handle_level_select_input(event)
            elif self.current_screen == "options":
                return self.handle_options_input(event)
            elif self.current_screen == "credits":
                return self.handle_credits_input(event)
        
        return None
    
    def handle_main_menu_input(self, event):
        """Gère les entrées du menu principal"""
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.selected_option = (self.selected_option - 1) % len(self.main_options)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.selected_option = (self.selected_option + 1) % len(self.main_options)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            action = self.main_options[self.selected_option]["action"]
            if action == "new_game":
                return "new_game"
            elif action == "continue":
                return "continue"
            elif action == "level_select":
                self.current_screen = "level_select"
                self.selected_option = 0
            elif action == "options":
                self.current_screen = "options"
                self.selected_option = 0
            elif action == "credits":
                self.current_screen = "credits"
            elif action == "quit":
                return "quit"
        elif event.key == pygame.K_ESCAPE:
            return "quit"
        
        return None
    
    def handle_level_select_input(self, event):
        """Gère les entrées de sélection de niveau"""
        if event.key == pygame.K_ESCAPE:
            self.current_screen = "main"
            self.selected_option = 2  # Retour sur "Sélection de Niveau"
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            # Au lieu de retourner "level_select", retourner "new_game" pour lancer le jeu
            return "new_game"
        
        return None
    
    def handle_options_input(self, event):
        """Gère les entrées du menu options"""
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.selected_option = (self.selected_option - 1) % len(self.options_menu)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.selected_option = (self.selected_option + 1) % len(self.options_menu)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            action = self.options_menu[self.selected_option]["action"]
            if action == "back":
                self.current_screen = "main"
                self.selected_option = 3  # Retour sur "Options"
            # Ici on pourrait ajouter la logique pour changer les options
        elif event.key == pygame.K_ESCAPE:
            self.current_screen = "main"
            self.selected_option = 3
        
        return None
    
    def handle_credits_input(self, event):
        """Gère les entrées de l'écran crédits"""
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
            self.current_screen = "main"
            self.selected_option = 4  # Retour sur "Crédits"
        
        return None
    
    def update(self):
        """Met à jour les animations du menu"""
        # Mettre à jour le fond étoilé
        self.background.update(0)
        
        # Mettre à jour les effets visuels
        self.title_glow += 0.05
        
        # Mettre à jour les particules d'étoiles
        for particle in self.star_particles:
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            particle['brightness'] += particle['pulse_speed']
            
            # Rebond aux bords
            if particle['x'] <= 0 or particle['x'] >= SCREEN_WIDTH:
                particle['vel_x'] *= -1
            if particle['y'] <= 0 or particle['y'] >= SCREEN_HEIGHT:
                particle['vel_y'] *= -1
            
            # Garder dans les limites
            particle['x'] = max(0, min(SCREEN_WIDTH, particle['x']))
            particle['y'] = max(0, min(SCREEN_HEIGHT, particle['y']))
        
        # Mettre à jour les effets de survol
        for i in range(len(self.main_options)):
            if i == self.selected_option:
                self.menu_hover_effect[i] = min(1.0, self.menu_hover_effect[i] + 0.1)
            else:
                self.menu_hover_effect[i] = max(0.0, self.menu_hover_effect[i] - 0.05)
    
    def draw(self):
        """Dessine le menu"""
        # Effacer l'écran
        self.screen.fill(COLORS['background'])
        
        # Dessiner le fond étoilé
        self.background.draw(self.screen, 0)
        
        # Dessiner les particules d'étoiles
        self.draw_star_particles()
        
        # Dessiner selon l'écran actuel
        if self.current_screen == "main":
            self.draw_main_menu()
        elif self.current_screen == "level_select":
            self.draw_level_select_placeholder()
        elif self.current_screen == "options":
            self.draw_options_menu()
        elif self.current_screen == "credits":
            self.draw_credits()
    
    def draw_star_particles(self):
        """Dessine les particules d'étoiles du menu"""
        for particle in self.star_particles:
            brightness = abs(math.sin(particle['brightness'])) * particle['brightness']
            color_intensity = max(0, min(255, int(255 * brightness)))  # S'assurer que la valeur est entre 0 et 255
            color = (color_intensity, color_intensity, color_intensity)
            
            pygame.draw.circle(self.screen, color, 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
    
    def draw_main_menu(self):
        """Dessine le menu principal"""
        # Titre avec effet de lueur
        title_glow_intensity = 0.8 + 0.2 * math.sin(self.title_glow)
        title_color = tuple(int(c * title_glow_intensity) for c in COLORS['star_fragment'])
        
        # Ombre du titre
        title_shadow = self.title_font.render("ÉCLATS D'ASTRALIS", True, (50, 50, 50))
        title_shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, 150 + 3))
        self.screen.blit(title_shadow, title_shadow_rect)
        
        # Titre principal
        title_text = self.title_font.render("ÉCLATS D'ASTRALIS", True, title_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Sous-titre mystique
        subtitle_text = self.small_font.render("~ Un voyage à travers les royaumes stellaires ~", True, COLORS['lyra_glow'])
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Options du menu
        menu_start_y = 280
        for i, option in enumerate(self.main_options):
            y_pos = menu_start_y + i * 60
            
            # Effet de survol
            hover_intensity = self.menu_hover_effect[i]
            
            # Couleur selon la sélection
            if i == self.selected_option:
                color = COLORS['star_fragment']
                # Aura de sélection
                glow_surface = pygame.Surface((400, 50), pygame.SRCALPHA)
                glow_alpha = int(30 + 20 * hover_intensity)
                glow_color = (*COLORS['star_fragment'], glow_alpha)
                pygame.draw.rect(glow_surface, glow_color, (0, 0, 400, 50))
                self.screen.blit(glow_surface, (SCREEN_WIDTH // 2 - 200, y_pos - 10))
            else:
                color = COLORS['text']
            
            # Texte de l'option
            option_text = self.menu_font.render(option["text"], True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            self.screen.blit(option_text, option_rect)
            
            # Indicateur de sélection
            if i == self.selected_option:
                indicator_x = option_rect.left - 30
                indicator_y = y_pos
                indicator_size = 5 + 3 * hover_intensity
                pygame.draw.circle(self.screen, COLORS['star_fragment'], 
                                 (int(indicator_x), int(indicator_y)), int(indicator_size))
        
        # Instructions en bas
        instructions = self.tiny_font.render("↑↓ Naviguer | Entrée Sélectionner | Échap Quitter", True, COLORS['text'])
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instructions, instructions_rect)
        
        # Version du jeu
        version_text = self.tiny_font.render("Version 2.2 - Accessibilité Parfaite", True, (100, 100, 100))
        version_rect = version_text.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))
        self.screen.blit(version_text, version_rect)
    
    def draw_level_select_placeholder(self):
        """Dessine un placeholder pour la sélection de niveau"""
        # Titre
        title_text = self.menu_font.render("SÉLECTION DE NIVEAU", True, COLORS['star_fragment'])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Message
        message_text = self.small_font.render("Cette fonctionnalité sera intégrée au jeu principal", True, COLORS['text'])
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(message_text, message_rect)
        
        # Instructions
        instructions = self.tiny_font.render("Échap Retour | Entrée Lancer le jeu", True, COLORS['text'])
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(instructions, instructions_rect)
    
    def draw_options_menu(self):
        """Dessine le menu des options"""
        # Titre
        title_text = self.menu_font.render("OPTIONS", True, COLORS['star_fragment'])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Options
        menu_start_y = 200
        for i, option in enumerate(self.options_menu):
            y_pos = menu_start_y + i * 50
            
            # Couleur selon la sélection
            if i == self.selected_option:
                color = COLORS['star_fragment']
                # Aura de sélection
                glow_surface = pygame.Surface((500, 40), pygame.SRCALPHA)
                glow_color = (*COLORS['star_fragment'], 30)
                pygame.draw.rect(glow_surface, glow_color, (0, 0, 500, 40))
                self.screen.blit(glow_surface, (SCREEN_WIDTH // 2 - 250, y_pos - 5))
            else:
                color = COLORS['text']
            
            # Texte de l'option
            option_text = self.small_font.render(option["text"], True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            self.screen.blit(option_text, option_rect)
        
        # Instructions
        instructions = self.tiny_font.render("↑↓ Naviguer | Entrée Modifier | Échap Retour", True, COLORS['text'])
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instructions, instructions_rect)
    
    def draw_credits(self):
        """Dessine l'écran des crédits"""
        # Titre
        title_text = self.menu_font.render("CRÉDITS", True, COLORS['star_fragment'])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Crédits
        credits_data = [
            ("Développement", "Claude Sonnet 4 & Utilisateur"),
            ("Concept & Design", "Collaboration IA-Humain"),
            ("Moteur de Jeu", "Pygame"),
            ("Inspiration", "Jeux de plateforme mystiques"),
            ("Musique", "Ambiances stellaires génératives"),
            ("Remerciements", "Communauté Pygame"),
            ("", ""),
            ("Éclats d'Astralis", "Un voyage infini commence..."),
        ]
        
        start_y = 150
        for i, (category, value) in enumerate(credits_data):
            y_pos = start_y + i * 40
            
            if category:
                # Catégorie
                cat_text = self.small_font.render(category + ":", True, COLORS['lyra_glow'])
                cat_rect = cat_text.get_rect(center=(SCREEN_WIDTH // 2 - 100, y_pos))
                self.screen.blit(cat_text, cat_rect)
                
                # Valeur
                val_text = self.small_font.render(value, True, COLORS['text'])
                val_rect = val_text.get_rect(center=(SCREEN_WIDTH // 2 + 100, y_pos))
                self.screen.blit(val_text, val_rect)
            else:
                # Ligne vide pour l'espacement
                continue
        
        # Message final
        final_text = self.tiny_font.render("Merci d'avoir joué à Éclats d'Astralis !", True, COLORS['star_fragment'])
        final_rect = final_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(final_text, final_rect)
        
        # Instructions
        instructions = self.tiny_font.render("Échap/Entrée Retour", True, COLORS['text'])
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(instructions, instructions_rect) 