# Fonctionnalités d'Éclats d'Astralis ✨

## Gameplay Principal

### 🌟 Lyra - L'Esprit Lumineux
- **Mouvement fluide** : Déplacement latéral avec les flèches ou WASD
- **Saut dynamique** : Saut principal avec Espace ou Flèche haut
- **Double saut magique** : Bonus temporaire obtenu tous les 5 fragments collectés
- **Physique réaliste** : Gravité, friction et limitation de vitesse
- **Traînée lumineuse** : Effet visuel de particules qui suit Lyra
- **Aura pulsante** : Lueur mystique qui change selon les bonus actifs

### 🏔️ Niveau Procédural Avancé
- **4 types de sections** qui alternent automatiquement :
  - **Section normale** : Équilibre standard entre difficulté et accessibilité
  - **Section rapprochée** : Plateformes plus proches et plus larges (plus facile)
  - **Section éloignée** : Plateformes plus espacées et plus petites (plus difficile)
  - **Section verticale** : Emphasis sur les sauts en hauteur
- **Difficulté progressive** : Les sections deviennent plus challengeantes avec la distance
- **Plateformes flottantes** : Tailles et espacements variables selon la section
- **Génération intelligente** : Évite les sauts impossibles tout en maintenant le défi

### ⭐ Fragments d'Étoiles
- **Collectibles magiques** : Formes d'étoiles dorées avec rotation
- **Particules orbitales** : Effets visuels enchanteurs
- **Système de points** : 100 points par fragment
- **Bonus progressifs** :
  - **Tous les 3 fragments** : Invincibilité temporaire (2 secondes)
  - **Tous les 5 fragments** : Double saut magique (5 secondes)

### 👤 Ombres Astrales
- **Obstacles animés** : Tentacules ondulants et yeux sinistres
- **IA basique** : Mouvement imprévisible
- **Système de dégâts** : -50 points au contact (si pas invincible)
- **Destruction** : Les ombres disparaissent après contact
- **Invincibilité automatique** : Protection temporaire après dégâts

## Système de Bonus

### 🚀 Double Saut Magique
- **Activation** : Collecte de 5 fragments d'étoiles
- **Durée** : 5 secondes (300 frames)
- **Utilisation** : Appuyer sur Espace en l'air après le saut principal
- **Effet visuel** : Lyra devient dorée et scintille
- **Reset** : Se recharge à chaque atterrissage

### 🛡️ Invincibilité
- **Activation** : Collecte de 3 fragments d'étoiles OU contact avec ombre
- **Durée** : 2 secondes (120 frames)
- **Effet visuel** : Aura clignotante dorée
- **Protection** : Immunité contre les ombres astrales

## Interface et Contrôles

### 🎮 Contrôles
- **Déplacement** : Flèches gauche/droite ou A/D
- **Saut** : Espace ou Flèche haut
- **Double saut** : Espace en l'air (si bonus actif)
- **Pause** : Échap
- **Redémarrage** : R (en game over)

### 📊 Interface Utilisateur
- **Score en temps réel** : Points accumulés
- **Compteur de fragments** : Nombre d'étoiles collectées
- **Distance parcourue** : Progression en mètres
- **Indicateurs de bonus** :
  - "DOUBLE SAUT" (texte doré)
  - "INVINCIBLE" (texte bleu)
- **Instructions** : Rappel des contrôles en bas d'écran

## Effets Visuels

### 🌌 Fond Étoilé Multicouche
- **3 couches parallax** :
  - Poussière cosmique (mouvement lent)
  - Nébuleuses colorées (mouvement moyen)
  - Étoiles brillantes (mouvement rapide)
- **Défilement fluide** : Effet de profondeur immersif

### ✨ Effets de Particules
- **Traînée de Lyra** : 8 positions avec transparence dégradée
- **Aura pulsante** : Rayon variable avec respiration lumineuse
- **Cristaux de plateformes** : Scintillements mystiques
- **Particules d'étoiles** : Orbites autour des fragments

