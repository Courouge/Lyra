import random
import math
import pygame
from settings import *
from entities.platform import Platform
from entities.star_fragment import StarFragment
from entities.shadow import Shadow
from entities.end_portal import EndPortal

class CelestialMirrorsGenerator:
    """Générateur pour les Miroirs Célestes avec portails et gravité inversée"""
    
    def __init__(self):
        self.platforms = []
        self.star_fragments = []
        self.shadows = []
        self.mirror_portals = []
        self.gravity_zones = []
        self.crystal_platforms = []
        self.floating_crystals = []
        self.portal_particles = []
        self.last_platform_x = 0
        self.last_platform_y = SCREEN_HEIGHT // 2
        self.difficulty = 1.5
        
        # Système de fin de niveau
        self.level_length = 7000
        self.end_platform_created = False
        self.end_portal = None
        
        # Couleurs spéciales pour les miroirs célestes
        self.colors = {
            'background': (15, 5, 30),
            'platform': (120, 80, 140),
            'crystal_platform': (180, 120, 255),
            'portal': (255, 120, 180),
            'gravity_zone': (120, 180, 255),
            'mirror': (200, 200, 255)
        }
        
        # Générer la plateforme de départ
        start_platform = CrystalPlatform(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH // 2, 30)
        self.platforms.append(start_platform)
        self.last_platform_x = start_platform.x + start_platform.width
        self.last_platform_y = start_platform.y
        
        # Générer le premier chunk pour avoir des éléments dès le début
        self.generate_chunk(0)
        
    def generate_chunk(self, camera_x):
        """Génère un nouveau chunk avec mécaniques de miroirs célestes"""
        chunk_start = int(camera_x + SCREEN_WIDTH)
        chunk_end = int(chunk_start + SCREEN_WIDTH)
        
        # Nettoyer les éléments hors de l'écran
        self.cleanup_offscreen_elements(camera_x)
        
        # Générer des plateformes (normales et cristallines)
        while self.last_platform_x < chunk_end:
            if random.random() < 0.4:  # 40% de chance de plateforme cristalline
                self.generate_crystal_platform()
            else:
                self.generate_next_platform()
                
        # Générer des portails miroirs
        self.generate_mirror_portals(chunk_start, chunk_end)
        
        # Générer des zones de gravité inversée
        self.generate_gravity_zones(chunk_start, chunk_end)
        
        # Générer des cristaux flottants
        self.generate_floating_crystals(chunk_start, chunk_end)
        
        # Générer des particules de portail
        self.generate_portal_particles(chunk_start, chunk_end)
        
        # Générer des fragments d'étoiles
        self.generate_star_fragments(chunk_start, chunk_end)
        
        # Générer des ombres cristallines
        self.generate_crystalline_shadows(chunk_start, chunk_end)
    
    def generate_next_platform(self):
        """Génère une plateforme normale avec style cristallin"""
        base_spacing = PLATFORM_SPACING_X * 0.9
        
        spacing_x = int(base_spacing + random.randint(-30, 30))
        spacing_x = max(80, spacing_x)
        
        # Variation verticale plus prononcée (effet de gravité variable)
        max_jump_height = 110
        spacing_y = random.randint(-max_jump_height, max_jump_height)
        
        new_x = int(self.last_platform_x + spacing_x)
        new_y = int(self.last_platform_y + spacing_y)
        new_y = max(50, min(SCREEN_HEIGHT - 50, new_y))
        
        # Validation de saut avec gravité variable
        if spacing_x > 160 or abs(new_y - self.last_platform_y) > 140:
            spacing_x = min(spacing_x, 150)
            new_x = int(self.last_platform_x + spacing_x)
            if new_y > self.last_platform_y:
                new_y = min(new_y, self.last_platform_y + 120)
            else:
                new_y = max(new_y, self.last_platform_y - 120)
        
        # Plateformes cristallines
        platform_width = PLATFORM_WIDTH + random.randint(-5, 40)
        platform_width = max(100, platform_width)
        
        platform = CrystalPlatform(new_x, new_y, platform_width)
        self.platforms.append(platform)
        
        self.last_platform_x = new_x + platform_width
        self.last_platform_y = new_y
    
    def generate_crystal_platform(self):
        """Génère une plateforme cristalline spéciale"""
        spacing_x = random.randint(100, 160)
        new_x = int(self.last_platform_x + spacing_x)
        new_y = int(self.last_platform_y + random.randint(-80, 80))
        new_y = max(80, min(SCREEN_HEIGHT - 80, new_y))
        
        platform = FloatingCrystalPlatform(new_x, new_y, 140, 25)
        self.platforms.append(platform)
        
        self.last_platform_x = new_x + 140
        self.last_platform_y = new_y
    
    def generate_mirror_portals(self, chunk_start, chunk_end):
        """Génère des portails miroirs pour la téléportation"""
        num_portals = random.randint(1, 2)  # Réduire le nombre pour éviter la confusion
        for _ in range(num_portals):
            if random.random() < 0.5:  # Augmenter la chance à 50%
                # Trouver une plateforme pour placer le premier portail
                suitable_platforms = [p for p in self.platforms if chunk_start <= p.x <= chunk_end - 500]
                if len(suitable_platforms) >= 2:  # S'assurer qu'on a au moins 2 plateformes
                    # Choisir deux plateformes différentes
                    platform1 = random.choice(suitable_platforms)
                    remaining_platforms = [p for p in suitable_platforms 
                                         if abs(p.x - platform1.x) > 400]  # Distance minimum
                    
                    if remaining_platforms:
                        platform2 = random.choice(remaining_platforms)
                        
                        # Créer les deux portails (bidirectionnels)
                        portal1_x = platform1.x + platform1.width // 2 - 30
                        portal1_y = platform1.y - 110  # Au-dessus de la plateforme
                        portal1 = MirrorPortal(portal1_x, portal1_y, 'bidirectional')
                        
                        portal2_x = platform2.x + platform2.width // 2 - 30
                        portal2_y = platform2.y - 110
                        portal2 = MirrorPortal(portal2_x, portal2_y, 'bidirectional')
                        
                        # Lier les portails (bidirectionnel)
                        portal1.linked_portal = portal2
                        portal2.linked_portal = portal1
                        
                        self.mirror_portals.extend([portal1, portal2])
    
    def generate_gravity_zones(self, chunk_start, chunk_end):
        """Génère des zones de gravité inversée"""
        num_zones = random.randint(1, 2)
        for _ in range(num_zones):
            if random.random() < 0.25:  # 25% de chance
                zone_x = random.randint(chunk_start, chunk_end - 300)
                zone_y = random.randint(100, SCREEN_HEIGHT - 200)
                zone_width = random.randint(200, 400)
                zone_height = random.randint(150, 250)
                
                zone = GravityZone(zone_x, zone_y, zone_width, zone_height)
                self.gravity_zones.append(zone)
    
    def generate_floating_crystals(self, chunk_start, chunk_end):
        """Génère des cristaux flottants décoratifs"""
        num_crystals = random.randint(5, 10)
        for _ in range(num_crystals):
            crystal_x = random.randint(chunk_start, chunk_end)
            crystal_y = random.randint(80, SCREEN_HEIGHT - 80)
            
            crystal = FloatingCrystal(crystal_x, crystal_y)
            self.floating_crystals.append(crystal)
    
    def generate_portal_particles(self, chunk_start, chunk_end):
        """Génère des particules de portail pour l'ambiance"""
        num_particles = random.randint(8, 15)
        for _ in range(num_particles):
            particle_x = random.randint(chunk_start, chunk_end)
            particle_y = random.randint(50, SCREEN_HEIGHT - 50)
            
            particle = PortalParticle(particle_x, particle_y)
            self.portal_particles.append(particle)
    
    def generate_star_fragments(self, chunk_start, chunk_end):
        """Génère des fragments avec style cristallin"""
        for platform in self.platforms:
            if chunk_start <= platform.x <= chunk_end:
                if random.random() < 0.35:  # Fragments plus rares mais plus précieux
                    star_x = platform.x + platform.width // 2 + random.randint(-20, 20)
                    star_y = platform.y - 50 - random.randint(0, 30)
                    
                    if self.is_star_reachable(star_x, star_y, platform):
                        star = StarFragment(star_x, star_y)
                        star.color = (180, 120, 255)  # Violet cristallin
                        star.value = 15  # Plus de valeur
                        self.star_fragments.append(star)
    
    def generate_crystalline_shadows(self, chunk_start, chunk_end):
        """Génère des ombres cristallines"""
        num_shadows = int(self.difficulty * 2)
        
        for _ in range(num_shadows):
            if random.random() < 0.2:
                attempts = 0
                while attempts < 10:
                    shadow_x = random.randint(chunk_start, chunk_end)
                    shadow_y = random.randint(150, SCREEN_HEIGHT - 150)
                    
                    if self.is_shadow_position_valid(shadow_x, shadow_y):
                        shadow = CrystallineShadow(shadow_x, shadow_y)
                        self.shadows.append(shadow)
                        break
                    attempts += 1
    
    def is_star_reachable(self, star_x, star_y, source_platform):
        """Vérifie l'accessibilité des fragments"""
        platform_center_x = source_platform.x + source_platform.width // 2
        horizontal_distance = abs(star_x - platform_center_x)
        vertical_distance = source_platform.y - star_y
        
        return (horizontal_distance <= source_platform.width // 2 + 50 and 
                0 <= vertical_distance <= 100)
    
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
        
        return (horizontal_distance <= 250 and vertical_distance <= 180)
    
    def cleanup_offscreen_elements(self, camera_x):
        """Nettoie les éléments hors écran"""
        cleanup_threshold = camera_x - SCREEN_WIDTH
        
        self.platforms = [p for p in self.platforms if p.x + p.width > cleanup_threshold]
        self.mirror_portals = [p for p in self.mirror_portals if p.x > cleanup_threshold]
        self.gravity_zones = [z for z in self.gravity_zones if z.x > cleanup_threshold]
        self.floating_crystals = [c for c in self.floating_crystals if c.x > cleanup_threshold]
        self.portal_particles = [p for p in self.portal_particles if p.x > cleanup_threshold]
        self.star_fragments = [s for s in self.star_fragments if s.x > cleanup_threshold and not s.collected]
        self.shadows = [s for s in self.shadows if s.x > cleanup_threshold and s.active]
    
    def check_portal_collisions(self, lyra):
        """Vérifie les collisions avec les portails miroirs"""
        for portal in self.mirror_portals:
            if portal.check_collision(lyra) and portal.linked_portal:
                # Vérifier qu'on ne téléporte pas en boucle
                if not hasattr(portal, 'cooldown_timer'):
                    portal.cooldown_timer = 0
                
                if portal.cooldown_timer <= 0:
                    # Téléporter Lyra vers le portail lié (bidirectionnel)
                    target_portal = portal.linked_portal
                    lyra.x = target_portal.x + target_portal.width // 2 - lyra.radius
                    lyra.y = target_portal.y - lyra.radius - 20  # Plus haut pour éviter de retomber dedans
                    lyra.vel_y = -5  # Petit saut vers le haut pour sortir du portail
                    
                    # Ajouter un cooldown plus long pour éviter la téléportation en boucle
                    portal.cooldown_timer = 90  # 1.5 secondes à 60 FPS
                    if portal.linked_portal:
                        portal.linked_portal.cooldown_timer = 90
                    
                    return True
        
        # Décrémenter les cooldowns
        for portal in self.mirror_portals:
            if hasattr(portal, 'cooldown_timer') and portal.cooldown_timer > 0:
                portal.cooldown_timer -= 1
        
        return False
    
    def check_gravity_zones(self, lyra):
        """Vérifie si Lyra est dans une zone de gravité inversée"""
        for zone in self.gravity_zones:
            if zone.contains_point(lyra.x + lyra.width // 2, lyra.y + lyra.height // 2):
                return True
        return False
    
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
        for portal in self.mirror_portals:
            portal.update()
        for zone in self.gravity_zones:
            zone.update()
        for crystal in self.floating_crystals:
            crystal.update()
        for particle in self.portal_particles:
            particle.update()
        for star in self.star_fragments:
            star.update()
        for shadow in self.shadows:
            shadow.update()
        if self.end_portal:
            self.end_portal.update()
    
    def create_end_platform(self):
        """Crée la fin de niveau avec style cristallin"""
        # Plateformes d'approche cristallines
        for i in range(4):
            approach_x = self.level_length - 500 + (i * 120)
            approach_y = SCREEN_HEIGHT // 2 + random.randint(-40, 40)
            approach_platform = FloatingCrystalPlatform(approach_x, approach_y, 130, 30)
            self.platforms.append(approach_platform)
        
        # Plateforme finale
        end_x = self.level_length - 50
        end_y = SCREEN_HEIGHT // 2
        end_platform = CrystalPlatform(end_x, end_y, 300, 60)
        end_platform.color = (200, 150, 255)  # Violet brillant
        end_platform.is_end_platform = True
        self.platforms.append(end_platform)
        
        self.end_portal = EndPortal(end_x + 150, end_y - 80)
        self.end_platform_created = True
    
    def check_level_completion(self, lyra):
        """Vérifie la fin de niveau"""
        if self.end_portal and self.end_portal.check_collision(lyra):
            return True
        return False
    
    def draw(self, screen, camera_x):
        """Dessine tous les éléments avec style miroirs célestes"""
        # Dessiner les zones de gravité en arrière-plan
        for zone in self.gravity_zones:
            zone.draw(screen, camera_x)
        
        # Dessiner les particules de portail en arrière-plan
        for particle in self.portal_particles:
            particle.draw(screen, camera_x)
        
        # Dessiner les cristaux flottants
        for crystal in self.floating_crystals:
            crystal.draw(screen, camera_x)
        
        # Dessiner les portails miroirs
        for portal in self.mirror_portals:
            portal.draw(screen, camera_x)
        
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


class CrystalPlatform(Platform):
    """Plateforme cristalline pour les miroirs célestes"""
    
    def __init__(self, x, y, width, height=20):
        super().__init__(x, y, width, height)
        self.color = (120, 80, 140)
        self.crystal_facets = []
        self.glow_offset = random.random() * 2 * math.pi
        
        # Générer des facettes cristallines
        for _ in range(random.randint(3, 6)):
            facet_x = random.randint(0, width)
            facet_size = random.randint(5, 12)
            self.crystal_facets.append((facet_x, facet_size))
    
    def update(self):
        """Met à jour les effets cristallins"""
        super().update()
        self.glow_offset += 0.03
    
    def draw(self, screen, camera_x):
        """Dessine la plateforme cristalline"""
        draw_x = self.x - camera_x
        
        if draw_x + self.width >= 0 and draw_x <= SCREEN_WIDTH:
            # Aura cristalline
            glow_intensity = 20 + int(math.sin(self.glow_offset) * 10)
            glow_surface = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
            glow_color = (180, 120, 255, glow_intensity)
            pygame.draw.rect(glow_surface, glow_color, (10, 10, self.width, self.height))
            screen.blit(glow_surface, (draw_x - 10, self.y - 10))
            
            # Plateforme de base
            pygame.draw.rect(screen, self.color, (draw_x, self.y, self.width, self.height))
            
            # Facettes cristallines
            for facet_x, facet_size in self.crystal_facets:
                facet_color = (200, 150, 255)
                facet_glow = int(math.sin(self.glow_offset + facet_x * 0.1) * 30 + 50)
                facet_final_color = (min(255, facet_color[0] + facet_glow), 
                                   min(255, facet_color[1] + facet_glow), 
                                   min(255, facet_color[2] + facet_glow))
                
                pygame.draw.circle(screen, facet_final_color, 
                                 (int(draw_x + facet_x), int(self.y + self.height // 2)), 
                                 facet_size)
            
            # Bordure brillante
            pygame.draw.rect(screen, (255, 255, 255), (draw_x, self.y, self.width, self.height), 2)


class FloatingCrystalPlatform(Platform):
    """Plateforme cristalline flottante"""
    
    def __init__(self, x, y, width=140, height=25):
        super().__init__(x, y, width, height)
        self.color = (180, 120, 255)
        
        # Mouvement de flottement
        self.start_y = y
        self.float_range = 40
        self.float_speed = 0.015
        self.float_offset = random.random() * 2 * math.pi
        
        # Effets visuels
        self.pulse_offset = 0
        self.crystal_shards = []
        
        # Générer des éclats cristallins
        for _ in range(random.randint(4, 8)):
            shard_x = random.randint(0, width)
            shard_y = random.randint(0, height)
            shard_size = random.randint(3, 7)
            self.crystal_shards.append((shard_x, shard_y, shard_size))
        
    def update(self):
        """Met à jour le mouvement de flottement"""
        super().update()
        self.float_offset += self.float_speed
        self.y = self.start_y + math.sin(self.float_offset) * self.float_range
        self.pulse_offset += 0.05
    
    def draw(self, screen, camera_x):
        """Dessine la plateforme flottante"""
        draw_x = self.x - camera_x
        
        if draw_x + self.width >= 0 and draw_x <= SCREEN_WIDTH:
            # Aura de flottement
            pulse_intensity = 30 + int(math.sin(self.pulse_offset) * 15)
            aura_surface = pygame.Surface((self.width + 40, self.height + 40), pygame.SRCALPHA)
            
            for i in range(4):
                aura_color = (*self.color, max(0, min(255, pulse_intensity - i * 6)))
                pygame.draw.rect(aura_surface, aura_color, 
                               (20 - i * 3, 20 - i * 3, self.width + i * 6, self.height + i * 6))
            
            screen.blit(aura_surface, (draw_x - 20, self.y - 20))
            
            # Plateforme principale
            pygame.draw.rect(screen, self.color, (draw_x, self.y, self.width, self.height))
            
            # Éclats cristallins
            for shard_x, shard_y, shard_size in self.crystal_shards:
                shard_glow = int(math.sin(self.pulse_offset + shard_x * 0.1) * 20 + 40)
                shard_color = (255, max(0, min(255, 200 + shard_glow)), 255)
                pygame.draw.circle(screen, shard_color, 
                                 (int(draw_x + shard_x), int(self.y + shard_y)), 
                                 shard_size)
            
            # Bordure énergétique
            border_color = (255, 255, 255, 150)
            border_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(border_surface, border_color, (0, 0, self.width, self.height), 3)
            screen.blit(border_surface, (draw_x, self.y))


class MirrorPortal:
    """Portail miroir pour la téléportation"""
    
    def __init__(self, x, y, portal_type='entry'):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 100
        self.portal_type = portal_type
        self.linked_portal = None
        self.cooldown_timer = 0
        
        # Animation
        self.rotation = 0
        self.pulse_offset = random.random() * 2 * math.pi
        self.energy_particles = []
        
        # Couleurs selon le type
        if portal_type == 'entry':
            self.color = (255, 120, 180)  # Rose
            self.glow_color = (255, 180, 220)
        else:
            self.color = (120, 180, 255)  # Bleu
            self.glow_color = (180, 220, 255)
        
        # Générer des particules d'énergie
        for _ in range(12):  # Plus de particules
            particle = {
                'angle': random.random() * 2 * math.pi,
                'distance': random.randint(40, 80),  # Plus loin
                'speed': random.uniform(0.02, 0.05),
                'size': random.randint(3, 7)  # Plus grosses
            }
            self.energy_particles.append(particle)
    
    def update(self):
        """Met à jour l'animation du portail"""
        self.rotation += 0.02
        self.pulse_offset += 0.04
        
        # Mettre à jour les particules
        for particle in self.energy_particles:
            particle['angle'] += particle['speed']
    
    def check_collision(self, lyra):
        """Vérifie la collision avec Lyra"""
        return (self.x <= lyra.x + lyra.width and 
                self.x + self.width >= lyra.x and
                self.y <= lyra.y + lyra.height and 
                self.y + self.height >= lyra.y)
    
    def draw(self, screen, camera_x):
        """Dessine le portail miroir"""
        draw_x = self.x - camera_x
        
        if draw_x + self.width >= 0 and draw_x <= SCREEN_WIDTH:
            # Aura de téléportation large
            aura_size = 150
            aura_surface = pygame.Surface((aura_size, aura_size), pygame.SRCALPHA)
            aura_intensity = max(0, min(255, 30 + int(math.sin(self.pulse_offset) * 20)))
            aura_color = (*self.glow_color, aura_intensity)
            pygame.draw.circle(aura_surface, aura_color, (aura_size // 2, aura_size // 2), aura_size // 2)
            screen.blit(aura_surface, (draw_x - aura_size // 2 + self.width // 2, 
                                     self.y - aura_size // 2 + self.height // 2))
            
            # Particules d'énergie
            for particle in self.energy_particles:
                particle_x = draw_x + self.width // 2 + math.cos(particle['angle']) * particle['distance']
                particle_y = self.y + self.height // 2 + math.sin(particle['angle']) * particle['distance']
                
                if 0 <= particle_x <= SCREEN_WIDTH:
                    particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                    particle_alpha = max(0, min(255, 150 + int(math.sin(self.pulse_offset + particle['angle']) * 50)))
                    particle_color = (*self.color, particle_alpha)
                    pygame.draw.circle(particle_surface, particle_color, 
                                     (particle['size'], particle['size']), particle['size'])
                    screen.blit(particle_surface, (particle_x - particle['size'], particle_y - particle['size']))
            
            # Portail principal avec effet de pulsation
            pulse = math.sin(self.pulse_offset) * 0.4 + 0.8
            portal_color = tuple(max(0, min(255, int(c * pulse))) for c in self.color)
            
            # Forme ovale du portail avec bordure brillante
            portal_surface = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
            
            # Bordure externe brillante
            border_color = (255, 255, 255, 200)
            pygame.draw.ellipse(portal_surface, border_color, (0, 0, self.width + 10, self.height + 10), 3)
            
            # Portail principal
            pygame.draw.ellipse(portal_surface, (*portal_color, 200), (5, 5, self.width, self.height))
            
            # Anneaux internes
            for i in range(4):
                ring_width = self.width - i * 12
                ring_height = self.height - i * 15
                if ring_width > 0 and ring_height > 0:
                    ring_alpha = max(0, min(255, 120 - i * 25))
                    ring_color = (*self.color, ring_alpha)
                    ring_x = 5 + i * 6
                    ring_y = 5 + i * 7.5
                    pygame.draw.ellipse(portal_surface, ring_color, 
                                      (ring_x, ring_y, ring_width, ring_height), 2)
            
            # Centre lumineux
            center_size = min(self.width, self.height) // 4
            center_color = (255, 255, 255, 180)
            pygame.draw.ellipse(portal_surface, center_color, 
                              (5 + self.width // 2 - center_size // 2, 
                               5 + self.height // 2 - center_size // 2, 
                               center_size, center_size))
            
            screen.blit(portal_surface, (draw_x - 5, self.y - 5))
            
            # Indicateur de type de portail
            font_size = 16
            if hasattr(pygame.font, 'Font'):
                font = pygame.font.Font(None, font_size)
                text = "ENTRÉE" if self.portal_type == 'entry' else "SORTIE"
                text_color = self.color
                text_surface = font.render(text, True, text_color)
                text_x = draw_x + self.width // 2 - text_surface.get_width() // 2
                text_y = self.y + self.height + 10
                screen.blit(text_surface, (text_x, text_y))


class GravityZone:
    """Zone de gravité inversée"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.wave_offset = random.random() * 2 * math.pi
        self.particles = []
        
        # Générer des particules flottantes
        for _ in range(15):
            particle = {
                'x': random.randint(0, width),
                'y': random.randint(0, height),
                'float_speed': random.uniform(0.01, 0.03),
                'float_range': random.randint(10, 25),
                'start_y': 0,
                'size': random.randint(2, 6)
            }
            particle['start_y'] = particle['y']
            self.particles.append(particle)
    
    def update(self):
        """Met à jour l'animation de la zone"""
        self.wave_offset += 0.02
        
        # Mettre à jour les particules
        for particle in self.particles:
            particle['float_speed'] += 0.001
            particle['y'] = particle['start_y'] + math.sin(self.wave_offset + particle['x'] * 0.01) * particle['float_range']
    
    def contains_point(self, x, y):
        """Vérifie si un point est dans la zone"""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def draw(self, screen, camera_x):
        """Dessine la zone de gravité"""
        draw_x = self.x - camera_x
        
        if draw_x + self.width >= 0 and draw_x <= SCREEN_WIDTH:
            # Zone de base
            zone_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            zone_color = (120, 180, 255, 40)
            zone_surface.fill(zone_color)
            
            # Ondes de gravité
            for i in range(5):
                wave_y = i * (self.height // 5) + int(math.sin(self.wave_offset + i) * 10)
                wave_alpha = 60 + int(math.sin(self.wave_offset + i) * 20)
                wave_color = (120, 180, 255, wave_alpha)
                pygame.draw.rect(zone_surface, wave_color, (0, wave_y, self.width, 3))
            
            screen.blit(zone_surface, (draw_x, self.y))
            
            # Particules flottantes
            for particle in self.particles:
                particle_x = draw_x + particle['x']
                particle_y = self.y + particle['y']
                
                if 0 <= particle_x <= SCREEN_WIDTH:
                    particle_color = (180, 220, 255, 120)
                    particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, particle_color, 
                                     (particle['size'], particle['size']), particle['size'])
                    screen.blit(particle_surface, (particle_x - particle['size'], particle_y - particle['size']))
            
            # Bordures de la zone
            border_color = (120, 180, 255, 100)
            border_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(border_surface, border_color, (0, 0, self.width, self.height), 4)
            screen.blit(border_surface, (draw_x, self.y))


class FloatingCrystal:
    """Cristal flottant décoratif"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_y = y
        self.size = random.randint(8, 20)
        self.rotation = random.random() * 2 * math.pi
        self.rotation_speed = random.uniform(0.01, 0.03)
        self.float_range = random.randint(20, 40)
        self.float_speed = random.uniform(0.008, 0.02)
        self.float_offset = random.random() * 2 * math.pi
        self.glow_offset = random.random() * 2 * math.pi
        self.facets = random.randint(5, 8)
        
    def update(self):
        """Met à jour l'animation du cristal"""
        self.rotation += self.rotation_speed
        self.float_offset += self.float_speed
        self.glow_offset += 0.04
        self.y = self.start_y + math.sin(self.float_offset) * self.float_range
    
    def draw(self, screen, camera_x):
        """Dessine le cristal flottant"""
        draw_x = self.x - camera_x
        
        if draw_x + self.size >= 0 and draw_x <= SCREEN_WIDTH:
            # Aura du cristal
            glow_intensity = 40 + int(math.sin(self.glow_offset) * 20)
            glow_surface = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
            glow_color = (180, 120, 255, glow_intensity)
            pygame.draw.circle(glow_surface, glow_color, 
                             (self.size * 1.5, self.size * 1.5), self.size * 1.5)
            screen.blit(glow_surface, (draw_x - self.size * 1.5, self.y - self.size * 1.5))
            
            # Forme cristalline
            crystal_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            
            # Points du cristal
            points = []
            for i in range(self.facets):
                angle = (i / self.facets) * 2 * math.pi + self.rotation
                x = self.size + math.cos(angle) * self.size * 0.8
                y = self.size + math.sin(angle) * self.size * 0.8
                points.append((x, y))
            
            # Couleur changeante
            color_shift = math.sin(self.glow_offset) * 50
            crystal_color = (150 + int(color_shift), 100, 200 + int(color_shift))
            
            pygame.draw.polygon(crystal_surface, crystal_color, points)
            
            # Reflets
            for i in range(3):
                highlight_color = (255, 255, 255, max(0, min(255, 80 - i * 20)))
                highlight_points = points[:len(points)//2]
                if len(highlight_points) >= 3:
                    pygame.draw.polygon(crystal_surface, highlight_color, highlight_points)
            
            screen.blit(crystal_surface, (draw_x - self.size, self.y - self.size))


class PortalParticle:
    """Particule de portail pour l'ambiance"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.size = random.randint(1, 4)
        self.orbit_radius = random.randint(20, 60)
        self.orbit_speed = random.uniform(0.01, 0.04)
        self.orbit_offset = random.random() * 2 * math.pi
        self.pulse_offset = random.random() * 2 * math.pi
        self.pulse_speed = random.uniform(0.05, 0.1)
        self.drift_speed = random.uniform(0.1, 0.3)
        
    def update(self):
        """Met à jour le mouvement de la particule"""
        self.orbit_offset += self.orbit_speed
        self.pulse_offset += self.pulse_speed
        self.start_x -= self.drift_speed
        
        # Mouvement orbital
        self.x = self.start_x + math.cos(self.orbit_offset) * self.orbit_radius
        self.y = self.start_y + math.sin(self.orbit_offset) * self.orbit_radius * 0.5
    
    def draw(self, screen, camera_x):
        """Dessine la particule de portail"""
        draw_x = self.x - camera_x
        
        if -10 <= draw_x <= SCREEN_WIDTH + 10:
            # Pulsation
            pulse = math.sin(self.pulse_offset) * 0.5 + 0.5
            alpha = int(100 + pulse * 100)
            
            # Couleur de portail
            particle_color = (200, 150, 255, alpha)
            particle_surface = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, particle_color, 
                             (self.size * 2, self.size * 2), self.size)
            screen.blit(particle_surface, (draw_x - self.size * 2, self.y - self.size * 2))


class CrystallineShadow(Shadow):
    """Ombre cristalline avec comportement spécial"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (60, 20, 80)  # Violet sombre
        self.crystal_shards = []
        self.shard_rotation = 0
        
        # Générer des éclats cristallins
        for _ in range(random.randint(4, 8)):
            shard = {
                'angle': random.random() * 2 * math.pi,
                'distance': random.randint(20, 40),
                'size': random.randint(3, 8),
                'rotation_speed': random.uniform(0.02, 0.05)
            }
            self.crystal_shards.append(shard)
        
    def update(self):
        """Met à jour l'ombre cristalline"""
        super().update()
        self.shard_rotation += 0.03
        
        # Mettre à jour les éclats
        for shard in self.crystal_shards:
            shard['angle'] += shard['rotation_speed']
    
    def draw(self, screen, camera_x):
        """Dessine l'ombre cristalline"""
        if not self.active:
            return
            
        draw_x = self.x - camera_x
        
        if draw_x + self.darkness_radius >= 0 and draw_x - self.darkness_radius <= SCREEN_WIDTH:
            # Aura cristalline
            for i in range(4):
                radius = self.darkness_radius + i * 8
                alpha = max(0, min(255, 80 - i * 15))
                if alpha > 0:
                    shadow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    shadow_color = (*self.color, alpha)
                    pygame.draw.circle(shadow_surface, shadow_color, (radius, radius), radius)
                    screen.blit(shadow_surface, (draw_x - radius, self.y - radius))
            
            # Éclats cristallins
            for shard in self.crystal_shards:
                shard_x = draw_x + math.cos(shard['angle']) * shard['distance']
                shard_y = self.y + math.sin(shard['angle']) * shard['distance']
                
                shard_color = (120, 80, 140, 150)
                shard_surface = pygame.Surface((shard['size'] * 2, shard['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(shard_surface, shard_color, 
                                 (shard['size'], shard['size']), shard['size'])
                screen.blit(shard_surface, (shard_x - shard['size'], shard_y - shard['size']))
            
            # Noyau central
            core_color = (100, 60, 120, 120)
            core_surface = pygame.Surface((self.darkness_radius, self.darkness_radius), pygame.SRCALPHA)
            pygame.draw.circle(core_surface, core_color, 
                             (self.darkness_radius // 2, self.darkness_radius // 2), 
                             self.darkness_radius // 2)
            screen.blit(core_surface, (draw_x - self.darkness_radius // 2, 
                                     self.y - self.darkness_radius // 2)) 