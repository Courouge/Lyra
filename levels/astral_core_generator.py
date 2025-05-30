import random
import math
import pygame
from settings import *
from entities.platform import Platform
from entities.star_fragment import StarFragment
from entities.shadow import Shadow
from entities.end_portal import EndPortal

class AstralCoreGenerator:
    """Générateur pour le Cœur d'Astralis - Niveau final ultime"""
    
    def __init__(self):
        self.platforms = []
        self.star_fragments = []
        self.shadows = []
        self.astral_nodes = []
        self.energy_streams = []
        self.cosmic_rifts = []
        self.stellar_platforms = []
        self.void_zones = []
        self.astral_guardians = []
        self.last_platform_x = 0
        self.last_platform_y = SCREEN_HEIGHT // 2
        self.difficulty = 2.5
        
        # Système de fin de niveau
        self.level_length = 8000
        self.end_platform_created = False
        self.end_portal = None
        
        # Couleurs spéciales pour le cœur d'Astralis
        self.colors = {
            'background': (5, 0, 20),
            'platform': (200, 150, 255),
            'stellar_platform': (255, 200, 100),
            'astral_node': (255, 255, 200),
            'energy_stream': (100, 255, 200),
            'void_zone': (50, 0, 100),
            'guardian': (255, 100, 150)
        }
        
        # Générer la plateforme de départ
        start_platform = StellarPlatform(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH // 2, 40)
        self.platforms.append(start_platform)
        self.last_platform_x = start_platform.x + start_platform.width
        self.last_platform_y = start_platform.y
        
        # Générer le premier chunk pour avoir des éléments dès le début
        self.generate_chunk(0)
        
    def generate_chunk(self, camera_x):
        """Génère un nouveau chunk avec toutes les mécaniques avancées"""
        chunk_start = int(camera_x + SCREEN_WIDTH)
        chunk_end = int(chunk_start + SCREEN_WIDTH)
        
        # Nettoyer les éléments hors de l'écran
        self.cleanup_offscreen_elements(camera_x)
        
        # Générer des plateformes (stellaires et normales)
        while self.last_platform_x < chunk_end:
            if random.random() < 0.6:  # 60% de chance de plateforme stellaire
                self.generate_stellar_platform()
            else:
                self.generate_next_platform()
                
        # Générer des nœuds astraux
        self.generate_astral_nodes(chunk_start, chunk_end)
        
        # Générer des flux d'énergie
        self.generate_energy_streams(chunk_start, chunk_end)
        
        # Générer des failles cosmiques
        self.generate_cosmic_rifts(chunk_start, chunk_end)
        
        # Générer des zones de vide
        self.generate_void_zones(chunk_start, chunk_end)
        
        # Générer des gardiens astraux
        self.generate_astral_guardians(chunk_start, chunk_end)
        
        # Générer des fragments d'étoiles
        self.generate_star_fragments(chunk_start, chunk_end)
        
        # Générer des ombres du vide
        self.generate_void_shadows(chunk_start, chunk_end)
    
    def generate_next_platform(self):
        """Génère une plateforme normale avec style astral"""
        base_spacing = PLATFORM_SPACING_X * 1.1  # Plus espacées
        
        spacing_x = int(base_spacing + random.randint(-40, 40))
        spacing_x = max(90, spacing_x)
        
        # Variation verticale extrême (gravité chaotique)
        max_jump_height = 130
        spacing_y = random.randint(-max_jump_height, max_jump_height)
        
        new_x = int(self.last_platform_x + spacing_x)
        new_y = int(self.last_platform_y + spacing_y)
        new_y = max(40, min(SCREEN_HEIGHT - 40, new_y))
        
        # Validation de saut avec gravité chaotique
        if spacing_x > 180 or abs(new_y - self.last_platform_y) > 160:
            spacing_x = min(spacing_x, 170)
            new_x = int(self.last_platform_x + spacing_x)
            if new_y > self.last_platform_y:
                new_y = min(new_y, self.last_platform_y + 140)
            else:
                new_y = max(new_y, self.last_platform_y - 140)
        
        # Plateformes astrales
        platform_width = PLATFORM_WIDTH + random.randint(0, 60)
        platform_width = max(110, platform_width)
        
        platform = AstralPlatform(new_x, new_y, platform_width)
        self.platforms.append(platform)
        
        self.last_platform_x = new_x + platform_width
        self.last_platform_y = new_y
    
    def generate_stellar_platform(self):
        """Génère une plateforme stellaire spéciale"""
        spacing_x = random.randint(120, 200)
        new_x = int(self.last_platform_x + spacing_x)
        new_y = int(self.last_platform_y + random.randint(-100, 100))
        new_y = max(100, min(SCREEN_HEIGHT - 100, new_y))
        
        platform = StellarPlatform(new_x, new_y, 160, 30)
        self.platforms.append(platform)
        
        self.last_platform_x = new_x + 160
        self.last_platform_y = new_y
    
    def generate_astral_nodes(self, chunk_start, chunk_end):
        """Génère des nœuds astraux énergétiques"""
        num_nodes = random.randint(2, 5)
        for _ in range(num_nodes):
            if random.random() < 0.4:
                node_x = random.randint(chunk_start, chunk_end)
                node_y = random.randint(100, SCREEN_HEIGHT - 100)
                
                node = AstralNode(node_x, node_y)
                self.astral_nodes.append(node)
    
    def generate_energy_streams(self, chunk_start, chunk_end):
        """Génère des flux d'énergie traversant l'espace"""
        num_streams = random.randint(1, 3)
        for _ in range(num_streams):
            if random.random() < 0.3:
                stream_x = random.randint(chunk_start, chunk_end - 400)
                stream_y = random.randint(50, SCREEN_HEIGHT - 50)
                stream_length = random.randint(300, 600)
                
                stream = EnergyStream(stream_x, stream_y, stream_length)
                self.energy_streams.append(stream)
    
    def generate_cosmic_rifts(self, chunk_start, chunk_end):
        """Génère des failles cosmiques dangereuses"""
        num_rifts = random.randint(1, 2)
        for _ in range(num_rifts):
            if random.random() < 0.2:
                rift_x = random.randint(chunk_start, chunk_end - 200)
                rift_y = random.randint(100, SCREEN_HEIGHT - 200)
                
                rift = CosmicRift(rift_x, rift_y)
                self.cosmic_rifts.append(rift)
    
    def generate_void_zones(self, chunk_start, chunk_end):
        """Génère des zones de vide spatial"""
        num_zones = random.randint(0, 2)
        for _ in range(num_zones):
            if random.random() < 0.15:
                zone_x = random.randint(chunk_start, chunk_end - 300)
                zone_y = random.randint(80, SCREEN_HEIGHT - 150)
                zone_width = random.randint(200, 350)
                zone_height = random.randint(120, 200)
                
                zone = VoidZone(zone_x, zone_y, zone_width, zone_height)
                self.void_zones.append(zone)
    
    def generate_astral_guardians(self, chunk_start, chunk_end):
        """Génère des gardiens astraux"""
        num_guardians = random.randint(0, 1)
        for _ in range(num_guardians):
            if random.random() < 0.1:
                guardian_x = random.randint(chunk_start, chunk_end)
                guardian_y = random.randint(150, SCREEN_HEIGHT - 150)
                
                guardian = AstralGuardian(guardian_x, guardian_y)
                self.astral_guardians.append(guardian)
    
    def generate_star_fragments(self, chunk_start, chunk_end):
        """Génère des fragments avec style cœur d'Astralis"""
        for platform in self.platforms:
            if chunk_start <= platform.x <= chunk_end:
                if random.random() < 0.3:  # Fragments rares mais très précieux
                    star_x = platform.x + platform.width // 2 + random.randint(-25, 25)
                    star_y = platform.y - 60 - random.randint(0, 40)
                    
                    if self.is_star_reachable(star_x, star_y, platform):
                        star = StarFragment(star_x, star_y)
                        star.color = (255, 255, 200)  # Or astral
                        star.value = 25  # Très précieux
                        self.star_fragments.append(star)
    
    def generate_void_shadows(self, chunk_start, chunk_end):
        """Génère des ombres du vide"""
        num_shadows = int(self.difficulty * 3)
        
        for _ in range(num_shadows):
            if random.random() < 0.3:
                attempts = 0
                while attempts < 10:
                    shadow_x = random.randint(chunk_start, chunk_end)
                    shadow_y = random.randint(150, SCREEN_HEIGHT - 150)
                    
                    if self.is_shadow_position_valid(shadow_x, shadow_y):
                        shadow = VoidShadow(shadow_x, shadow_y)
                        self.shadows.append(shadow)
                        break
                    attempts += 1
    
    def is_star_reachable(self, star_x, star_y, source_platform):
        """Vérifie l'accessibilité des fragments"""
        platform_center_x = source_platform.x + source_platform.width // 2
        horizontal_distance = abs(star_x - platform_center_x)
        vertical_distance = source_platform.y - star_y
        
        return (horizontal_distance <= source_platform.width // 2 + 60 and 
                0 <= vertical_distance <= 120)
    
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
        
        return (horizontal_distance <= 300 and vertical_distance <= 200)
    
    def cleanup_offscreen_elements(self, camera_x):
        """Nettoie les éléments hors écran"""
        cleanup_threshold = camera_x - SCREEN_WIDTH
        
        self.platforms = [p for p in self.platforms if p.x + p.width > cleanup_threshold]
        self.astral_nodes = [n for n in self.astral_nodes if n.x > cleanup_threshold]
        self.energy_streams = [s for s in self.energy_streams if s.x > cleanup_threshold]
        self.cosmic_rifts = [r for r in self.cosmic_rifts if r.x > cleanup_threshold]
        self.void_zones = [z for z in self.void_zones if z.x > cleanup_threshold]
        self.astral_guardians = [g for g in self.astral_guardians if g.x > cleanup_threshold]
        self.star_fragments = [s for s in self.star_fragments if s.x > cleanup_threshold and not s.collected]
        self.shadows = [s for s in self.shadows if s.x > cleanup_threshold and s.active]
    
    def check_void_zones(self, lyra):
        """Vérifie si Lyra est dans une zone de vide (danger)"""
        for zone in self.void_zones:
            if zone.contains_point(lyra.x + lyra.width // 2, lyra.y + lyra.height // 2):
                return True
        return False
    
    def check_energy_streams(self, lyra):
        """Vérifie les collisions avec les flux d'énergie (boost)"""
        for stream in self.energy_streams:
            if stream.check_collision(lyra):
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
        for node in self.astral_nodes:
            node.update()
        for stream in self.energy_streams:
            stream.update()
        for rift in self.cosmic_rifts:
            rift.update()
        for zone in self.void_zones:
            zone.update()
        for guardian in self.astral_guardians:
            guardian.update()
        for star in self.star_fragments:
            star.update()
        for shadow in self.shadows:
            shadow.update()
        if self.end_portal:
            self.end_portal.update()
    
    def create_end_platform(self):
        """Crée la fin de niveau avec style cœur d'Astralis"""
        # Plateformes d'approche stellaires
        for i in range(5):
            approach_x = self.level_length - 600 + (i * 120)
            approach_y = SCREEN_HEIGHT // 2 + random.randint(-50, 50)
            approach_platform = StellarPlatform(approach_x, approach_y, 140, 35)
            self.platforms.append(approach_platform)
        
        # Plateforme finale - Le Cœur d'Astralis
        end_x = self.level_length - 50
        end_y = SCREEN_HEIGHT // 2
        end_platform = AstralPlatform(end_x, end_y, 400, 80)
        end_platform.color = (255, 255, 200)  # Or astral brillant
        end_platform.is_end_platform = True
        self.platforms.append(end_platform)
        
        self.end_portal = EndPortal(end_x + 200, end_y - 100)
        self.end_platform_created = True
    
    def check_level_completion(self, lyra):
        """Vérifie la fin de niveau"""
        if self.end_portal and self.end_portal.check_collision(lyra):
            return True
        return False
    
    def draw(self, screen, camera_x):
        """Dessine tous les éléments avec style cœur d'Astralis"""
        # Dessiner les zones de vide en arrière-plan
        for zone in self.void_zones:
            zone.draw(screen, camera_x)
        
        # Dessiner les flux d'énergie
        for stream in self.energy_streams:
            stream.draw(screen, camera_x)
        
        # Dessiner les nœuds astraux
        for node in self.astral_nodes:
            node.draw(screen, camera_x)
        
        # Dessiner les failles cosmiques
        for rift in self.cosmic_rifts:
            rift.draw(screen, camera_x)
        
        # Dessiner les gardiens astraux
        for guardian in self.astral_guardians:
            guardian.draw(screen, camera_x)
        
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


# Classes spécialisées pour le Cœur d'Astralis

class AstralPlatform(Platform):
    """Plateforme astrale pour le cœur d'Astralis"""
    
    def __init__(self, x, y, width, height=25):
        super().__init__(x, y, width, height)
        self.color = (200, 150, 255)
        self.astral_energy = []
        self.pulse_offset = random.random() * 2 * math.pi
        
        # Générer des points d'énergie astrale
        for _ in range(random.randint(5, 10)):
            energy_x = random.randint(0, width)
            energy_y = random.randint(0, height)
            energy_intensity = random.uniform(0.5, 1.0)
            self.astral_energy.append((energy_x, energy_y, energy_intensity))
    
    def update(self):
        """Met à jour les effets astraux"""
        super().update()
        self.pulse_offset += 0.04
    
    def draw(self, screen, camera_x):
        """Dessine la plateforme astrale"""
        draw_x = self.x - camera_x
        
        if draw_x + self.width >= 0 and draw_x <= SCREEN_WIDTH:
            # Aura astrale
            pulse_intensity = max(0, min(255, 30 + int(math.sin(self.pulse_offset) * 15)))
            aura_surface = pygame.Surface((self.width + 30, self.height + 30), pygame.SRCALPHA)
            aura_color = (255, 200, 255, pulse_intensity)
            pygame.draw.rect(aura_surface, aura_color, (15, 15, self.width, self.height))
            screen.blit(aura_surface, (draw_x - 15, self.y - 15))
            
            # Plateforme de base
            pygame.draw.rect(screen, self.color, (draw_x, self.y, self.width, self.height))
            
            # Points d'énergie astrale
            for energy_x, energy_y, intensity in self.astral_energy:
                energy_glow = max(0, min(255, int(math.sin(self.pulse_offset + energy_x * 0.1) * 40 * intensity + 60)))
                energy_color = (255, 255, max(0, min(255, 200 + energy_glow)))
                energy_size = max(1, int(3 + intensity * 4))
                pygame.draw.circle(screen, energy_color, 
                                 (int(draw_x + energy_x), int(self.y + energy_y)), 
                                 energy_size)
            
            # Bordure énergétique
            border_intensity = max(0, min(255, int(math.sin(self.pulse_offset) * 50 + 100)))
            border_color = (255, 255, border_intensity)
            pygame.draw.rect(screen, border_color, (draw_x, self.y, self.width, self.height), 3)


class StellarPlatform(Platform):
    """Plateforme stellaire ultra-avancée"""
    
    def __init__(self, x, y, width=160, height=30):
        super().__init__(x, y, width, height)
        self.color = (255, 200, 100)
        
        # Mouvement stellaire
        self.start_y = y
        self.orbit_range = 50
        self.orbit_speed = 0.01
        self.orbit_offset = random.random() * 2 * math.pi
        
        # Effets stellaires
        self.stellar_flares = []
        self.corona_offset = 0
        
        # Générer des éruptions stellaires
        for _ in range(random.randint(6, 12)):
            flare_angle = random.random() * 2 * math.pi
            flare_distance = random.randint(20, 40)
            flare_intensity = random.uniform(0.7, 1.0)
            self.stellar_flares.append((flare_angle, flare_distance, flare_intensity))
        
    def update(self):
        """Met à jour le mouvement stellaire"""
        super().update()
        self.orbit_offset += self.orbit_speed
        self.y = self.start_y + math.sin(self.orbit_offset) * self.orbit_range
        self.corona_offset += 0.06
    
    def draw(self, screen, camera_x):
        """Dessine la plateforme stellaire"""
        draw_x = self.x - camera_x
        
        if draw_x + self.width >= 0 and draw_x <= SCREEN_WIDTH:
            # Couronne stellaire
            corona_intensity = max(0, min(255, 40 + int(math.sin(self.corona_offset) * 20)))
            corona_surface = pygame.Surface((self.width + 60, self.height + 60), pygame.SRCALPHA)
            
            for i in range(6):
                corona_alpha = max(0, min(255, corona_intensity - i * 6))
                corona_color = (self.color[0], self.color[1], self.color[2], corona_alpha)
                pygame.draw.rect(corona_surface, corona_color, 
                               (30 - i * 5, 30 - i * 5, self.width + i * 10, self.height + i * 10))
            
            screen.blit(corona_surface, (draw_x - 30, self.y - 30))
            
            # Plateforme principale
            pygame.draw.rect(screen, self.color, (draw_x, self.y, self.width, self.height))
            
            # Éruptions stellaires
            center_x = draw_x + self.width // 2
            center_y = self.y + self.height // 2
            
            for flare_angle, flare_distance, intensity in self.stellar_flares:
                flare_x = center_x + math.cos(flare_angle + self.corona_offset) * flare_distance
                flare_y = center_y + math.sin(flare_angle + self.corona_offset) * flare_distance
                
                flare_size = max(1, int(4 + intensity * 6))
                flare_color = (255, max(0, min(255, 150 + int(intensity * 100))), 50)
                pygame.draw.circle(screen, flare_color, (int(flare_x), int(flare_y)), flare_size)
            
            # Noyau stellaire
            core_color = (255, 255, 255)
            pygame.draw.rect(screen, core_color, 
                           (draw_x + 10, self.y + 5, self.width - 20, self.height - 10))


class AstralNode:
    """Nœud astral énergétique"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(15, 25)
        self.energy_level = 1.0
        self.pulse_offset = random.random() * 2 * math.pi
        self.connections = []
        
        # Générer des connexions énergétiques
        for _ in range(random.randint(3, 6)):
            connection_angle = random.random() * 2 * math.pi
            connection_length = random.randint(40, 80)
            self.connections.append((connection_angle, connection_length))
    
    def update(self):
        """Met à jour le nœud astral"""
        self.pulse_offset += 0.05
        self.energy_level = 0.7 + 0.3 * math.sin(self.pulse_offset)
    
    def draw(self, screen, camera_x):
        """Dessine le nœud astral"""
        draw_x = self.x - camera_x
        
        if draw_x + self.size >= 0 and draw_x <= SCREEN_WIDTH:
            # Connexions énergétiques
            for angle, length in self.connections:
                end_x = draw_x + math.cos(angle + self.pulse_offset * 0.5) * length
                end_y = self.y + math.sin(angle + self.pulse_offset * 0.5) * length
                
                connection_alpha = max(0, min(255, int(100 * self.energy_level)))
                connection_color = (100, 255, 200, connection_alpha)
                connection_surface = pygame.Surface((int(abs(end_x - draw_x)) + 10, int(abs(end_y - self.y)) + 10), pygame.SRCALPHA)
                pygame.draw.line(connection_surface, connection_color, 
                               (5, 5), (int(end_x - draw_x + 5), int(end_y - self.y + 5)), 3)
                screen.blit(connection_surface, (int(min(draw_x, end_x)) - 5, int(min(self.y, end_y)) - 5))
            
            # Nœud principal
            node_size = max(1, int(self.size * self.energy_level))
            node_color = (255, 255, max(0, min(255, int(200 * self.energy_level))))
            
            # Aura du nœud
            aura_surface = pygame.Surface((node_size * 3, node_size * 3), pygame.SRCALPHA)
            aura_alpha = max(0, min(255, int(60 * self.energy_level)))
            aura_color = (255, 255, 200, aura_alpha)
            pygame.draw.circle(aura_surface, aura_color, 
                             (int(node_size * 1.5), int(node_size * 1.5)), int(node_size * 1.5))
            screen.blit(aura_surface, (int(draw_x - node_size * 1.5), int(self.y - node_size * 1.5)))
            
            # Nœud central
            pygame.draw.circle(screen, node_color, (int(draw_x), int(self.y)), node_size)
            pygame.draw.circle(screen, (255, 255, 255), (int(draw_x), int(self.y)), node_size // 2)


class EnergyStream:
    """Flux d'énergie traversant l'espace"""
    
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length
        self.width = 20
        self.flow_offset = 0
        self.particles = []
        
        # Générer des particules de flux
        for i in range(length // 20):
            particle_x = i * 20
            particle_speed = random.uniform(2, 5)
            particle_size = random.randint(2, 6)
            self.particles.append({'x': particle_x, 'speed': particle_speed, 'size': particle_size})
    
    def update(self):
        """Met à jour le flux d'énergie"""
        self.flow_offset += 3
        
        # Mettre à jour les particules
        for particle in self.particles:
            particle['x'] += particle['speed']
            if particle['x'] > self.length:
                particle['x'] = 0
    
    def check_collision(self, lyra):
        """Vérifie la collision avec Lyra"""
        return (self.x <= lyra.x + lyra.width and 
                self.x + self.length >= lyra.x and
                self.y - self.width // 2 <= lyra.y + lyra.height and 
                self.y + self.width // 2 >= lyra.y)
    
    def draw(self, screen, camera_x):
        """Dessine le flux d'énergie"""
        draw_x = self.x - camera_x
        
        if draw_x + self.length >= 0 and draw_x <= SCREEN_WIDTH:
            # Flux principal
            stream_surface = pygame.Surface((self.length, self.width), pygame.SRCALPHA)
            stream_color = (100, 255, 200, 120)
            pygame.draw.rect(stream_surface, stream_color, (0, 0, self.length, self.width))
            screen.blit(stream_surface, (draw_x, self.y - self.width // 2))
            
            # Particules de flux
            for particle in self.particles:
                particle_x = draw_x + particle['x']
                if 0 <= particle_x <= SCREEN_WIDTH:
                    particle_color = (150, 255, 250)
                    pygame.draw.circle(screen, particle_color, 
                                     (int(particle_x), int(self.y)), particle['size'])
            
            # Bordures énergétiques
            border_color = (200, 255, 255)
            pygame.draw.rect(screen, border_color, 
                           (draw_x, self.y - self.width // 2, self.length, self.width), 2)


class CosmicRift:
    """Faille cosmique dangereuse"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = random.randint(60, 100)
        self.height = random.randint(150, 250)
        self.distortion_offset = random.random() * 2 * math.pi
        self.void_particles = []
        
        # Générer des particules de vide
        for _ in range(20):
            particle_x = random.randint(0, self.width)
            particle_y = random.randint(0, self.height)
            particle_speed = random.uniform(0.5, 2.0)
            self.void_particles.append({'x': particle_x, 'y': particle_y, 'speed': particle_speed})
    
    def update(self):
        """Met à jour la faille cosmique"""
        self.distortion_offset += 0.03
        
        # Mettre à jour les particules de vide
        for particle in self.void_particles:
            particle['y'] += particle['speed']
            if particle['y'] > self.height:
                particle['y'] = 0
                particle['x'] = random.randint(0, self.width)
    
    def draw(self, screen, camera_x):
        """Dessine la faille cosmique"""
        draw_x = self.x - camera_x
        
        if draw_x + self.width >= 0 and draw_x <= SCREEN_WIDTH:
            # Distorsion de l'espace
            distortion = math.sin(self.distortion_offset) * 8
            
            # Faille principale
            rift_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            for i in range(self.height // 5):
                rift_y = i * 5
                rift_alpha = 80 + int(math.sin(self.distortion_offset + i * 0.2) * 40)
                rift_color = (50, 0, 100, rift_alpha)
                pygame.draw.rect(rift_surface, rift_color, (0, rift_y, self.width, 5))
            
            screen.blit(rift_surface, (draw_x + distortion, self.y))
            
            # Particules de vide
            for particle in self.void_particles:
                particle_x = draw_x + particle['x'] + distortion
                particle_y = self.y + particle['y']
                
                if 0 <= particle_x <= SCREEN_WIDTH:
                    particle_color = (100, 50, 150, 180)
                    particle_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, particle_color, (3, 3), 3)
                    screen.blit(particle_surface, (particle_x - 3, particle_y - 3))


class VoidZone:
    """Zone de vide spatial dangereuse"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.void_intensity = 0
        self.void_particles = []
        
        # Générer des particules de vide
        for _ in range(30):
            particle = {
                'x': random.randint(0, width),
                'y': random.randint(0, height),
                'drift_x': random.uniform(-0.5, 0.5),
                'drift_y': random.uniform(-0.5, 0.5),
                'size': random.randint(1, 4)
            }
            self.void_particles.append(particle)
    
    def update(self):
        """Met à jour la zone de vide"""
        self.void_intensity += 0.02
        
        # Mettre à jour les particules
        for particle in self.void_particles:
            particle['x'] += particle['drift_x']
            particle['y'] += particle['drift_y']
            
            # Rebond aux limites
            if particle['x'] <= 0 or particle['x'] >= self.width:
                particle['drift_x'] *= -1
            if particle['y'] <= 0 or particle['y'] >= self.height:
                particle['drift_y'] *= -1
    
    def contains_point(self, x, y):
        """Vérifie si un point est dans la zone"""
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def draw(self, screen, camera_x):
        """Dessine la zone de vide"""
        draw_x = self.x - camera_x
        
        if draw_x + self.width >= 0 and draw_x <= SCREEN_WIDTH:
            # Zone de vide
            void_alpha = int(60 + 30 * math.sin(self.void_intensity))
            void_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            void_color = (20, 0, 40, void_alpha)
            void_surface.fill(void_color)
            screen.blit(void_surface, (draw_x, self.y))
            
            # Particules de vide
            for particle in self.void_particles:
                particle_x = draw_x + particle['x']
                particle_y = self.y + particle['y']
                
                if 0 <= particle_x <= SCREEN_WIDTH:
                    particle_alpha = int(120 + 60 * math.sin(self.void_intensity + particle['x'] * 0.1))
                    particle_color = (80, 40, 120, particle_alpha)
                    particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                    pygame.draw.circle(particle_surface, particle_color, 
                                     (particle['size'], particle['size']), particle['size'])
                    screen.blit(particle_surface, (particle_x - particle['size'], particle_y - particle['size']))
            
            # Bordure de danger
            border_color = (150, 50, 200, 150)
            border_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(border_surface, border_color, (0, 0, self.width, self.height), 5)
            screen.blit(border_surface, (draw_x, self.y))


class AstralGuardian:
    """Gardien astral mobile"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.size = 30
        self.patrol_range = 200
        self.patrol_speed = 0.8
        self.patrol_direction = 1
        self.energy_aura = 0
        self.guardian_type = random.choice(['protector', 'sentinel'])
        
        if self.guardian_type == 'protector':
            self.color = (100, 255, 150)
        else:
            self.color = (255, 100, 150)
    
    def update(self):
        """Met à jour le gardien astral"""
        # Patrouille
        self.x += self.patrol_speed * self.patrol_direction
        
        if self.x > self.start_x + self.patrol_range or self.x < self.start_x - self.patrol_range:
            self.patrol_direction *= -1
        
        self.energy_aura += 0.08
    
    def draw(self, screen, camera_x):
        """Dessine le gardien astral"""
        draw_x = self.x - camera_x
        
        if draw_x + self.size >= 0 and draw_x <= SCREEN_WIDTH:
            # Aura énergétique
            aura_intensity = max(0, min(255, 40 + int(math.sin(self.energy_aura) * 20)))
            aura_surface = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
            aura_color = (self.color[0], self.color[1], self.color[2], aura_intensity)
            pygame.draw.circle(aura_surface, aura_color, 
                             (int(self.size * 1.5), int(self.size * 1.5)), int(self.size * 1.5))
            screen.blit(aura_surface, (int(draw_x - self.size * 1.5), int(self.y - self.size * 1.5)))
            
            # Corps du gardien
            pygame.draw.circle(screen, self.color, (int(draw_x), int(self.y)), self.size)
            
            # Noyau énergétique
            core_size = int(self.size * 0.6)
            core_color = (255, 255, 255)
            pygame.draw.circle(screen, core_color, (int(draw_x), int(self.y)), core_size)
            
            # Rayons d'énergie
            for i in range(8):
                ray_angle = (i / 8) * 2 * math.pi + self.energy_aura
                ray_x = draw_x + math.cos(ray_angle) * self.size * 1.5
                ray_y = self.y + math.sin(ray_angle) * self.size * 1.5
                pygame.draw.line(screen, self.color, (int(draw_x), int(self.y)), (int(ray_x), int(ray_y)), 2)


class VoidShadow(Shadow):
    """Ombre du vide - la plus dangereuse"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (20, 0, 40)  # Violet très sombre
        self.void_tendrils = []
        self.void_pulse = 0
        
        # Générer des tentacules de vide
        for _ in range(random.randint(6, 10)):
            tendril = {
                'angle': random.random() * 2 * math.pi,
                'length': random.randint(30, 60),
                'thickness': random.randint(3, 8),
                'wave_speed': random.uniform(0.03, 0.08)
            }
            self.void_tendrils.append(tendril)
        
    def update(self):
        """Met à jour l'ombre du vide"""
        super().update()
        self.void_pulse += 0.04
        
        # Mettre à jour les tentacules
        for tendril in self.void_tendrils:
            tendril['angle'] += tendril['wave_speed']
    
    def draw(self, screen, camera_x):
        """Dessine l'ombre du vide"""
        if not self.active:
            return
            
        draw_x = self.x - camera_x
        
        if draw_x + self.darkness_radius >= 0 and draw_x - self.darkness_radius <= SCREEN_WIDTH:
            # Tentacules de vide
            for tendril in self.void_tendrils:
                tendril_end_x = draw_x + math.cos(tendril['angle']) * tendril['length']
                tendril_end_y = self.y + math.sin(tendril['angle']) * tendril['length']
                
                tendril_color = (60, 20, 80, 150)
                tendril_surface = pygame.Surface((int(abs(tendril_end_x - draw_x)) + 20, int(abs(tendril_end_y - self.y)) + 20), pygame.SRCALPHA)
                pygame.draw.line(tendril_surface, tendril_color, 
                               (10, 10), (int(tendril_end_x - draw_x + 10), int(tendril_end_y - self.y + 10)), 
                               tendril['thickness'])
                screen.blit(tendril_surface, (int(min(draw_x, tendril_end_x)) - 10, int(min(self.y, tendril_end_y)) - 10))
            
            # Aura de vide
            for i in range(5):
                radius = self.darkness_radius + i * 12
                alpha = max(0, min(255, 100 - i * 18))
                if alpha > 0:
                    void_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    void_color = (self.color[0], self.color[1], self.color[2], alpha)
                    pygame.draw.circle(void_surface, void_color, (radius, radius), radius)
                    screen.blit(void_surface, (int(draw_x - radius), int(self.y - radius)))
            
            # Noyau du vide
            core_intensity = max(0, min(255, int(150 + 50 * math.sin(self.void_pulse))))
            core_color = (core_intensity, 0, core_intensity // 2, 200)
            core_surface = pygame.Surface((self.darkness_radius, self.darkness_radius), pygame.SRCALPHA)
            pygame.draw.circle(core_surface, core_color, 
                             (self.darkness_radius // 2, self.darkness_radius // 2), 
                             self.darkness_radius // 2)
            screen.blit(core_surface, (int(draw_x - self.darkness_radius // 2), 
                                     int(self.y - self.darkness_radius // 2))) 