### 🎬 Effets d'Impact
- **Tremblement d'écran** : Lors des collisions avec ombres
- **Flash blanc** : Feedback visuel des événements importants
- **Changements de couleur** : Lyra dorée avec bonus actifs

## Système de Caméra

### 📹 Suivi Intelligent
- **Suivi fluide** : Interpolation douce vers la position de Lyra
- **Scroll automatique** : Progression constante vers la droite
- **Limites dynamiques** : Lyra peut reculer légèrement mais pas trop
- **Anticipation** : Caméra positionnée pour voir les obstacles à venir

## États de Jeu

### 🎮 Mode Jeu
- **Gameplay principal** : Saut, collecte, évitement
- **Pause** : Gel complet avec overlay
- **Statistiques temps réel** : Score, distance, fragments

### 💀 Game Over
- **Conditions** : Chute hors de l'écran (haut ou bas)
- **Écran de fin** : Statistiques finales complètes
- **Redémarrage** : Touche R pour recommencer
- **Sauvegarde** : Meilleur score affiché

### ⏸️ Pause
- **Activation** : Touche Échap
- **Overlay** : Fond semi-transparent
- **Reprise** : Même touche pour continuer

## Optimisations Techniques

### ⚡ Performance
- **60 FPS stable** : Optimisé pour un gameplay fluide
- **Nettoyage automatique** : Suppression des éléments hors écran
- **Rendu conditionnel** : Seuls les éléments visibles sont dessinés
- **Gestion mémoire** : Limitation des listes de particules

### 🔧 Architecture
- **Code modulaire** : Séparation claire des responsabilités
- **Configuration centralisée** : Fichier settings.py pour tous les paramètres
- **Extensibilité** : Structure prête pour de nouvelles fonctionnalités

---

## Prochaines Améliorations Prévues

- 🎵 **Système audio** : Musique d'ambiance et effets sonores
- 🏆 **Système de scores** : Sauvegarde des meilleurs scores
- 🌍 **Niveaux multiples** : Différents environnements et thèmes
- 🎨 **Personnalisation** : Skins pour Lyra et options visuelles
- 📱 **Support mobile** : Adaptation pour écrans tactiles

## Personnage Principal - Lyra 🌟

### Apparence et Effets Visuels
- **Corps lumineux** : Cercle doré brillant avec effet de lueur
- **Traînée lumineuse** : Particules qui suivent Lyra avec transparence dégradée
- **Aura pulsante** : Effet de respiration lumineux autour du personnage
- **Scintillement** : 3 points lumineux qui tournent autour de Lyra
- **États visuels** : Couleur change selon les bonus actifs

### Physique et Mouvement
- **Déplacement latéral** : Flèches ou WASD avec friction réaliste
- **Saut** : Espace ou flèche haut avec physique de gravité
- **Gravité inversée** : Bonus qui inverse la gravité temporairement
- **Collision** : Détection précise cercle-rectangle avec les plateformes
- **Limites d'écran** : Empêche Lyra de sortir latéralement

## Environnement et Monde 🌌

### Fond Étoilé Multicouche
- **Poussière cosmique** : 200 particules lointaines (parallax 0.1x)
- **Nébuleuses** : 30 particules colorées avec dérive (parallax 0.3x)
- **Étoiles** : 100 étoiles scintillantes avec croix lumineuses (parallax 0.5x)
- **Gradient de fond** : Transition de couleur verticale
- **Repositionnement automatique** : Les éléments se recyclent

### Plateformes Flottantes
- **Génération procédurale** : Espacement et hauteur variables
- **Cristaux scintillants** : 6 points lumineux qui clignotent
- **Aura mystique** : Effet de lueur autour des plateformes
- **Bordure lumineuse** : Contour coloré pour la visibilité
- **Nettoyage automatique** : Suppression des plateformes hors écran

## Collectibles et Obstacles ⭐

### Fragments d'Étoiles
- **Forme d'étoile** : 5 branches avec rotation continue
- **Effet de flottement** : Mouvement vertical sinusoïdal
- **Particules de scintillement** : 5 particules orbitales
- **Aura pulsante** : Gradient lumineux qui respire
- **Double étoile** : Étoile principale + étoile centrale
- **Points** : 100 points par fragment collecté

