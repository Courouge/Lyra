import pygame
import math
import random
from settings import *

class Lyra:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.radius = LYRA_RADIUS
        
        # Dimensions pour la compatibilité avec les systèmes de collision
        self.width = self.radius * 2
        self.height = self.radius * 2
        
        # Effets visuels
        self.glow_pulse = 0
        self.trail_positions = []
        
        # États spéciaux
        self.gravity_reversed = False
        self.gravity_reverse_timer = 0
        self.invincible = False
        self.invincible_timer = 0
        
        # Système de double saut
        self.can_double_jump = False
        self.double_jump_timer = 0
        self.has_double_jumped = False
        
        # Système de particules simplifié
        self.particles = []
        self.particle_timer = 0
        self.max_particles = 8  # Réduit de 20 à 8
        
    def update(self, keys_pressed, platforms, camera_x=0):
        # Gestion des entrées
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.vel_x = -LYRA_SPEED
        elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.vel_x = LYRA_SPEED
        else:
            self.vel_x *= 0.8  # Friction
            
        if (keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_UP]):
            if self.on_ground:
                # Saut normal - AMÉLIORÉ
                self.vel_y = JUMP_STRENGTH * 1.1  # 10% plus puissant
                self.on_ground = False
                self.has_double_jumped = False
            elif self.can_double_jump and not self.has_double_jumped:
                # Double saut - AMÉLIORÉ
                self.vel_y = JUMP_STRENGTH * 0.9  # Plus puissant qu'avant (était 0.8)
                self.has_double_jumped = True
            
        # Physique simplifiée (plus de gravité inversée)
        self.vel_y += GRAVITY
        
        # Mouvement
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Limitation de la vitesse de chute
        self.vel_y = min(15, self.vel_y)
        
        # Collision avec les plateformes
        self.check_platform_collisions(platforms)
        
        # Limites de mouvement par rapport à la caméra
        # Empêcher Lyra de sortir trop loin à gauche de la caméra
        min_x = camera_x - 50  # Peut aller un peu à gauche de la caméra
        max_x = camera_x + SCREEN_WIDTH + 50  # Peut aller un peu à droite
        self.x = max(min_x, min(max_x, self.x))
        
        # Mort si tombe hors de l'écran
        if self.y > SCREEN_HEIGHT + 100 or self.y < -100:
            return False  # Game over
            
        # Mise à jour des effets
        self.glow_pulse += 0.2
        self.update_trail()
        self.update_special_states()
        self.update_particles()
        
        return True
        
    def check_platform_collisions(self, platforms):
        self.on_ground = False
        
        for platform in platforms:
            # Collision améliorée - vérifier si Lyra est au-dessus de la plateforme
            if (self.x + self.radius > platform.x and 
                self.x - self.radius < platform.x + platform.width):
                
                # Collision par le haut (atterrissage)
                if (self.vel_y > 0 and 
                    self.y + self.radius >= platform.y and 
                    self.y + self.radius <= platform.y + platform.height + 10):  # Marge d'erreur
                    
                    self.y = platform.y - self.radius
                    self.vel_y = 0
                    self.on_ground = True
                    self.has_double_jumped = False  # Reset du double saut
                    break  # Sortir de la boucle une fois qu'on a trouvé une collision
        
    def update_trail(self):
        # Ajouter la position actuelle à la traînée
        self.trail_positions.append((self.x, self.y))
        
        # Limiter la longueur de la traînée
        if len(self.trail_positions) > 8:
            self.trail_positions.pop(0)
            
    def update_special_states(self):
        # Double saut
        if self.double_jump_timer > 0:
            self.double_jump_timer -= 1
            if self.double_jump_timer == 0:
                self.can_double_jump = False
                
        # Invincibilité
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            if self.invincible_timer == 0:
                self.invincible = False
                
    def activate_double_jump(self):
        """Active le double saut temporairement"""
        self.can_double_jump = True
        self.double_jump_timer = 300  # 5 secondes à 60 FPS
        
    def activate_invincibility(self):
        self.invincible = True
        self.invincible_timer = INVINCIBILITY_DURATION
        
    def draw(self, screen, camera_x):
        draw_x = self.x - camera_x
        
        # Dessiner la traînée lumineuse
        for i, (trail_x, trail_y) in enumerate(self.trail_positions[:-1]):
            alpha = (i + 1) / len(self.trail_positions) * 0.5
            trail_draw_x = trail_x - camera_x
            
            if 0 <= trail_draw_x <= SCREEN_WIDTH:
                # Créer une surface avec alpha pour la traînée
                trail_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
                trail_color = (*COLORS['lyra_glow'], int(255 * alpha))
                pygame.draw.circle(trail_surface, trail_color, (self.radius, self.radius), self.radius)
                screen.blit(trail_surface, (trail_draw_x - self.radius, trail_y - self.radius))
        
        # Dessiner l'aura lumineuse (effet de lueur)
        if 0 <= draw_x <= SCREEN_WIDTH:
            # Dessiner d'abord les particules (derrière Lyra)
            self.draw_particles(screen, camera_x)
            
            glow_radius = GLOW_RADIUS + math.sin(self.glow_pulse) * 5
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            
            # Gradient de lueur
            for r in range(int(glow_radius), 0, -2):
                alpha = max(0, 30 - (glow_radius - r) * 2)
                if self.invincible and (self.invincible_timer // 5) % 2:
                    glow_color = (*COLORS['star_fragment'], alpha)
                else:
                    glow_color = (*COLORS['lyra_glow'], alpha)
                pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), r)
            
            screen.blit(glow_surface, (draw_x - glow_radius, self.y - glow_radius))
            
            # Dessiner le corps principal de Lyra
            core_color = COLORS['lyra_core']
            if self.can_double_jump:
                core_color = COLORS['star_fragment']  # Couleur différente avec double saut
                
            pygame.draw.circle(screen, core_color, (int(draw_x), int(self.y)), self.radius)
            
            # Effet de scintillement
            sparkle_color = (255, 255, 255)
            if self.can_double_jump:
                sparkle_color = COLORS['star_fragment']  # Scintillement doré avec double saut
                
            for i in range(3):
                angle = self.glow_pulse * 2 + i * (2 * math.pi / 3)
                sparkle_x = draw_x + math.cos(angle) * (self.radius - 5)
                sparkle_y = self.y + math.sin(angle) * (self.radius - 5)
                pygame.draw.circle(screen, sparkle_color, (int(sparkle_x), int(sparkle_y)), 2) 

    def update_particles(self):
        """Met à jour le système de particules simplifié"""
        # Générer de nouvelles particules moins fréquemment
        self.particle_timer += 1
        if self.particle_timer >= 8:  # Nouvelle particule toutes les 8 frames au lieu de 3
            self.particle_timer = 0
            if len(self.particles) < self.max_particles:
                # Particule simple
                particle = {
                    'x': self.x + random.uniform(-self.radius//2, self.radius//2),
                    'y': self.y + random.uniform(-self.radius//2, self.radius//2),
                    'vel_x': random.uniform(-0.5, 0.5),
                    'vel_y': random.uniform(-1, 0),
                    'life': 30,  # Réduit de 60 à 30 frames
                    'max_life': 30,
                    'size': random.uniform(1, 2),  # Taille réduite
                    'color': COLORS['lyra_glow'] if not self.can_double_jump else COLORS['star_fragment']
                }
                self.particles.append(particle)
        
        # Mettre à jour les particules existantes
        for particle in self.particles[:]:
            particle['life'] -= 1
            particle['x'] += particle['vel_x']
            particle['y'] += particle['vel_y']
            
            # Supprimer les particules mortes
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw_particles(self, screen, camera_x):
        """Dessine les particules simplifiées"""
        for particle in self.particles:
            draw_x = particle['x'] - camera_x
            if -20 <= draw_x <= SCREEN_WIDTH + 20:
                # Calculer l'alpha basé sur la vie restante
                alpha = int((particle['life'] / particle['max_life']) * 150)  # Alpha réduit
                
                # Particule simple sans effets complexes
                color_with_alpha = (*particle['color'], alpha)
                particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, color_with_alpha,
                                 (particle['size'], particle['size']), int(particle['size']))
                screen.blit(particle_surface, (draw_x - particle['size'], particle['y'] - particle['size'])) 