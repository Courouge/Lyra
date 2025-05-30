import random
import math
import pygame
from settings import *
from entities.platform import Platform
from entities.star_fragment import StarFragment
from entities.shadow import Shadow
from entities.end_portal import EndPortal

class SpectralForestGenerator:
    """Générateur pour la Forêt Spectrale avec mécaniques spéciales"""
    
    def __init__(self):
        self.platforms = []
        self.star_fragments = []
        self.shadows = []
        self.phantom_trees = []
        self.floating_leaves = []
        self.mystical_orbs = []
        self.last_platform_x = 0
        self.last_platform_y = SCREEN_HEIGHT // 2
        self.difficulty = 1.2
        
        # Système de fin de niveau
        self.level_length = 6000
        self.end_platform_created = False
        self.end_portal = None
        
        # Couleurs spéciales pour la forêt spectrale
        self.colors = {
            'background': (10, 25, 15),
            'platform': (60, 120, 80),
            'moving_platform': (80, 150, 100),
            'ambient': (100, 200, 150),
            'phantom': (80, 255, 120, 100),
            'mystical': (120, 255, 180)
        }
        
        # Générer la plateforme de départ
        start_platform = Platform(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH // 2, 30)
        start_platform.color = self.colors['platform']
        self.platforms.append(start_platform)
        self.last_platform_x = start_platform.x + start_platform.width
        self.last_platform_y = start_platform.y
        
    def generate_chunk(self, camera_x):
        """Génère un nouveau chunk avec mécaniques de forêt spectrale"""
        chunk_start = int(camera_x + SCREEN_WIDTH)
        chunk_end = int(chunk_start + SCREEN_WIDTH)
        
        # Nettoyer les éléments hors de l'écran
        self.cleanup_offscreen_elements(camera_x)
        
        # Générer des plateformes (normales et mobiles)
        while self.last_platform_x < chunk_end:
            if random.random() < 0.3:  # 30% de chance de plateforme mobile
                self.generate_moving_platform()
            else:
                self.generate_next_platform()
                
        # Générer des arbres fantômes
        self.generate_phantom_trees(chunk_start, chunk_end)
        
        # Générer des feuilles flottantes
        self.generate_floating_leaves(chunk_start, chunk_end)
        
        # Générer des orbes mystiques
        self.generate_mystical_orbs(chunk_start, chunk_end)
        
        # Générer des fragments d'étoiles
        self.generate_star_fragments(chunk_start, chunk_end)
        
        # Générer des ombres spectrales
        self.generate_spectral_shadows(chunk_start, chunk_end)
    
    def generate_next_platform(self):
        """Génère une plateforme normale avec style forêt"""
        base_spacing = PLATFORM_SPACING_X * 0.8  # Légèrement plus rapprochées
        
        spacing_x = int(base_spacing + random.randint(-25, 25))
        spacing_x = max(70, spacing_x)
        
        # Variation verticale plus organique (comme des branches)
        max_jump_height = 90
        spacing_y = random.randint(-max_jump_height, max_jump_height)
        
        new_x = int(self.last_platform_x + spacing_x)
        new_y = int(self.last_platform_y + spacing_y)
        new_y = max(50, min(SCREEN_HEIGHT - 50, new_y))
        
        # Validation de saut
        if spacing_x > 150 or abs(new_y - self.last_platform_y) > 120:
            spacing_x = min(spacing_x, 140)
            new_x = int(self.last_platform_x + spacing_x)
            if new_y > self.last_platform_y:
                new_y = min(new_y, self.last_platform_y + 100)
            else:
                new_y = max(new_y, self.last_platform_y - 100)
        
        # Plateformes de style organique
        platform_width = PLATFORM_WIDTH + random.randint(-10, 50)
        platform_width = max(90, platform_width)
        
        platform = OrganicPlatform(new_x, new_y, platform_width)
        self.platforms.append(platform)
        
        self.last_platform_x = new_x + platform_width
        self.last_platform_y = new_y
    
    def generate_moving_platform(self):
        """Génère une plateforme mobile (branche flottante) - CORRIGÉ"""
        spacing_x = random.randint(120, 180)
        new_x = int(self.last_platform_x + spacing_x)
        new_y = int(self.last_platform_y + random.randint(-60, 60))
        new_y = max(100, min(SCREEN_HEIGHT - 100, new_y))
        
        # CORRECTION : Créer une plateforme mobile qui hérite de Platform
        platform = MovingPlatform(new_x, new_y, 120, 25)
        # IMPORTANT : Ajouter à la liste principale des plateformes pour les collisions
        self.platforms.append(platform)
        
        self.last_platform_x = new_x + 120
        self.last_platform_y = new_y
    
    def generate_phantom_trees(self, chunk_start, chunk_end):
        """Génère des arbres fantômes décoratifs"""
        num_trees = random.randint(3, 7)  # Plus d'arbres
        for _ in range(num_trees):
            tree_x = random.randint(chunk_start, chunk_end)
            tree_y = random.randint(200, SCREEN_HEIGHT - 50)
            
            tree = PhantomTree(tree_x, tree_y)
            self.phantom_trees.append(tree)
    
    def generate_floating_leaves(self, chunk_start, chunk_end):
        """Génère des feuilles flottantes pour l'ambiance"""
        num_leaves = random.randint(5, 12)
        for _ in range(num_leaves):
            leaf_x = random.randint(chunk_start, chunk_end)
            leaf_y = random.randint(50, SCREEN_HEIGHT - 50)
            
            leaf = FloatingLeaf(leaf_x, leaf_y)
            self.floating_leaves.append(leaf)
    
    def generate_mystical_orbs(self, chunk_start, chunk_end):
        """Génère des orbes mystiques pour l'éclairage ambiant"""
        num_orbs = random.randint(2, 5)
        for _ in range(num_orbs):
            orb_x = random.randint(chunk_start, chunk_end)
            orb_y = random.randint(100, SCREEN_HEIGHT - 100)
            
            orb = MysticalOrb(orb_x, orb_y)
            self.mystical_orbs.append(orb)
    
    def generate_star_fragments(self, chunk_start, chunk_end):
        """Génère des fragments avec style forêt spectrale"""
        for platform in self.platforms:
            if chunk_start <= platform.x <= chunk_end:
                if random.random() < 0.4:  # Plus de fragments dans la forêt
                    star_x = platform.x + platform.width // 2 + random.randint(-15, 15)
                    star_y = platform.y - 40 - random.randint(0, 20)
                    
                    if self.is_star_reachable(star_x, star_y, platform):
                        star = StarFragment(star_x, star_y)
                        star.color = (150, 255, 180)  # Vert lumineux
                        self.star_fragments.append(star)
    
    def generate_spectral_shadows(self, chunk_start, chunk_end):
        """Génère des ombres spectrales plus agressives"""
        num_shadows = int(self.difficulty * 2.5)
        
        for _ in range(num_shadows):
            if random.random() < 0.25:
                attempts = 0
                while attempts < 10:
                    shadow_x = random.randint(chunk_start, chunk_end)
                    shadow_y = random.randint(150, SCREEN_HEIGHT - 150)
                    
                    if self.is_shadow_position_valid(shadow_x, shadow_y):
                        shadow = SpectralShadow(shadow_x, shadow_y)
                        self.shadows.append(shadow)
                        break
                    attempts += 1
    
    def is_star_reachable(self, star_x, star_y, source_platform):
        """Vérifie l'accessibilité des fragments"""
        platform_center_x = source_platform.x + source_platform.width // 2
        horizontal_distance = abs(star_x - platform_center_x)
        vertical_distance = source_platform.y - star_y
        
        return (horizontal_distance <= source_platform.width // 2 + 40 and 
                0 <= vertical_distance <= 80)
    
    def is_shadow_position_valid(self, shadow_x, shadow_y):
        """Vérifie la validité des positions d'ombres"""
        closest_platform = None
        min_distance = float('inf')
        
        for platform in self.platforms:
            platform_center_x = platform.x + platform.width // 2
            distance = abs(shadow_x - platform_center_x)
            if distance < min_distance:
                min_distance = distance
                closest_platform = platform
        
        if closest_platform is None:
            return False
        
        platform_center_x = closest_platform.x + closest_platform.width // 2
        horizontal_distance = abs(shadow_x - platform_center_x)
        vertical_distance = abs(shadow_y - closest_platform.y)
        
        return (horizontal_distance <= 200 and vertical_distance <= 150)
    
    def cleanup_offscreen_elements(self, camera_x):
        """Nettoie les éléments hors écran"""
        cleanup_threshold = camera_x - SCREEN_WIDTH
        
        self.platforms = [p for p in self.platforms if p.x + p.width > cleanup_threshold]
        self.phantom_trees = [t for t in self.phantom_trees if t.x > cleanup_threshold]
        self.floating_leaves = [l for l in self.floating_leaves if l.x > cleanup_threshold]
        self.mystical_orbs = [o for o in self.mystical_orbs if o.x > cleanup_threshold]
        self.star_fragments = [s for s in self.star_fragments if s.x > cleanup_threshold and not s.collected]
        self.shadows = [s for s in self.shadows if s.x > cleanup_threshold and s.active]
    
    def update(self, camera_x):
        """Met à jour tous les éléments"""
        camera_x = int(camera_x)
        
        if not self.end_platform_created and camera_x > self.level_length - SCREEN_WIDTH * 2:
            self.create_end_platform()
            
        if camera_x + SCREEN_WIDTH * 2 > self.last_platform_x and not self.end_platform_created:
            self.generate_chunk(camera_x)
        
        # Mettre à jour tous les éléments
        for platform in self.platforms:
            platform.update()
        for tree in self.phantom_trees:
            tree.update()
        for leaf in self.floating_leaves:
            leaf.update()
        for orb in self.mystical_orbs:
            orb.update()
        for star in self.star_fragments:
            star.update()
        for shadow in self.shadows:
            shadow.update()
        if self.end_portal:
            self.end_portal.update()
    
    def create_end_platform(self):
        """Crée la fin de niveau avec style forêt"""
        # Plateformes d'approche
        for i in range(3):
            approach_x = self.level_length - 400 + (i * 120)
            approach_y = SCREEN_HEIGHT // 2 + random.randint(-30, 30)
            approach_platform = OrganicPlatform(approach_x, approach_y, 120, 30)
            self.platforms.append(approach_platform)
        
        # Plateforme finale
        end_x = self.level_length - 50
        end_y = SCREEN_HEIGHT // 2
        end_platform = OrganicPlatform(end_x, end_y, 250, 50)
        end_platform.color = (100, 200, 120)  # Vert brillant
        end_platform.is_end_platform = True
        self.platforms.append(end_platform)
        
        self.end_portal = EndPortal(end_x + 125, end_y - 60)
        self.end_platform_created = True
    
    def check_level_completion(self, lyra):
        """Vérifie la fin de niveau"""
        if self.end_portal and self.end_portal.check_collision(lyra):
            return True
        return False
    
    def draw(self, screen, camera_x):
        """Dessine tous les éléments avec style forêt spectrale"""
        # Dessiner le fond de forêt spectrale
        self.draw_forest_background(screen, camera_x)
        
        # Dessiner les orbes mystiques en arrière-plan
        for orb in self.mystical_orbs:
            orb.draw(screen, camera_x)
        
        # Dessiner les arbres fantômes en arrière-plan
        for tree in self.phantom_trees:
            tree.draw(screen, camera_x)
        
        # Dessiner les feuilles flottantes
        for leaf in self.floating_leaves:
            leaf.draw(screen, camera_x)
        
        # Dessiner les plateformes
        for platform in self.platforms:
            platform.draw(screen, camera_x)
        
        # Dessiner les fragments
        for star in self.star_fragments:
            star.draw(screen, camera_x)
        
        # Dessiner les ombres
        for shadow in self.shadows:
            shadow.draw(screen, camera_x)
            
        # Dessiner le portail
        if self.end_portal:
            self.end_portal.draw(screen, camera_x)
        
        # Effet de brouillard mystique
        self.draw_mystical_fog(screen, camera_x)
    
    def draw_forest_background(self, screen, camera_x):
        """Dessine le fond de forêt spectrale"""
        # Gradient de fond vert mystique
        for y in range(0, SCREEN_HEIGHT, 4):
            intensity = int(10 + (y / SCREEN_HEIGHT) * 15)
            color = (intensity, intensity * 2, intensity)
            pygame.draw.rect(screen, color, (0, y, SCREEN_WIDTH, 4))
        
        # Lignes de brume horizontales
        for i in range(5):
            mist_y = (i * SCREEN_HEIGHT // 5) + int(math.sin(camera_x * 0.001 + i) * 20)
            mist_alpha = 30 + int(math.sin(camera_x * 0.002 + i) * 10)
            mist_surface = pygame.Surface((SCREEN_WIDTH, 40), pygame.SRCALPHA)
            mist_surface.fill((80, 255, 120, mist_alpha))
            screen.blit(mist_surface, (0, mist_y))
    
    def draw_mystical_fog(self, screen, camera_x):
        """Dessine un effet de brouillard mystique au premier plan"""
        fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Particules de brouillard
        for i in range(20):
            fog_x = (camera_x * 0.1 + i * 60) % SCREEN_WIDTH
            fog_y = 50 + i * 30 + int(math.sin(camera_x * 0.003 + i) * 15)
            fog_size = 30 + int(math.sin(camera_x * 0.002 + i) * 10)
            fog_alpha = 20 + int(math.sin(camera_x * 0.001 + i) * 10)
            
            fog_color = (100, 200, 150, fog_alpha)
            pygame.draw.circle(fog_surface, fog_color, (int(fog_x), int(fog_y)), fog_size)
        
        screen.blit(fog_surface, (0, 0))


class OrganicPlatform(Platform):
    """Plateforme organique pour la forêt spectrale"""
    
    def __init__(self, x, y, width, height=20):
        super().__init__(x, y, width, height)
        self.color = (60, 120, 80)
        self.moss_spots = []
        self.growth_offset = random.random() * 2 * math.pi
        
        # Générer des spots de mousse
        for _ in range(random.randint(2, 5)):
            moss_x = random.randint(0, width)
            moss_y = random.randint(0, height)
            moss_size = random.randint(3, 8)
            self.moss_spots.append((moss_x, moss_y, moss_size))
    
    def update(self):
        """Met à jour les effets organiques"""
        super().update()
        self.growth_offset += 0.02
    
    def draw(self, screen, camera_x):
        """Dessine la plateforme organique"""
        draw_x = self.x - camera_x
        
        if draw_x + self.width >= 0 and draw_x <= SCREEN_WIDTH:
            # Plateforme de base avec texture organique
            base_color = self.color
            pygame.draw.rect(screen, base_color, (draw_x, self.y, self.width, self.height))
            
            # Bordure plus sombre
            border_color = (40, 80, 60)
            pygame.draw.rect(screen, border_color, (draw_x, self.y, self.width, self.height), 2)
            
            # Spots de mousse
            for moss_x, moss_y, moss_size in self.moss_spots:
                moss_color = (80, 150, 100)
                actual_size = moss_size + int(math.sin(self.growth_offset) * 2)
                pygame.draw.circle(screen, moss_color, 
                                 (int(draw_x + moss_x), int(self.y + moss_y)), 
                                 max(1, actual_size))
            
            # Effet de croissance sur les bords
            growth_intensity = int(10 + math.sin(self.growth_offset) * 5)
            growth_color = (100, 180, 120, growth_intensity)
            growth_surface = pygame.Surface((self.width, 4), pygame.SRCALPHA)
            growth_surface.fill(growth_color)
            screen.blit(growth_surface, (draw_x, self.y - 2))


class MovingPlatform(Platform):
    """Plateforme mobile pour la forêt spectrale - CORRIGÉE"""
    
    def __init__(self, x, y, width=120, height=25):
        super().__init__(x, y, width, height)
        self.color = (80, 150, 100)
        
        # Mouvement
        self.start_y = y
        self.move_range = 60
        self.move_speed = 0.02
        self.move_offset = random.random() * 2 * math.pi
        
        # Effets visuels
        self.glow_offset = 0
        
    def update(self):
        """Met à jour le mouvement de la plateforme"""
        super().update()  # Appeler la méthode parent
        self.move_offset += self.move_speed
        self.y = self.start_y + math.sin(self.move_offset) * self.move_range
        self.glow_offset += 0.1
    
    def draw(self, screen, camera_x):
        """Dessine la plateforme mobile"""
        draw_x = self.x - camera_x
        
        if draw_x + self.width >= 0 and draw_x <= SCREEN_WIDTH:
            # Aura de mouvement
            glow_intensity = 20 + math.sin(self.glow_offset) * 10
            glow_surface = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
            
            for i in range(5):
                glow_color = (*self.color, max(0, min(255, int(glow_intensity - i * 5))))
                pygame.draw.rect(glow_surface, glow_color, 
                               (10 - i * 2, 10 - i * 2, self.width + i * 4, self.height + i * 4))
            
            screen.blit(glow_surface, (draw_x - 10, self.y - 10))
            
            # Plateforme principale
            pygame.draw.rect(screen, self.color, (draw_x, self.y, self.width, self.height))
            
            # Détails organiques
            for i in range(3):
                detail_x = draw_x + (i + 1) * (self.width // 4)
                detail_y = self.y + self.height // 2
                pygame.draw.circle(screen, (100, 180, 120), (int(detail_x), int(detail_y)), 3)


class PhantomTree:
    """Arbre fantôme décoratif amélioré"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = random.randint(120, 250)
        self.width = random.randint(25, 50)
        self.transparency = random.randint(40, 90)
        self.sway_offset = random.random() * 2 * math.pi
        self.sway_speed = random.uniform(0.01, 0.03)
        self.glow_offset = random.random() * 2 * math.pi
        
    def update(self):
        """Met à jour l'animation de l'arbre"""
        self.sway_offset += self.sway_speed
        self.glow_offset += 0.05
    
    def draw(self, screen, camera_x):
        """Dessine l'arbre fantôme amélioré"""
        draw_x = self.x - camera_x
        
        if draw_x + self.width >= 0 and draw_x <= SCREEN_WIDTH:
            # Balancement
            sway = math.sin(self.sway_offset) * 8
            
            # Aura mystique
            glow_intensity = 30 + int(math.sin(self.glow_offset) * 15)
            glow_surface = pygame.Surface((self.width * 3, self.height + 50), pygame.SRCALPHA)
            glow_color = (80, 255, 120, glow_intensity)
            pygame.draw.ellipse(glow_surface, glow_color, 
                              (0, 0, self.width * 3, self.height + 50))
            screen.blit(glow_surface, (draw_x - self.width + sway, self.y - self.height - 25))
            
            # Tronc
            trunk_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            trunk_color = (60, 40, 20, self.transparency)
            pygame.draw.rect(trunk_surface, trunk_color, (0, 0, self.width, self.height))
            screen.blit(trunk_surface, (draw_x + sway, self.y - self.height))
            
            # Feuillage fantôme
            foliage_size = self.width * 2.5
            foliage_surface = pygame.Surface((foliage_size, foliage_size), pygame.SRCALPHA)
            foliage_color = (80, 255, 120, self.transparency // 2)
            pygame.draw.circle(foliage_surface, foliage_color, 
                             (int(foliage_size // 2), int(foliage_size // 2)), int(foliage_size // 2))
            screen.blit(foliage_surface, (draw_x - foliage_size // 4 + sway, 
                                        self.y - self.height - foliage_size // 2))


class FloatingLeaf:
    """Feuille flottante pour l'ambiance"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_y = y
        self.float_range = random.randint(20, 40)
        self.float_speed = random.uniform(0.01, 0.03)
        self.float_offset = random.random() * 2 * math.pi
        self.drift_speed = random.uniform(0.2, 0.5)
        self.size = random.randint(3, 8)
        self.rotation = 0
        self.rotation_speed = random.uniform(0.02, 0.05)
        
    def update(self):
        """Met à jour le mouvement de la feuille"""
        self.float_offset += self.float_speed
        self.y = self.start_y + math.sin(self.float_offset) * self.float_range
        self.x -= self.drift_speed  # Dérive lente vers la gauche
        self.rotation += self.rotation_speed
    
    def draw(self, screen, camera_x):
        """Dessine la feuille flottante"""
        draw_x = self.x - camera_x
        
        if draw_x + self.size >= 0 and draw_x <= SCREEN_WIDTH:
            # Créer une surface pour la feuille avec rotation
            leaf_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            leaf_color = (100, 200, 120, 180)
            
            # Dessiner la forme de feuille
            points = [
                (self.size, 0),
                (self.size * 1.5, self.size // 2),
                (self.size, self.size * 2),
                (self.size // 2, self.size // 2)
            ]
            pygame.draw.polygon(leaf_surface, leaf_color, points)
            
            # Rotation
            rotated_surface = pygame.transform.rotate(leaf_surface, math.degrees(self.rotation))
            rect = rotated_surface.get_rect(center=(draw_x, self.y))
            screen.blit(rotated_surface, rect)


class MysticalOrb:
    """Orbe mystique pour l'éclairage ambiant"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_y = y
        self.pulse_offset = random.random() * 2 * math.pi
        self.pulse_speed = random.uniform(0.02, 0.04)
        self.float_range = random.randint(10, 25)
        self.base_size = random.randint(8, 15)
        self.color_shift = random.random() * 2 * math.pi
        
    def update(self):
        """Met à jour l'animation de l'orbe"""
        self.pulse_offset += self.pulse_speed
        self.color_shift += 0.03
        self.y = self.start_y + math.sin(self.pulse_offset * 0.5) * self.float_range
    
    def draw(self, screen, camera_x):
        """Dessine l'orbe mystique"""
        draw_x = self.x - camera_x
        
        if draw_x + self.base_size >= 0 and draw_x <= SCREEN_WIDTH:
            # Taille pulsante
            size = self.base_size + int(math.sin(self.pulse_offset) * 3)
            
            # Couleur changeante
            color_r = 120 + int(math.sin(self.color_shift) * 30)
            color_g = 255
            color_b = 180 + int(math.cos(self.color_shift) * 40)
            
            # Aura externe
            for i in range(4):
                aura_alpha = max(0, min(255, 20 - i * 5))
                if aura_alpha > 0:
                    aura_size = size + (3 - i) * 8
                    aura_surface = pygame.Surface((aura_size * 2, aura_size * 2), pygame.SRCALPHA)
                    aura_color = (color_r, color_g, color_b, aura_alpha)
                    pygame.draw.circle(aura_surface, aura_color, (aura_size, aura_size), aura_size)
                    screen.blit(aura_surface, (draw_x - aura_size, self.y - aura_size))
            
            # Orbe central
            pygame.draw.circle(screen, (color_r, color_g, color_b), (int(draw_x), int(self.y)), size)
            pygame.draw.circle(screen, (255, 255, 255), (int(draw_x), int(self.y)), size // 2)


class SpectralShadow(Shadow):
    """Ombre spectrale avec comportement spécial"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (40, 20, 60)  # Violet spectral
        self.phase_speed = 0.05
        self.phase_offset = random.random() * 2 * math.pi
        
    def update(self):
        """Met à jour l'ombre spectrale"""
        super().update()
        self.phase_offset += self.phase_speed
        
        # Mouvement de phase (apparition/disparition)
        self.transparency = 0.5 + 0.3 * math.sin(self.phase_offset)
    
    def draw(self, screen, camera_x):
        """Dessine l'ombre spectrale avec effet de phase"""
        if not self.active:
            return
            
        draw_x = self.x - camera_x
        
        if draw_x + self.darkness_radius >= 0 and draw_x - self.darkness_radius <= SCREEN_WIDTH:
            # Effet de phase avec transparence variable
            phase_alpha = int(100 * self.transparency)
            
            # Aura spectrale
            for i in range(4):
                aura_alpha = max(0, min(255, 20 - i * 5))
                if aura_alpha > 0:
                    radius = self.darkness_radius + i * 10
                    shadow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    shadow_color = (*self.color, aura_alpha)
                    pygame.draw.circle(shadow_surface, shadow_color, (radius, radius), radius)
                    screen.blit(shadow_surface, (draw_x - radius, self.y - radius))
            
            # Noyau central
            core_color = (60, 40, 80, phase_alpha)
            core_surface = pygame.Surface((self.darkness_radius, self.darkness_radius), pygame.SRCALPHA)
            pygame.draw.circle(core_surface, core_color, 
                             (self.darkness_radius // 2, self.darkness_radius // 2), 
                             self.darkness_radius // 2)
            screen.blit(core_surface, (draw_x - self.darkness_radius // 2, 
                                     self.y - self.darkness_radius // 2)) 