### Ombres Astrales
- **Tentacules animés** : 4-7 tentacules qui bougent
- **Yeux sinistres** : Points rouges qui pulsent
- **Aura de ténèbres** : Gradient sombre multicouche
- **Mouvement flottant** : Déplacement vertical aléatoire
- **Destruction** : Disparaissent après collision

## Système de Jeu 🎮

### Score et Progression
- **Score** : Points gagnés par collecte et distance
- **Distance** : Mesure en mètres de progression
- **Fragments collectés** : Compteur de collectibles
- **Difficulté progressive** : Augmente avec la distance

### Bonus et Power-ups
- **Gravité inversée** : Tous les 5 fragments (300 frames)
- **Invincibilité** : Tous les 3 fragments (120 frames)
- **Indicateurs visuels** : Texte et couleurs pour les états actifs

### Caméra et Scroll
- **Suivi fluide** : Caméra qui suit Lyra avec interpolation
- **Scroll automatique** : Mouvement horizontal constant
- **Tremblement d'écran** : Effet lors des collisions
- **Optimisation** : Rendu uniquement des éléments visibles

## Interface Utilisateur 📱

### Affichage en Jeu
- **Score** : Affiché en haut à gauche
- **Fragments** : Compteur avec couleur dorée
- **Distance** : Progression en mètres
- **États actifs** : Indicateurs de bonus en haut à droite
- **Contrôles** : Aide en bas d'écran

### Écrans de Jeu
- **Écran de pause** : Overlay semi-transparent
- **Game Over** : Statistiques finales et option de redémarrage
- **Instructions** : Contrôles et touches de raccourci

## Effets Visuels et Audio 🎨

### Effets de Particules
- **Traînées lumineuses** : Pour Lyra et les collectibles
- **Scintillement** : Points lumineux animés
- **Auras et lueurs** : Gradients avec transparence
- **Flash d'écran** : Feedback visuel pour les événements

### Optimisations Graphiques
- **Surfaces avec alpha** : Pour les effets de transparence
- **Culling** : Rendu uniquement des éléments visibles
- **Recyclage** : Réutilisation des objets hors écran
- **Performance** : 60 FPS stable

## Fonctionnalités Avancées (Niveau 2) 🚀

### Mécaniques Supplémentaires
- **Plateformes mobiles** : Mouvement vertical sinusoïdal
- **Puits de gravité** : Zones d'attraction avec anneaux visuels
- **Checkpoints** : Points de sauvegarde avec particules orbitales
- **Ombres traqueuses** : Ennemis qui suivent le joueur

### Système de Niveaux
- **Générateur modulaire** : Architecture extensible
- **Difficulté adaptative** : Paramètres ajustables
- **Chunks procéduraux** : Génération à la demande
- **Nettoyage intelligent** : Gestion mémoire optimisée

## Architecture Technique 🔧

### Structure Modulaire
```
/entities     - Classes des objets du jeu
/levels       - Générateurs de niveaux
/assets       - Ressources et effets visuels
settings.py   - Configuration centralisée
game.py       - Boucle principale
main.py       - Point d'entrée
```

### Bonnes Pratiques
- **Séparation des responsabilités** : Chaque classe a un rôle précis
- **Configuration centralisée** : Toutes les constantes dans settings.py
- **Gestion d'état** : États de jeu clairs (playing, paused, game_over)
- **Extensibilité** : Architecture prête pour de nouvelles fonctionnalités

## Performance et Optimisation ⚡

### Optimisations Implémentées
- **Rendu conditionnel** : Objets visibles uniquement
- **Nettoyage automatique** : Suppression des objets hors écran
- **Interpolation de caméra** : Mouvement fluide sans saccades
- **Limitation FPS** : 60 FPS pour une expérience stable
- **Gestion mémoire** : Recyclage des objets et surfaces

Cette architecture robuste et ces fonctionnalités riches créent une expérience de jeu mystique et engageante, prête pour l'extension et l'amélioration continue ! ✨ 