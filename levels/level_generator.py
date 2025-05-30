import random
import math
from settings import *
from entities.platform import Platform
from entities.star_fragment import StarFragment
from entities.shadow import Shadow
from entities.end_portal import EndPortal

class LevelGenerator:
    def __init__(self):
        self.platforms = []
        self.star_fragments = []
        self.shadows = []
        self.last_platform_x = 0
        self.last_platform_y = SCREEN_HEIGHT // 2
        self.difficulty = 1.0
        
        # Système de fin de niveau
        self.level_length = 6000  # Réduit de 8000 à 6000 pixels
        self.end_platform_created = False
        self.end_portal = None
        
        # Générer la plateforme de départ
        start_platform = Platform(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH // 2, 30)
        self.platforms.append(start_platform)
        self.last_platform_x = start_platform.x + start_platform.width
        self.last_platform_y = start_platform.y
        
    def update_difficulty(self, distance_traveled):
        """Met à jour la difficulté basée sur la distance parcourue"""
        self.difficulty = 1.0 + (distance_traveled / 2000) * 0.5
        
    def generate_chunk(self, camera_x):
        """Génère un nouveau chunk de niveau"""
        chunk_start = int(camera_x + SCREEN_WIDTH)
        chunk_end = int(chunk_start + SCREEN_WIDTH)
        
        # Nettoyer les éléments hors de l'écran
        self.cleanup_offscreen_elements(camera_x)
        
        # Générer de nouvelles plateformes
        while self.last_platform_x < chunk_end:
            self.generate_next_platform()
            
        # Générer des fragments d'étoiles
        self.generate_star_fragments(chunk_start, chunk_end)
        
        # Générer des ombres astrales
        self.generate_shadows(chunk_start, chunk_end)
    
    def generate_next_platform(self):
        """Génère la prochaine plateforme avec plus de variété"""
        # Espacement horizontal avec plus de variété - RÉDUIT pour éviter les sauts impossibles
        base_spacing = PLATFORM_SPACING_X * 0.7  # Réduction de 30%
        
        # Créer des sections avec des thèmes différents
        section_type = (int(self.last_platform_x / 800) % 4)  # 4 types de sections
        
        if section_type == 0:  # Section normale
            spacing_x = int(base_spacing + random.randint(-20, 20))  # Réduit de -30,30 à -20,20
            spacing_x = max(60, spacing_x)  # Réduit de 80 à 60
            max_jump_height = int(80 + (self.difficulty - 1) * 20)  # Réduit de 120 à 80
            
        elif section_type == 1:  # Section rapprochée (plus facile)
            spacing_x = int(base_spacing * 0.6 + random.randint(-15, 15))  # Plus rapprochée
            spacing_x = max(50, spacing_x)  # Réduit de 60 à 50
            max_jump_height = int(60 + (self.difficulty - 1) * 15)  # Réduit
            
        elif section_type == 2:  # Section éloignée (plus difficile) - LIMITÉE
            spacing_x = int(base_spacing * 0.9 + random.randint(-25, 25))  # Réduit de 1.3 à 0.9
            spacing_x = max(70, spacing_x)  # Réduit de 100 à 70
            max_jump_height = int(100 + (self.difficulty - 1) * 25)  # Réduit
            
        else:  # Section verticale (sauts en hauteur)
            spacing_x = int(base_spacing * 0.7 + random.randint(-20, 20))
            spacing_x = max(55, spacing_x)  # Réduit de 70 à 55
            max_jump_height = int(120 + (self.difficulty - 1) * 30)  # Réduit de 200 à 120
        
        spacing_y = random.randint(-max_jump_height, max_jump_height)
        
        # Nouvelle position
        new_x = int(self.last_platform_x + spacing_x)
        new_y = int(self.last_platform_y + spacing_y)
        
        # Limiter la hauteur
        new_y = max(50, min(SCREEN_HEIGHT - 50, new_y))
        
        # VALIDATION : Vérifier que le saut est possible
        # Distance horizontale maximale qu'on peut sauter (approximation)
        max_jump_distance = 150  # Basé sur la vitesse et la force de saut de Lyra
        max_jump_height_diff = 120  # Différence de hauteur maximale
        
        actual_distance = spacing_x
        actual_height_diff = abs(new_y - self.last_platform_y)
        
        # Si le saut est trop difficile, ajuster
        if actual_distance > max_jump_distance or actual_height_diff > max_jump_height_diff:
            # Réduire la distance et la hauteur
            spacing_x = min(spacing_x, max_jump_distance - 20)
            new_x = int(self.last_platform_x + spacing_x)
            
            # Ajuster la hauteur pour qu'elle soit atteignable
            if new_y > self.last_platform_y:
                new_y = min(new_y, self.last_platform_y + max_jump_height_diff)
            else:
                new_y = max(new_y, self.last_platform_y - max_jump_height_diff)
        
        # Taille variable de plateforme selon la section - PLUS GRANDES
        if section_type == 1:  # Plateformes plus larges pour section facile
            platform_width = PLATFORM_WIDTH + random.randint(20, 80)  # Augmenté
        elif section_type == 2:  # Plateformes plus petites pour section difficile
            platform_width = PLATFORM_WIDTH + random.randint(-20, 40)  # Augmenté
        else:
            platform_width = PLATFORM_WIDTH + random.randint(0, 60)  # Augmenté
            
        platform_width = max(100, platform_width)  # Augmenté de 80 à 100
        
        # Créer la plateforme
        platform = Platform(new_x, new_y, platform_width)
        self.platforms.append(platform)
        
        # Mettre à jour la position de référence
        self.last_platform_x = new_x + platform_width
        self.last_platform_y = new_y
        
    def generate_star_fragments(self, chunk_start, chunk_end):
        """Génère des fragments d'étoiles dans le chunk - VERSION AMÉLIORÉE"""
        for platform in self.platforms:
            if chunk_start <= platform.x <= chunk_end:
                # Chance de spawn basée sur la difficulté
                spawn_chance = STAR_SPAWN_CHANCE * (1 + self.difficulty * 0.2)
                
                if random.random() < spawn_chance:
                    # Position au-dessus de la plateforme - PLUS ACCESSIBLE
                    star_x = platform.x + platform.width // 2 + random.randint(-20, 20)  # Réduit de -30,30 à -20,20
                    star_y = platform.y - 35 - random.randint(0, 15)  # Réduit de -50,-30 à -35,-15
                    
                    # NOUVELLE VALIDATION : S'assurer que le fragment est atteignable
                    if self.is_star_reachable(star_x, star_y, platform):
                        # Vérifier qu'il n'y a pas déjà un fragment proche
                        too_close = False
                        for existing_star in self.star_fragments:
                            distance = math.sqrt((star_x - existing_star.x)**2 + (star_y - existing_star.y)**2)
                            if distance < 60:
                                too_close = True
                                break
                        
                        if not too_close:
                            star = StarFragment(star_x, star_y)
                            self.star_fragments.append(star)
    
    def is_star_reachable(self, star_x, star_y, source_platform):
        """Vérifie si un fragment d'étoile est atteignable depuis une plateforme"""
        # Distance horizontale depuis le centre de la plateforme
        platform_center_x = source_platform.x + source_platform.width // 2
        horizontal_distance = abs(star_x - platform_center_x)
        
        # Hauteur au-dessus de la plateforme
        vertical_distance = source_platform.y - star_y
        
        # Critères d'accessibilité
        max_horizontal_reach = source_platform.width // 2 + 40  # Peut s'étendre un peu au-delà
        max_vertical_reach = 80  # Hauteur de saut maximale
        
        # Le fragment doit être dans une zone atteignable
        return (horizontal_distance <= max_horizontal_reach and 
                0 <= vertical_distance <= max_vertical_reach)
    
    def generate_shadows(self, chunk_start, chunk_end):
        """Génère des ombres astrales dans le chunk - VERSION AMÉLIORÉE"""
        num_shadows = int(self.difficulty * 2)
        
        for _ in range(num_shadows):
            if random.random() < SHADOW_SPAWN_CHANCE:
                # Essayer plusieurs positions pour trouver une position valide
                attempts = 0
                max_attempts = 10
                
                while attempts < max_attempts:
                    shadow_x = random.randint(chunk_start, chunk_end)
                    shadow_y = random.randint(150, SCREEN_HEIGHT - 150)  # Zone plus restreinte
                    
                    # NOUVELLE VALIDATION : Vérifier que l'ombre est dans une zone accessible
                    if self.is_shadow_position_valid(shadow_x, shadow_y):
                        # Vérifier qu'il n'y a pas de plateforme trop proche
                        too_close_to_platform = False
                        for platform in self.platforms:
                            distance = math.sqrt((shadow_x - platform.x)**2 + (shadow_y - platform.y)**2)
                            if distance < 80:  # Réduit de 100 à 80
                                too_close_to_platform = True
                                break
                        
                        # Vérifier qu'il n'y a pas d'autre ombre trop proche
                        too_close_to_shadow = False
                        for existing_shadow in self.shadows:
                            distance = math.sqrt((shadow_x - existing_shadow.x)**2 + (shadow_y - existing_shadow.y)**2)
                            if distance < 80:
                                too_close_to_shadow = True
                                break
                        
                        if not too_close_to_platform and not too_close_to_shadow:
                            shadow = Shadow(shadow_x, shadow_y)
                            self.shadows.append(shadow)
                            break  # Position valide trouvée
                    
                    attempts += 1
    
    def is_shadow_position_valid(self, shadow_x, shadow_y):
        """Vérifie si une position d'ombre est dans une zone accessible au joueur"""
        # Trouver la plateforme la plus proche
        closest_platform = None
        min_distance = float('inf')
        
        for platform in self.platforms:
            # Distance horizontale au centre de la plateforme
            platform_center_x = platform.x + platform.width // 2
            distance = abs(shadow_x - platform_center_x)
            
            if distance < min_distance:
                min_distance = distance
                closest_platform = platform
        
        if closest_platform is None:
            return False
        
        # L'ombre doit être dans une zone où le joueur peut aller
        platform_center_x = closest_platform.x + closest_platform.width // 2
        horizontal_distance = abs(shadow_x - platform_center_x)
        vertical_distance = abs(shadow_y - closest_platform.y)
        
        # Zone accessible : pas trop loin horizontalement et à une hauteur raisonnable
        max_horizontal_distance = 200  # Distance maximale depuis une plateforme
        max_vertical_distance = 150   # Hauteur maximale/minimale
        
        return (horizontal_distance <= max_horizontal_distance and 
                vertical_distance <= max_vertical_distance)
    
    def cleanup_offscreen_elements(self, camera_x):
        """Nettoie les éléments hors de l'écran"""
        cleanup_threshold = camera_x - SCREEN_WIDTH
        
        # Nettoyer les plateformes
        self.platforms = [p for p in self.platforms if p.x + p.width > cleanup_threshold]
        
        # Nettoyer les fragments d'étoiles
        self.star_fragments = [s for s in self.star_fragments if s.x > cleanup_threshold and not s.collected]
        
        # Nettoyer les ombres
        self.shadows = [s for s in self.shadows if s.x > cleanup_threshold and s.active]
    
    def get_platforms_in_range(self, x_start, x_end):
        """Retourne les plateformes dans une plage donnée"""
        return [p for p in self.platforms if p.x < x_end and p.x + p.width > x_start]
    
    def update(self, camera_x):
        """Met à jour tous les éléments du niveau"""
        # Convertir camera_x en entier pour éviter les erreurs float
        camera_x = int(camera_x)
        
        # Créer la plateforme de fin si on approche de la fin du niveau
        if not self.end_platform_created and camera_x > self.level_length - SCREEN_WIDTH * 2:
            self.create_end_platform()
            
        # Générer de nouveaux chunks si nécessaire (seulement si pas encore à la fin)
        if camera_x + SCREEN_WIDTH * 2 > self.last_platform_x and not self.end_platform_created:
            self.generate_chunk(camera_x)
        
        # Mettre à jour la difficulté
        self.update_difficulty(camera_x)
        
        # Mettre à jour les plateformes
        for platform in self.platforms:
            platform.update()
        
        # Mettre à jour les fragments d'étoiles
        for star in self.star_fragments:
            star.update()
        
        # Mettre à jour les ombres
        for shadow in self.shadows:
            shadow.update()
            
        # Mettre à jour le portail de fin
        if self.end_portal:
            self.end_portal.update()
    
    def create_end_platform(self):
        """Crée la plateforme de fin avec le portail"""
        # Créer des plateformes intermédiaires pour faciliter l'accès
        approach_distance = 400  # Distance d'approche
        num_approach_platforms = 3
        
        for i in range(num_approach_platforms):
            # Plateformes d'approche avec espacement réduit
            approach_x = self.level_length - approach_distance + (i * 120)
            approach_y = SCREEN_HEIGHT // 2 + random.randint(-30, 30)
            approach_platform = Platform(approach_x, approach_y, 120, 30)
            self.platforms.append(approach_platform)
        
        # Grande plateforme de fin - PLUS ACCESSIBLE
        end_x = self.level_length - 50  # Plus proche du bord
        end_y = SCREEN_HEIGHT // 2
        end_platform = Platform(end_x, end_y, 250, 50)  # Plus large et plus haute
        end_platform.is_end_platform = True  # Marquer comme plateforme de fin
        self.platforms.append(end_platform)
        
        # Créer le portail de fin - PLUS BAS pour être accessible
        self.end_portal = EndPortal(end_x + 125, end_y - 60)  # Centré et plus bas
        self.end_platform_created = True
    
    def check_level_completion(self, lyra):
        """Vérifie si Lyra a atteint le portail de fin"""
        if self.end_portal and self.end_portal.check_collision(lyra):
            return True
        return False
    
    def draw(self, screen, camera_x):
        """Dessine tous les éléments du niveau"""
        # Dessiner les plateformes
        for platform in self.platforms:
            platform.draw(screen, camera_x)
        
        # Dessiner les fragments d'étoiles
        for star in self.star_fragments:
            star.draw(screen, camera_x)
        
        # Dessiner les ombres
        for shadow in self.shadows:
            shadow.draw(screen, camera_x)
            
        # Dessiner le portail de fin
        if self.end_portal:
            self.end_portal.draw(screen, camera_x) 