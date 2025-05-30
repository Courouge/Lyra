# 📝 Changelog - Éclats d'Astralis

## Version 2.3 - Menu Principal et Sauvegarde Persistante 🎮

### 🏠 Menu Principal Complet
- **Menu principal animé** : Navigation fluide avec effets visuels
- **Écrans multiples** : Menu principal, options, crédits, sélection de niveau
- **Particules d'étoiles** : Fond animé avec particules scintillantes
- **Effets de survol** : Animations et auras pour les options sélectionnées

### 💾 Système de Sauvegarde Persistante
- **Sauvegarde automatique** : Progression conservée entre les sessions
- **Statistiques complètes** : Temps de jeu, sessions, meilleurs scores
- **Migration de données** : Compatibilité avec les anciennes sauvegardes
- **Sauvegarde de sécurité** : Fichier de backup automatique
- **Export/Import** : Possibilité d'exporter et importer les sauvegardes

### 🌍 Niveaux Spécialisés avec Mécaniques Uniques
- **Forêt Spectrale** : Plateformes mobiles et arbres fantômes
- **Miroirs Célestes** : Portails de téléportation et zones de gravité inversée
- **Générateurs spécialisés** : Chaque niveau a ses propres mécaniques
- **Effets visuels uniques** : Couleurs et animations spécifiques par niveau

### 🎯 Nouvelles Mécaniques de Gameplay
- **Plateformes mobiles** : Branches flottantes dans la Forêt Spectrale
- **Portails miroirs** : Téléportation instantanée entre portails connectés
- **Zones de gravité inversée** : Gravité modifiée dans certaines zones
- **Formations cristallines** : Éléments décoratifs animés
- **Ombres spectrales** : Ennemis avec comportements spéciaux

### 🎨 Améliorations Visuelles
- **Plateformes cristallines** : Effets de scintillement et reflets
- **Arbres fantômes** : Éléments semi-transparents avec balancement
- **Particules orbitales** : Effets autour des portails
- **Auras dynamiques** : Effets de lueur sur les éléments interactifs

### 🔧 Système de Navigation Amélioré
- **Retour au menu** : Touche M pour retourner au menu depuis n'importe où
- **Navigation intuitive** : Flèches et Entrée pour naviguer
- **États persistants** : Position dans les menus conservée
- **Transitions fluides** : Changements d'état sans coupure

### 📊 Statistiques et Progression
- **Temps de jeu total** : Suivi du temps passé dans le jeu
- **Statistiques par niveau** : Meilleurs scores et temps par niveau
- **Compteur de sessions** : Nombre de fois que le jeu a été lancé
- **Progression globale** : Vue d'ensemble des accomplissements

### 🛠️ Améliorations Techniques
- **Architecture modulaire** : Séparation claire entre menu et jeu
- **Gestion d'erreurs** : Récupération automatique en cas de problème
- **Performance optimisée** : Chargement et sauvegarde efficaces
- **Code extensible** : Facilité d'ajout de nouveaux niveaux

### 🎮 Contrôles Étendus
- **Menu principal** : ↑↓ Naviguer, Entrée Sélectionner, Échap Quitter
- **En jeu** : M pour retourner au menu, R pour redémarrer
- **Sélection de niveau** : ←→ Changer de niveau, Entrée Jouer
- **Pause** : Échap pour pause/reprendre, M pour menu

---

## Version 2.2 - Accessibilité Parfaite 🎯

### 🔧 Corrections d'Accessibilité
- **Fragments d'étoiles 100% accessibles** : Validation automatique de l'atteignabilité depuis les plateformes
- **Ombres dans zones accessibles** : Système de validation pour éviter les positions inaccessibles
- **Orbes de pouvoir optimisés** : Placement intelligent près des plateformes

### 🎮 Améliorations de Génération
- **Validation intelligente** : Vérification automatique de la distance et hauteur pour tous les éléments
- **Système de tentatives** : Jusqu'à 10 essais pour trouver une position valide pour les ombres
- **Zones restreintes** : Limitation des zones de spawn pour garantir l'accessibilité

### 📊 Métriques d'Accessibilité
- **Fragments d'étoiles** : Position limitée à ±20px horizontalement et 35-50px au-dessus des plateformes
- **Ombres** : Maximum 200px horizontalement et 150px verticalement des plateformes
- **Orbes de pouvoir** : Placement à 60px au-dessus des plateformes avec variation de ±30px

### 🧪 Système de Test
- **Script de validation** : `test_accessibility.py` pour vérifier l'accessibilité
- **Tests automatisés** : Validation des fragments, ombres et espacement des plateformes
- **Score global** : Métrique de qualité d'accessibilité du niveau

---

## Version 2.1 - Améliorations de Jouabilité 🎮

### 🔧 Corrections Majeures
- **Espacement des plateformes optimisé** : Réduction de 30% de l'espacement de base
- **Validation des sauts impossibles** : Système automatique pour éviter les gaps infranchissables
- **Fin de niveau accessible** : Plateformes d'approche ajoutées avant le portail final

### ⚡ Améliorations de Gameplay
- **Saut principal renforcé** : +10% de puissance pour faciliter la navigation
- **Double saut amélioré** : Puissance augmentée de 0.8x à 0.9x
- **Plateformes plus grandes** : Taille minimale augmentée de 80 à 100 pixels
- **Niveau plus court** : Longueur réduite de 8000 à 6000 pixels

### 🎯 Ajustements par Section
- **Section normale** : Espacement réduit, hauteur de saut limitée
- **Section facile** : Plateformes encore plus rapprochées et larges
- **Section difficile** : Limitée pour éviter la frustration
- **Section verticale** : Hauteur maximale réduite pour la faisabilité

### 🏁 Fin de Niveau Améliorée
- **3 plateformes d'approche** : Espacement de 120 pixels pour faciliter l'accès
- **Plateforme finale agrandie** : 250x50 pixels (au lieu de 200x40)
- **Portail repositionné** : Plus bas et centré pour un accès facile

### 🛠️ Système de Difficulté
- **Paramètres configurables** : Facile, Normal, Difficile
- **Ajustement dynamique** : Espacement, taille des plateformes, puissance de saut
- **Validation intelligente** : Distance maximale de saut respectée

### 📊 Métriques de Saut
- **Distance maximale** : 150 pixels (ajustable selon difficulté)
- **Différence de hauteur** : 120 pixels maximum
- **Validation automatique** : Ajustement si saut impossible détecté

---

## Version 2.0 - Systèmes Avancés ✨

### 🏰 Système Multi-Niveaux
- 4 royaumes uniques avec progression par fragments
- Écran de sélection avec navigation intuitive
- Ambiances et couleurs spécifiques par niveau

### 🔮 Pouvoirs Temporaires
- 4 pouvoirs collectibles via orbes mystiques
- Effets visuels avec particules orbitales
- Système de durée et cooldown

### 🏆 Système de Succès
- 6 succès avec tracking automatique
- Notifications en temps réel
- Récompenses et déblocages

### 🎨 Effets Visuels Avancés
- Particules mystiques autour de Lyra
- Fond parallaxe multicouche
- Portail de fin animé
- Interface enrichie

---

## Version 1.0 - Base du Jeu 🌟

### 🎮 Fonctionnalités de Base
- Mouvement fluide de Lyra
- Collecte de fragments d'étoiles
- Évitement d'ombres astrales
- Génération procédurale de niveaux

### 🌌 Ambiance Mystique
- Fond étoilé avec parallaxe
- Plateformes cristallines
- Effets de particules
- Système narratif

---

*"Chaque mise à jour rapproche Lyra de la perfection..."* ✨ 