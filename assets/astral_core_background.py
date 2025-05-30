import pygame
import math
import random
from settings import *

class AstralCoreBackground:
    """Fond spécialisé pour le Cœur d'Astralis - Niveau final ultime"""
    
    def __init__(self):
        # Couches de parallaxe
        self.cosmic_vortex = []
        self.stellar_nurseries = []
        self.quantum_fields = []
        self.astral_streams = []
        self.void_rifts = []
        self.energy_cascades = []
        self.dimensional_tears = []
        
        # Générer les éléments de fond
        self.generate_cosmic_vortex()
        self.generate_stellar_nurseries()
        self.generate_quantum_fields()
        self.generate_astral_streams()
        self.generate_void_rifts()
        self.generate_energy_cascades()
        self.generate_dimensional_tears()
        
        # Animation
        self.time_offset = 0
        self.cosmic_pulse = 0
        self.dimensional_shift = 0
        
    def generate_cosmic_vortex(self):
        """Génère des vortex cosmiques en arrière-plan"""
        for _ in range(3):
            vortex = {
                'x': random.randint(-200, SCREEN_WIDTH + 200),
                'y': random.randint(-100, SCREEN_HEIGHT + 100),
                'size': random.randint(300, 600),
                'rotation_speed': random.uniform(0.005, 0.02),
                'rotation': random.random() * 2 * math.pi,
                'intensity': random.uniform(0.3, 0.8),
                'color_shift': random.uniform(0, 2 * math.pi)
            }
            self.cosmic_vortex.append(vortex)
    
    def generate_stellar_nurseries(self):
        """Génère des pépinières stellaires"""
        for _ in range(5):
            nursery = {
                'x': random.randint(-300, SCREEN_WIDTH + 300),
                'y': random.randint(-150, SCREEN_HEIGHT + 150),
                'width': random.randint(200, 400),
                'height': random.randint(100, 200),
                'star_count': random.randint(15, 30),
                'nebula_color': (
                    random.randint(100, 255),
                    random.randint(50, 200),
                    random.randint(150, 255)
                ),
                'drift_x': random.uniform(-0.2, 0.2),
                'drift_y': random.uniform(-0.1, 0.1),
                'pulse_offset': random.random() * 2 * math.pi
            }
            self.stellar_nurseries.append(nursery)
    
    def generate_quantum_fields(self):
        """Génère des champs quantiques"""
        for _ in range(8):
            field = {
                'x': random.randint(-100, SCREEN_WIDTH + 100),
                'y': random.randint(-50, SCREEN_HEIGHT + 50),
                'particles': [],
                'field_strength': random.uniform(0.5, 1.5),
                'oscillation_speed': random.uniform(0.02, 0.08),
                'phase_offset': random.random() * 2 * math.pi
            }
            
            # Générer des particules quantiques
            for _ in range(random.randint(20, 40)):
                particle = {
                    'local_x': random.randint(-50, 50),
                    'local_y': random.randint(-50, 50),
                    'quantum_state': random.random(),
                    'entanglement': random.random() * 2 * math.pi,
                    'size': random.randint(1, 3)
                }
                field['particles'].append(particle)
            
            self.quantum_fields.append(field)
    
    def generate_astral_streams(self):
        """Génère des flux astraux traversant l'espace"""
        for _ in range(6):
            stream = {
                'start_x': random.randint(-200, SCREEN_WIDTH + 200),
                'start_y': random.randint(0, SCREEN_HEIGHT),
                'end_x': random.randint(-200, SCREEN_WIDTH + 200),
                'end_y': random.randint(0, SCREEN_HEIGHT),
                'width': random.randint(8, 20),
                'flow_speed': random.uniform(1, 4),
                'flow_offset': random.random() * 100,
                'energy_color': (
                    random.randint(150, 255),
                    random.randint(200, 255),
                    random.randint(100, 255)
                ),
                'segments': random.randint(10, 20)
            }
            self.astral_streams.append(stream)
    
    def generate_void_rifts(self):
        """Génère des failles dans le vide spatial"""
        for _ in range(4):
            rift = {
                'x': random.randint(-100, SCREEN_WIDTH + 100),
                'y': random.randint(-50, SCREEN_HEIGHT + 50),
                'length': random.randint(150, 300),
                'angle': random.random() * 2 * math.pi,
                'distortion_strength': random.uniform(0.5, 2.0),
                'void_intensity': random.uniform(0.3, 0.8),
                'tear_width': random.randint(5, 15),
                'void_particles': []
            }
            
            # Générer des particules de vide
            for _ in range(random.randint(10, 20)):
                particle = {
                    'offset': random.random(),
                    'drift': random.uniform(-1, 1),
                    'size': random.randint(1, 4),
                    'intensity': random.uniform(0.3, 1.0)
                }
                rift['void_particles'].append(particle)
            
            self.void_rifts.append(rift)
    
    def generate_energy_cascades(self):
        """Génère des cascades d'énergie"""
        for _ in range(10):
            cascade = {
                'x': random.randint(-50, SCREEN_WIDTH + 50),
                'y': random.randint(-100, SCREEN_HEIGHT + 100),
                'energy_nodes': [],
                'connection_strength': random.uniform(0.5, 1.5),
                'pulse_frequency': random.uniform(0.03, 0.1),
                'cascade_color': (
                    random.randint(200, 255),
                    random.randint(150, 255),
                    random.randint(100, 255)
                )
            }
            
            # Générer des nœuds d'énergie
            for _ in range(random.randint(3, 8)):
                node = {
                    'local_x': random.randint(-80, 80),
                    'local_y': random.randint(-80, 80),
                    'energy_level': random.uniform(0.3, 1.0),
                    'pulse_offset': random.random() * 2 * math.pi,
                    'size': random.randint(3, 8)
                }
                cascade['energy_nodes'].append(node)
            
            self.energy_cascades.append(cascade)
    
    def generate_dimensional_tears(self):
        """Génère des déchirures dimensionnelles"""
        for _ in range(3):
            tear = {
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': random.randint(100, SCREEN_HEIGHT - 100),
                'width': random.randint(80, 150),
                'height': random.randint(120, 200),
                'reality_distortion': random.uniform(0.5, 1.5),
                'dimensional_phase': random.random() * 2 * math.pi,
                'tear_intensity': random.uniform(0.4, 0.9),
                'otherworld_color': (
                    random.randint(50, 150),
                    random.randint(100, 200),
                    random.randint(150, 255)
                )
            }
            self.dimensional_tears.append(tear)
    
    def update(self, camera_x):
        """Met à jour tous les effets de fond"""
        self.time_offset += 0.016
        self.cosmic_pulse += 0.02
        self.dimensional_shift += 0.01
        
        # Mettre à jour les vortex cosmiques
        for vortex in self.cosmic_vortex:
            vortex['rotation'] += vortex['rotation_speed']
        
        # Mettre à jour les pépinières stellaires
        for nursery in self.stellar_nurseries:
            nursery['x'] += nursery['drift_x']
            nursery['y'] += nursery['drift_y']
            nursery['pulse_offset'] += 0.03
        
        # Mettre à jour les champs quantiques
        for field in self.quantum_fields:
            field['phase_offset'] += field['oscillation_speed']
            for particle in field['particles']:
                particle['quantum_state'] += 0.05
                particle['entanglement'] += 0.08
        
        # Mettre à jour les flux astraux
        for stream in self.astral_streams:
            stream['flow_offset'] += stream['flow_speed']
        
        # Mettre à jour les failles du vide
        for rift in self.void_rifts:
            for particle in rift['void_particles']:
                particle['offset'] += particle['drift'] * 0.01
                if particle['offset'] > 1:
                    particle['offset'] = 0
                elif particle['offset'] < 0:
                    particle['offset'] = 1
        
        # Mettre à jour les cascades d'énergie
        for cascade in self.energy_cascades:
            for node in cascade['energy_nodes']:
                node['pulse_offset'] += cascade['pulse_frequency']
        
        # Mettre à jour les déchirures dimensionnelles
        for tear in self.dimensional_tears:
            tear['dimensional_phase'] += 0.04
    
    def draw(self, screen, camera_x):
        """Dessine le fond du Cœur d'Astralis"""
        # Fond de base - Vide cosmique profond
        base_color = (5, 0, 20)
        cosmic_intensity = int(10 + 5 * math.sin(self.cosmic_pulse))
        background_color = (
            base_color[0] + cosmic_intensity,
            base_color[1],
            base_color[2] + cosmic_intensity // 2
        )
        screen.fill(background_color)
        
        # Dessiner les vortex cosmiques (arrière-plan lointain)
        self.draw_cosmic_vortex(screen, camera_x)
        
        # Dessiner les pépinières stellaires
        self.draw_stellar_nurseries(screen, camera_x)
        
        # Dessiner les déchirures dimensionnelles
        self.draw_dimensional_tears(screen, camera_x)
        
        # Dessiner les failles du vide
        self.draw_void_rifts(screen, camera_x)
        
        # Dessiner les champs quantiques
        self.draw_quantum_fields(screen, camera_x)
        
        # Dessiner les cascades d'énergie
        self.draw_energy_cascades(screen, camera_x)
        
        # Dessiner les flux astraux (premier plan)
        self.draw_astral_streams(screen, camera_x)
    
    def draw_cosmic_vortex(self, screen, camera_x):
        """Dessine les vortex cosmiques"""
        for vortex in self.cosmic_vortex:
            draw_x = vortex['x'] - camera_x * 0.1  # Parallaxe lente
            
            if draw_x + vortex['size'] >= -100 and draw_x <= SCREEN_WIDTH + 100:
                vortex_surface = pygame.Surface((vortex['size'], vortex['size']), pygame.SRCALPHA)
                
                # Dessiner les spirales du vortex
                center_x = vortex['size'] // 2
                center_y = vortex['size'] // 2
                
                for spiral in range(5):
                    spiral_radius = (spiral + 1) * vortex['size'] // 12
                    spiral_points = []
                    
                    for angle_step in range(0, 360, 10):
                        angle = math.radians(angle_step) + vortex['rotation'] + spiral * 0.5
                        spiral_x = center_x + math.cos(angle) * spiral_radius
                        spiral_y = center_y + math.sin(angle) * spiral_radius
                        spiral_points.append((spiral_x, spiral_y))
                    
                    if len(spiral_points) > 2:
                        spiral_alpha = max(0, min(255, int(vortex['intensity'] * 60 / (spiral + 1))))
                        spiral_color = (
                            max(0, min(255, 100 + int(50 * math.sin(vortex['color_shift'] + spiral)))),
                            max(0, min(255, 50 + int(30 * math.cos(vortex['color_shift'] + spiral)))),
                            max(0, min(255, 150 + int(80 * math.sin(vortex['color_shift'] + spiral * 0.7)))),
                            spiral_alpha
                        )
                        
                        for i in range(len(spiral_points) - 1):
                            pygame.draw.line(vortex_surface, spiral_color, 
                                           spiral_points[i], spiral_points[i + 1], 3)
                
                screen.blit(vortex_surface, (draw_x, vortex['y']))
    
    def draw_stellar_nurseries(self, screen, camera_x):
        """Dessine les pépinières stellaires"""
        for nursery in self.stellar_nurseries:
            draw_x = nursery['x'] - camera_x * 0.3  # Parallaxe moyenne
            
            if draw_x + nursery['width'] >= -50 and draw_x <= SCREEN_WIDTH + 50:
                # Nébuleuse de fond
                nebula_surface = pygame.Surface((nursery['width'], nursery['height']), pygame.SRCALPHA)
                
                pulse_intensity = 0.5 + 0.3 * math.sin(nursery['pulse_offset'])
                nebula_alpha = max(0, min(255, int(40 * pulse_intensity)))
                
                for layer in range(3):
                    layer_color = (
                        max(0, min(255, int(nursery['nebula_color'][0] * pulse_intensity))),
                        max(0, min(255, int(nursery['nebula_color'][1] * pulse_intensity))),
                        max(0, min(255, int(nursery['nebula_color'][2] * pulse_intensity))),
                        max(0, min(255, nebula_alpha - layer * 10))
                    )
                    
                    layer_rect = (
                        layer * 10, layer * 5,
                        nursery['width'] - layer * 20,
                        nursery['height'] - layer * 10
                    )
                    pygame.draw.ellipse(nebula_surface, layer_color, layer_rect)
                
                screen.blit(nebula_surface, (draw_x, nursery['y']))
                
                # Étoiles en formation
                for star in range(nursery['star_count']):
                    star_x = draw_x + (star * 37) % nursery['width']
                    star_y = nursery['y'] + (star * 23) % nursery['height']
                    
                    star_brightness = 0.3 + 0.7 * math.sin(self.time_offset * 2 + star * 0.5)
                    star_size = max(1, int(2 + star_brightness * 3))
                    star_color = (
                        max(0, min(255, int(255 * star_brightness))),
                        max(0, min(255, int(200 * star_brightness))),
                        max(0, min(255, int(150 * star_brightness)))
                    )
                    
                    if 0 <= star_x <= SCREEN_WIDTH and 0 <= star_y <= SCREEN_HEIGHT:
                        pygame.draw.circle(screen, star_color, (int(star_x), int(star_y)), star_size)
    
    def draw_dimensional_tears(self, screen, camera_x):
        """Dessine les déchirures dimensionnelles"""
        for tear in self.dimensional_tears:
            draw_x = tear['x'] - camera_x * 0.4
            
            if draw_x + tear['width'] >= -50 and draw_x <= SCREEN_WIDTH + 50:
                # Distorsion de la réalité
                distortion = math.sin(tear['dimensional_phase']) * tear['reality_distortion'] * 10
                
                tear_surface = pygame.Surface((tear['width'], tear['height']), pygame.SRCALPHA)
                
                # Couches de la déchirure
                for layer in range(5):
                    layer_alpha = max(0, min(255, int(tear['tear_intensity'] * 80 / (layer + 1))))
                    layer_color = (
                        max(0, min(255, int(tear['otherworld_color'][0] * (1 - layer * 0.1)))),
                        max(0, min(255, int(tear['otherworld_color'][1] * (1 - layer * 0.1)))),
                        max(0, min(255, int(tear['otherworld_color'][2] * (1 - layer * 0.1)))),
                        layer_alpha
                    )
                    
                    layer_rect = (
                        layer * 5, layer * 8,
                        tear['width'] - layer * 10,
                        tear['height'] - layer * 16
                    )
                    pygame.draw.ellipse(tear_surface, layer_color, layer_rect)
                
                screen.blit(tear_surface, (draw_x + distortion, tear['y']))
                
                # Particules d'autre dimension
                for particle in range(15):
                    particle_x = draw_x + (particle * 17) % tear['width'] + distortion
                    particle_y = tear['y'] + (particle * 13) % tear['height']
                    
                    particle_phase = self.dimensional_shift + particle * 0.3
                    particle_alpha = max(0, min(255, int(100 + 50 * math.sin(particle_phase))))
                    particle_color = (
                        tear['otherworld_color'][0],
                        tear['otherworld_color'][1], 
                        tear['otherworld_color'][2],
                        particle_alpha
                    )
                    
                    if 0 <= particle_x <= SCREEN_WIDTH and 0 <= particle_y <= SCREEN_HEIGHT:
                        particle_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
                        pygame.draw.circle(particle_surface, particle_color, (3, 3), 3)
                        screen.blit(particle_surface, (particle_x - 3, particle_y - 3))
    
    def draw_void_rifts(self, screen, camera_x):
        """Dessine les failles du vide"""
        for rift in self.void_rifts:
            draw_x = rift['x'] - camera_x * 0.5
            
            if draw_x + rift['length'] >= -50 and draw_x <= SCREEN_WIDTH + 50:
                # Ligne principale de la faille
                end_x = draw_x + math.cos(rift['angle']) * rift['length']
                end_y = rift['y'] + math.sin(rift['angle']) * rift['length']
                
                # Distorsion spatiale
                distortion = math.sin(self.time_offset * 3) * rift['distortion_strength']
                
                # Dessiner la faille
                rift_surface = pygame.Surface((int(abs(end_x - draw_x)) + 20, int(abs(end_y - rift['y'])) + 20), pygame.SRCALPHA)
                
                for thickness in range(rift['tear_width']):
                    line_alpha = max(0, min(255, int(rift['void_intensity'] * 100 / (thickness + 1))))
                    line_color = (
                        max(0, min(255, 50 - thickness * 5)),
                        0,
                        max(0, min(255, 80 - thickness * 8)),
                        line_alpha
                    )
                    
                    offset_x = thickness * math.cos(rift['angle'] + math.pi/2)
                    offset_y = thickness * math.sin(rift['angle'] + math.pi/2)
                    
                    start_point = (10 + offset_x, 10 + offset_y)
                    end_point = (end_x - draw_x + 10 + offset_x, end_y - rift['y'] + 10 + offset_y)
                    
                    pygame.draw.line(rift_surface, line_color, start_point, end_point, 2)
                
                screen.blit(rift_surface, (min(draw_x, end_x) - 10 + distortion, min(rift['y'], end_y) - 10))
                
                # Particules de vide
                for particle in rift['void_particles']:
                    particle_pos = particle['offset'] * rift['length']
                    particle_x = draw_x + math.cos(rift['angle']) * particle_pos + distortion
                    particle_y = rift['y'] + math.sin(rift['angle']) * particle_pos
                    
                    if 0 <= particle_x <= SCREEN_WIDTH and 0 <= particle_y <= SCREEN_HEIGHT:
                        particle_alpha = max(0, min(255, int(particle['intensity'] * 120)))
                        particle_color = (80, 20, 120, particle_alpha)
                        particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                        pygame.draw.circle(particle_surface, particle_color, 
                                         (particle['size'], particle['size']), particle['size'])
                        screen.blit(particle_surface, (particle_x - particle['size'], particle_y - particle['size']))
    
    def draw_quantum_fields(self, screen, camera_x):
        """Dessine les champs quantiques"""
        for field in self.quantum_fields:
            draw_x = field['x'] - camera_x * 0.6
            
            if draw_x + 100 >= -50 and draw_x <= SCREEN_WIDTH + 50:
                # Dessiner les particules quantiques
                for particle in field['particles']:
                    # Position avec oscillation quantique
                    quantum_x = draw_x + particle['local_x'] + math.sin(field['phase_offset'] + particle['quantum_state']) * 20
                    quantum_y = field['y'] + particle['local_y'] + math.cos(field['phase_offset'] + particle['entanglement']) * 15
                    
                    if 0 <= quantum_x <= SCREEN_WIDTH and 0 <= quantum_y <= SCREEN_HEIGHT:
                        # Effet d'intrication quantique
                        entanglement_intensity = 0.5 + 0.5 * math.sin(particle['entanglement'])
                        particle_alpha = max(0, min(255, int(entanglement_intensity * 150)))
                        
                        particle_color = (
                            max(0, min(255, int(100 + entanglement_intensity * 155))),
                            max(0, min(255, int(150 + entanglement_intensity * 105))),
                            max(0, min(255, int(200 + entanglement_intensity * 55))),
                            particle_alpha
                        )
                        
                        particle_surface = pygame.Surface((particle['size'] * 4, particle['size'] * 4), pygame.SRCALPHA)
                        pygame.draw.circle(particle_surface, particle_color, 
                                         (particle['size'] * 2, particle['size'] * 2), particle['size'])
                        screen.blit(particle_surface, (quantum_x - particle['size'] * 2, quantum_y - particle['size'] * 2))
    
    def draw_energy_cascades(self, screen, camera_x):
        """Dessine les cascades d'énergie"""
        for cascade in self.energy_cascades:
            draw_x = cascade['x'] - camera_x * 0.7
            
            if draw_x + 160 >= -50 and draw_x <= SCREEN_WIDTH + 50:
                # Dessiner les connexions entre nœuds
                for i, node1 in enumerate(cascade['energy_nodes']):
                    for j, node2 in enumerate(cascade['energy_nodes'][i+1:], i+1):
                        node1_x = draw_x + node1['local_x']
                        node1_y = cascade['y'] + node1['local_y']
                        node2_x = draw_x + node2['local_x']
                        node2_y = cascade['y'] + node2['local_y']
                        
                        # Intensité de la connexion
                        connection_pulse = math.sin(node1['pulse_offset']) * math.sin(node2['pulse_offset'])
                        connection_alpha = max(0, min(255, int(cascade['connection_strength'] * 80 * abs(connection_pulse))))
                        
                        if connection_alpha > 20:
                            connection_color = (
                                cascade['cascade_color'][0],
                                cascade['cascade_color'][1],
                                cascade['cascade_color'][2],
                                connection_alpha
                            )
                            connection_surface = pygame.Surface((int(abs(node2_x - node1_x)) + 10, int(abs(node2_y - node1_y)) + 10), pygame.SRCALPHA)
                            pygame.draw.line(connection_surface, connection_color, 
                                           (5, 5), (node2_x - node1_x + 5, node2_y - node1_y + 5), 2)
                            screen.blit(connection_surface, (min(node1_x, node2_x) - 5, min(node1_y, node2_y) - 5))
                
                # Dessiner les nœuds d'énergie
                for node in cascade['energy_nodes']:
                    node_x = draw_x + node['local_x']
                    node_y = cascade['y'] + node['local_y']
                    
                    if 0 <= node_x <= SCREEN_WIDTH and 0 <= node_y <= SCREEN_HEIGHT:
                        energy_pulse = 0.5 + 0.5 * math.sin(node['pulse_offset'])
                        node_size = max(1, int(node['size'] * energy_pulse))
                        node_alpha = max(0, min(255, int(node['energy_level'] * 200 * energy_pulse)))
                        
                        node_color = (
                            cascade['cascade_color'][0],
                            cascade['cascade_color'][1],
                            cascade['cascade_color'][2],
                            node_alpha
                        )
                        node_surface = pygame.Surface((node_size * 2, node_size * 2), pygame.SRCALPHA)
                        pygame.draw.circle(node_surface, node_color, (node_size, node_size), node_size)
                        screen.blit(node_surface, (node_x - node_size, node_y - node_size))
    
    def draw_astral_streams(self, screen, camera_x):
        """Dessine les flux astraux"""
        for stream in self.astral_streams:
            draw_start_x = stream['start_x'] - camera_x * 0.8
            draw_end_x = stream['end_x'] - camera_x * 0.8
            
            if max(draw_start_x, draw_end_x) >= -50 and min(draw_start_x, draw_end_x) <= SCREEN_WIDTH + 50:
                # Dessiner le flux par segments
                for segment in range(stream['segments']):
                    segment_progress = segment / stream['segments']
                    next_progress = (segment + 1) / stream['segments']
                    
                    # Position interpolée
                    seg_start_x = draw_start_x + (draw_end_x - draw_start_x) * segment_progress
                    seg_start_y = stream['start_y'] + (stream['end_y'] - stream['start_y']) * segment_progress
                    seg_end_x = draw_start_x + (draw_end_x - draw_start_x) * next_progress
                    seg_end_y = stream['start_y'] + (stream['end_y'] - stream['start_y']) * next_progress
                    
                    # Effet de flux
                    flow_wave = math.sin(segment_progress * 4 * math.pi + stream['flow_offset'] * 0.1)
                    segment_alpha = max(0, min(255, int(150 + 50 * flow_wave)))
                    
                    segment_color = (
                        stream['energy_color'][0],
                        stream['energy_color'][1],
                        stream['energy_color'][2],
                        segment_alpha
                    )
                    
                    if (0 <= seg_start_x <= SCREEN_WIDTH or 0 <= seg_end_x <= SCREEN_WIDTH):
                        stream_surface = pygame.Surface((int(abs(seg_end_x - seg_start_x)) + stream['width'], 
                                                       int(abs(seg_end_y - seg_start_y)) + stream['width']), pygame.SRCALPHA)
                        pygame.draw.line(stream_surface, segment_color, 
                                       (stream['width']//2, stream['width']//2), 
                                       (seg_end_x - seg_start_x + stream['width']//2, 
                                        seg_end_y - seg_start_y + stream['width']//2), 
                                       stream['width'])
                        screen.blit(stream_surface, (min(seg_start_x, seg_end_x) - stream['width']//2, 
                                                   min(seg_start_y, seg_end_y) - stream['width']//2)) 