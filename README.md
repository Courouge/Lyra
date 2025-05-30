# 🌟 Éclats d'Astralis ✨

**Version 2.3 - Menu Principal et Sauvegarde Persistante**

Un jeu de plateforme mystique où vous incarnez Lyra, un esprit lumineux qui traverse les royaumes stellaires pour collecter les fragments d'étoiles et restaurer l'équilibre cosmique.

![Version](https://img.shields.io/badge/Version-2.3-gold)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

## 🎮 Nouvelles Fonctionnalités v2.3

### 🏠 Menu Principal Complet
- **Navigation fluide** avec effets visuels et particules d'étoiles
- **Écrans multiples** : Menu principal, options, crédits, sélection de niveau
- **Effets de survol** animés avec auras lumineuses
- **Interface intuitive** avec contrôles clavier

### 💾 Sauvegarde Persistante
- **Progression automatique** conservée entre les sessions
- **Statistiques complètes** : temps de jeu, sessions, meilleurs scores
- **Migration de données** compatible avec les anciennes versions
- **Sauvegarde de sécurité** avec fichier de backup automatique
- **Export/Import** de sauvegardes

### 🌍 Niveaux Spécialisés
- **Ruines Lunaires** : Niveau classique d'introduction
- **Forêt Spectrale** : Plateformes mobiles et arbres fantômes
- **Miroirs Célestes** : Portails de téléportation et gravité inversée
- **Cœur d'Astralis** : Niveau final avec difficulté maximale

## 🎯 Mécaniques de Gameplay

### 🏃‍♀️ Mouvement de Base
- **Déplacement latéral** fluide avec inertie
- **Saut principal** avec physique réaliste
- **Double saut** pour atteindre les plateformes éloignées
- **Atterrissage parfait** avec bonus de score

### 🌟 Collectibles
- **Fragments d'étoiles** : Objectif principal, 100% accessibles
- **Orbes de pouvoir** : Capacités temporaires spéciales
- **Zones secrètes** : Bonus cachés pour les explorateurs

### 👻 Obstacles et Défis
- **Ombres astrales** : Ennemis flottants à éviter
- **Ombres spectrales** : Variantes avec comportements spéciaux
- **Plateformes mobiles** : Timing et précision requis
- **Zones de gravité** : Mécaniques de gravité inversée

### 🔮 Pouvoirs Temporaires
- **Saut Astral** (Bleu) : Double saut amélioré
- **Lévitation** (Orange) : Flotte pendant 2 secondes
- **Bouclier Lumineux** (Jaune) : Traverse les ombres sans dégâts
- **Éclat de Vitesse** (Violet) : Mouvement accéléré

## 🎨 Caractéristiques Visuelles

### 🌌 Ambiance Mystique
- **Fond étoilé** avec parallaxe multicouche
- **Particules mystiques** autour de Lyra
- **Effets de lueur** sur tous les éléments interactifs
- **Palette de couleurs** évolutive selon les niveaux

### ✨ Effets Spéciaux
- **Plateformes cristallines** avec scintillements
- **Portails miroirs** avec particules orbitales
- **Arbres fantômes** semi-transparents
- **Formations cristallines** animées

## 🏆 Système de Succès

- **Atterrissage Parfait** : 10 atterrissages parfaits d'affilée
- **Maître des Ombres** : Terminer un niveau sans toucher d'ombre
- **Collectionneur Parfait** : Collecter 100% des fragments d'un niveau
- **Coureur Astral** : Terminer un niveau en moins de 2 minutes
- **Explorateur Mystique** : Découvrir 5 zones secrètes
- **Maître des Combos** : 20 sauts consécutifs sans toucher le sol

## 🎮 Contrôles

### Menu Principal
- **↑↓** ou **W/S** : Naviguer dans les menus
- **Entrée** ou **Espace** : Sélectionner une option
- **Échap** : Retour/Quitter

### En Jeu
- **←→** ou **A/D** : Déplacement latéral
- **Espace** ou **↑** : Saut principal
- **Espace** (en l'air) : Double saut
- **Échap** : Pause/Reprendre
- **M** : Retour au menu principal
- **R** : Redémarrer le niveau (en game over)

### Sélection de Niveau
- **←→** : Changer de niveau
- **Entrée** : Lancer le niveau sélectionné
- **Échap** : Retour au menu principal

## 📊 Système de Progression

### 🔓 Déblocage de Niveaux
- **Ruines Lunaires** : Disponible dès le début
- **Forêt Spectrale** : 25 fragments requis
- **Miroirs Célestes** : 50 fragments requis
- **Cœur d'Astralis** : 75 fragments requis

### 📈 Statistiques Suivies
- Temps de jeu total et par session
- Meilleurs scores et temps par niveau
- Fragments collectés par niveau
- Nombre de morts et de sauts
- Distance totale parcourue
- Succès débloqués

## 🛠️ Installation et Lancement

### Prérequis
```bash
Python 3.8+
Pygame 2.0+
```

### Installation
```bash
# Cloner le repository
git clone [repository-url]
cd Lyra

# Installer les dépendances
pip install pygame

# Lancer le jeu
python main.py
```

### Installation avec environnement virtuel (recommandé)
```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Linux/Mac:
source venv/bin/activate
# Sur Windows:
venv\Scripts\activate

# Installer les dépendances
pip install pygame

# Lancer le jeu
python main.py
```

## 📁 Structure du Projet

```
Lyra/
├── main.py                 # Point d'entrée principal avec menu
├── game.py                 # Logique principale du jeu
├── settings.py             # Configuration et constantes
├── entities/               # Entités du jeu
│   ├── lyra.py            # Personnage principal
│   ├── platform.py        # Plateformes
│   ├── star_fragment.py   # Fragments collectibles
│   ├── shadow.py          # Ombres ennemies
│   ├── end_portal.py      # Portail de fin
│   └── power_manager.py   # Gestionnaire de pouvoirs
├── levels/                 # Générateurs de niveaux
│   ├── level_generator.py           # Générateur classique
│   ├── spectral_forest_generator.py # Forêt Spectrale
│   ├── celestial_mirrors_generator.py # Miroirs Célestes
│   ├── level_manager.py    # Gestionnaire de progression
│   └── zone_manager.py     # Gestionnaire de zones
├── menu/                   # Système de menu
│   └── main_menu.py       # Menu principal
├── systems/                # Systèmes du jeu
│   ├── achievement_system.py # Système de succès
│   └── save_system.py     # Système de sauvegarde
├── assets/                 # Ressources visuelles
│   └── background.py      # Fond étoilé
├── README.md              # Documentation
├── CHANGELOG.md           # Historique des versions
└── save_data.json         # Fichier de sauvegarde (généré)
```

## 🔧 Configuration

### Paramètres de Difficulté
Le jeu propose plusieurs niveaux de difficulté configurables dans `settings.py` :

- **Facile** : Plateformes plus larges, sauts plus puissants
- **Normal** : Équilibrage standard
- **Difficile** : Plateformes plus petites, plus d'obstacles

### Personnalisation
- Vitesse de défilement ajustable
- Nombre de particules configurable
- Effets visuels activables/désactivables
- Volume sonore (préparé pour future implémentation)

## 🎯 Conseils de Jeu

### 🌟 Pour les Débutants
1. **Maîtrisez le double saut** : Essential pour atteindre les plateformes éloignées
2. **Collectez les fragments** : Ils débloquent de nouveaux niveaux
3. **Évitez les ombres** : Elles réduisent votre score et activent l'invincibilité temporaire
4. **Utilisez les pouvoirs** : Les orbes donnent des capacités temporaires puissantes

### 🏆 Pour les Experts
1. **Atterrissages parfaits** : Atterrissez au centre des plateformes pour des bonus
2. **Combos de sauts** : Enchaînez les sauts sans toucher le sol
3. **Exploration** : Cherchez les zones secrètes pour des fragments bonus
4. **Optimisation de temps** : Utilisez les portails et pouvoirs pour des parcours rapides

## 🐛 Résolution de Problèmes

### Problèmes Courants
- **Jeu lent** : Réduisez le nombre de particules dans `settings.py`
- **Sauvegarde corrompue** : Le jeu utilise automatiquement le fichier de backup
- **Contrôles non responsifs** : Vérifiez que Pygame est correctement installé

### Fichiers de Sauvegarde
- **Emplacement** : `save_data.json` dans le dossier du jeu
- **Backup** : `save_data_backup.json` créé automatiquement
- **Reset** : Supprimez `save_data.json` pour recommencer

## 🤝 Contribution

Ce projet est développé en collaboration entre IA et humain. Les contributions sont les bienvenues !

### Idées d'Améliorations
- Nouveaux types de plateformes
- Mécaniques de gameplay innovantes
- Effets visuels et sonores
- Niveaux additionnels
- Système de classement en ligne

## 📜 Licence

Ce projet est développé à des fins éducatives et de démonstration.

## 🙏 Remerciements

- **Pygame Community** : Pour l'excellent framework
- **Inspiration** : Jeux de plateforme classiques et modernes
- **Collaboration IA-Humain** : Démonstration des possibilités créatives

---

*"Dans les éclats d'Astralis, chaque fragment collecté rapproche l'univers de l'harmonie parfaite..."* ✨

**Développé avec ❤️ et Pygame** 