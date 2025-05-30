#!/usr/bin/env python3
"""
Éclats d'Astralis - Jeu de plateforme mystique
Version 2.3 - Menu Principal et Sauvegarde Persistante

Un voyage à travers les royaumes stellaires où Lyra collecte
les fragments d'étoiles pour restaurer l'équilibre cosmique.
"""

import pygame
import sys
from game import Game
from menu.main_menu import MainMenu
from systems.save_system import SaveSystem

class AstralisMain:
    """Classe principale gérant le menu et le jeu"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))  # Utiliser les constantes de settings
        pygame.display.set_caption("Éclats d'Astralis ✨ - Menu Principal")
        self.clock = pygame.time.Clock()
        
        # États de l'application
        self.running = True
        self.current_state = "menu"  # "menu", "game", "transition"
        
        # Systèmes
        self.save_system = SaveSystem()
        self.main_menu = MainMenu(self.screen)
        self.game = None
        
        # Transition
        self.transition_timer = 0
        self.transition_alpha = 0
        
        # Démarrer une session
        self.save_system.start_session()
        
        print("🌟 Éclats d'Astralis - Version 2.3")
        print("✨ Menu Principal et Sauvegarde Persistante")
        print(f"💾 Sauvegarde chargée: {self.save_system.get_save_summary()}")
    
    def handle_events(self):
        """Gère les événements globaux"""
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()
                return
            
            # Déléguer selon l'état
            if self.current_state == "menu":
                action = self.main_menu.handle_event(event)
                if action:
                    self.handle_menu_action(action)
            
            elif self.current_state == "game" and self.game:
                # Déléguer l'événement au jeu
                self.game.handle_single_event(event)
    
    def handle_menu_action(self, action):
        """Gère les actions du menu"""
        if action == "new_game":
            self.start_new_game()
        elif action == "continue":
            self.continue_game()
        elif action == "level_select":
            self.start_level_select()
        elif action == "quit":
            self.quit_game()
    
    def start_new_game(self):
        """Démarre une nouvelle partie"""
        print("🎮 Démarrage d'une nouvelle partie...")
        
        # Créer une nouvelle instance de jeu
        self.game = Game()
        
        # Charger les données de sauvegarde dans le jeu
        self.load_save_data_to_game()
        
        # Changer d'état
        self.current_state = "game"
        pygame.display.set_caption("Éclats d'Astralis ✨ - En Jeu")
    
    def continue_game(self):
        """Continue la partie sauvegardée"""
        print("🔄 Continuation de la partie sauvegardée...")
        
        # Créer une nouvelle instance de jeu
        self.game = Game()
        
        # Charger les données de sauvegarde
        self.load_save_data_to_game()
        
        # Aller au niveau actuel sauvegardé
        current_level = self.save_system.save_data.get("current_level", 0)
        self.game.level_manager.current_level = current_level
        
        # Changer d'état
        self.current_state = "game"
        pygame.display.set_caption("Éclats d'Astralis ✨ - En Jeu")
    
    def start_level_select(self):
        """Démarre le mode sélection de niveau"""
        print("📋 Mode sélection de niveau...")
        
        # Créer une nouvelle instance de jeu en mode sélection
        self.game = Game()
        self.load_save_data_to_game()
        
        # Forcer l'état de sélection de niveau
        self.game.game_state = "level_select"
        
        # Changer d'état
        self.current_state = "game"
        pygame.display.set_caption("Éclats d'Astralis ✨ - Sélection de Niveau")
    
    def load_save_data_to_game(self):
        """Charge les données de sauvegarde dans le jeu"""
        if self.game:
            # Charger la progression des niveaux
            levels_unlocked = self.save_system.save_data.get("levels_unlocked", 1)
            total_fragments = self.save_system.get_total_fragments()
            
            # Mettre à jour le LevelManager
            self.game.level_manager.levels_unlocked = levels_unlocked
            self.game.level_manager.total_fragments_collected = total_fragments
            
            # Charger les succès
            achievements_unlocked = self.save_system.save_data.get("achievements_unlocked", [])
            for achievement_id in achievements_unlocked:
                self.game.achievement_system.unlock_achievement(achievement_id)
            
            # Charger les paramètres
            settings = self.save_system.save_data.get("settings", {})
            # Ici on pourrait appliquer les paramètres au jeu
            
            print(f"📊 Données chargées: {levels_unlocked} niveaux débloqués, {total_fragments} fragments")
    
    def save_game_data(self):
        """Sauvegarde les données du jeu"""
        if self.game:
            # Sauvegarder la progression du niveau actuel
            level_index = self.game.level_manager.current_level
            score = self.game.score
            time_taken = (pygame.time.get_ticks() - self.game.level_start_time) // 1000
            fragments = self.game.stars_collected
            completed = self.game.game_state == "level_complete"
            
            self.save_system.update_level_progress(level_index, score, time_taken, fragments, completed)
            
            # Sauvegarder les statistiques globales
            self.save_system.update_global_stats(
                distance_traveled=self.game.distance_traveled,
                deaths=1 if self.game.game_state == "game_over" else 0,
                jumps=getattr(self.game.lyra, 'total_jumps', 0)
            )
            
            # Sauvegarder les niveaux débloqués
            self.save_system.save_data["levels_unlocked"] = self.game.level_manager.levels_unlocked
            self.save_system.save_data["current_level"] = self.game.level_manager.current_level
            
            # Sauvegarder les succès
            if hasattr(self.game.achievement_system, 'achievements'):
                for achievement in self.game.achievement_system.achievements:
                    if hasattr(achievement, 'unlocked') and achievement.unlocked:
                        self.save_system.unlock_achievement(achievement.id)
            
            # Sauvegarder sur disque
            self.save_system.save_data_to_file()
            print("💾 Progression sauvegardée !")
    
    def return_to_menu(self):
        """Retourne au menu principal"""
        print("🏠 Retour au menu principal...")
        
        # Sauvegarder avant de quitter
        if self.game:
            self.save_game_data()
        
        # Nettoyer le jeu
        self.game = None
        
        # Retourner au menu
        self.current_state = "menu"
        pygame.display.set_caption("Éclats d'Astralis ✨ - Menu Principal")
    
    def update(self):
        """Met à jour l'état de l'application"""
        if self.current_state == "menu":
            self.main_menu.update()
        
        elif self.current_state == "game" and self.game:
            # Mettre à jour le jeu (les événements sont gérés dans handle_events)
            self.game.update()
            
            # Vérifier si on doit retourner au menu
            if not self.game.running:
                self.return_to_menu()
            
            # Sauvegarder périodiquement (toutes les 30 secondes)
            if pygame.time.get_ticks() % (30 * 1000) < 16:  # ~30 secondes
                self.save_game_data()
    
    def draw(self):
        """Dessine l'état actuel"""
        if self.current_state == "menu":
            self.main_menu.draw()
        
        elif self.current_state == "game" and self.game:
            self.game.draw()
        
        # Mettre à jour l'affichage
        pygame.display.flip()
    
    def quit_game(self):
        """Quitte le jeu proprement"""
        print("👋 Fermeture du jeu...")
        
        # Sauvegarder avant de quitter
        if self.game:
            self.save_game_data()
        
        # Terminer la session
        self.save_system.end_session()
        
        # Afficher les statistiques finales
        stats = self.save_system.get_statistics_summary()
        print("\n📊 Statistiques de session:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        print("\n✨ Merci d'avoir joué à Éclats d'Astralis !")
        
        self.running = False
    
    def run(self):
        """Boucle principale de l'application"""
        print("🚀 Lancement de l'application...")
        
        while self.running:
            # Gérer les événements
            self.handle_events()
            
            # Mettre à jour
            self.update()
            
            # Dessiner
            self.draw()
            
            # Limiter les FPS
            self.clock.tick(60)
        
        # Quitter Pygame
        pygame.quit()
        sys.exit()


def main():
    """Point d'entrée principal"""
    try:
        app = AstralisMain()
        app.run()
    except KeyboardInterrupt:
        print("\n⚠️ Interruption par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main() 