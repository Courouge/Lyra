# Configuration du jeu Éclats d'Astralis

# Dimensions de l'écran
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Couleurs mystiques
COLORS = {
    'background': (10, 5, 25),  # Bleu nuit profond
    'lyra_core': (255, 255, 200),  # Jaune lumineux
    'lyra_glow': (150, 200, 255),  # Bleu clair
    'star_fragment': (255, 215, 0),  # Or
    'shadow': (20, 0, 40),  # Violet très sombre
    'platform': (80, 60, 120),  # Violet mystique
    'star_bg': (200, 200, 255),  # Blanc-bleu pour étoiles de fond
    'text': (255, 255, 255),  # Blanc
}

# Physique du jeu
GRAVITY = 0.7
JUMP_STRENGTH = -16
SCROLL_SPEED = 3
LYRA_SPEED = 6

# Tailles des entités
LYRA_RADIUS = 20
PLATFORM_WIDTH = 150
PLATFORM_HEIGHT = 20
STAR_FRAGMENT_SIZE = 15
SHADOW_SIZE = 30

# Génération procédurale
PLATFORM_SPACING_X = 160
PLATFORM_SPACING_Y_MIN = 80
PLATFORM_SPACING_Y_MAX = 150
STAR_SPAWN_CHANCE = 0.3
SHADOW_SPAWN_CHANCE = 0.2

# Effets visuels
GLOW_RADIUS = 40
STAR_POINTS = 5
BACKGROUND_STARS = 100

# Bonus
GRAVITY_REVERSE_DURATION = 300  # frames
INVINCIBILITY_DURATION = 120  # frames

# Paramètres de difficulté
DIFFICULTY_EASY = {
    'platform_spacing_multiplier': 0.6,  # Plateformes plus rapprochées
    'jump_power_multiplier': 1.2,        # Sauts plus puissants
    'platform_size_bonus': 40,           # Plateformes plus grandes
    'max_jump_distance': 180,            # Distance de saut augmentée
}

DIFFICULTY_NORMAL = {
    'platform_spacing_multiplier': 0.7,  # Espacement normal (actuel)
    'jump_power_multiplier': 1.1,        # Sauts légèrement améliorés
    'platform_size_bonus': 20,           # Taille normale
    'max_jump_distance': 150,            # Distance normale
}

DIFFICULTY_HARD = {
    'platform_spacing_multiplier': 0.9,  # Plateformes plus éloignées
    'jump_power_multiplier': 1.0,        # Sauts normaux
    'platform_size_bonus': 0,            # Plateformes plus petites
    'max_jump_distance': 120,            # Distance réduite
}

# Difficulté actuelle (peut être changée)
CURRENT_DIFFICULTY = DIFFICULTY_NORMAL 