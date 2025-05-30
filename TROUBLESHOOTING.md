# Guide de Dépannage - Éclats d'Astralis 🔧

## Erreurs Courantes et Solutions

### ❌ Erreur : 'float' object cannot be interpreted as an integer
**Cause** : Problème de conversion de types dans les calculs
**Solution** : ✅ Corrigé dans la version actuelle

### ❌ Erreur : externally-managed-environment
**Cause** : Tentative d'installation de paquets Python dans l'environnement système
**Solutions** :
```bash
# Option 1 : Utiliser le script automatique (recommandé)
./run_game.sh

# Option 2 : Créer un environnement virtuel manuellement
python3 -m venv venv
source venv/bin/activate
pip install pygame

# Option 3 : Installation système
sudo apt install python3-pygame
```

### ❌ Erreur : python3-venv not found
**Cause** : Module venv non installé
**Solution** :
```bash
sudo apt install python3-venv
```

### ❌ Erreur : pygame not found
**Cause** : Pygame non installé ou environnement virtuel non activé
**Solutions** :
```bash
# Vérifier l'activation de l'environnement virtuel
source venv/bin/activate

# Installer pygame
pip install pygame

# Ou utiliser le script automatique
./run_game.sh
```

### ❌ Erreur : Permission denied sur run_game.sh
**Cause** : Script non exécutable
**Solution** :
```bash
chmod +x run_game.sh
```

### ❌ Jeu lent ou saccadé
**Causes possibles** :
- Système avec peu de RAM
- Carte graphique ancienne
- Trop d'applications ouvertes

**Solutions** :
- Fermer les autres applications
- Réduire la résolution dans `settings.py`
- Diminuer le nombre d'étoiles de fond (`BACKGROUND_STARS`)

### ❌ Pas de son
**Cause** : Le jeu n'a pas encore d'audio implémenté
**Note** : Fonctionnalité prévue pour les futures versions

## Vérification de l'Installation

### Test Rapide
```bash
# Vérifier Python
python3 --version

# Vérifier Pygame (dans l'environnement virtuel)
source venv/bin/activate
python -c "import pygame; print(pygame.version.ver)"
```

### Structure des Fichiers
Vérifiez que tous ces fichiers sont présents :
```
Lyra/
├── entities/
│   ├── __init__.py
│   ├── lyra.py
│   ├── platform.py
│   ├── star_fragment.py
│   └── shadow.py
├── levels/
│   ├── __init__.py
│   ├── level_generator.py
│   └── level_2.py
├── assets/
│   ├── __init__.py
│   └── background.py
├── venv/
├── main.py
├── game.py
├── settings.py
├── requirements.txt
└── run_game.sh
```

## Performance et Optimisation

### Paramètres Modifiables dans settings.py
```python
# Réduire pour améliorer les performances
BACKGROUND_STARS = 50  # au lieu de 100
FPS = 30              # au lieu de 60
SCREEN_WIDTH = 800    # au lieu de 1200
SCREEN_HEIGHT = 600   # au lieu de 800
```

### Surveillance des Performances
- Le jeu vise 60 FPS
- Utilisation mémoire normale : ~50-100 MB
- Temps de démarrage : 2-5 secondes

## Support et Aide

### Informations Système Utiles
```bash
# Version du système
lsb_release -a

# Version Python
python3 --version

# Espace disque
df -h

# Mémoire disponible
free -h
```

### Logs de Débogage
Pour activer les logs détaillés, modifiez `main.py` :
```python
import traceback

# Dans la section except Exception as e:
traceback.print_exc()
```

### Réinitialisation Complète
Si tout échoue :
```bash
# Supprimer l'environnement virtuel
rm -rf venv

# Relancer l'installation
./run_game.sh
```

## Fonctionnalités Connues

### Limitations Actuelles
- Pas d'audio/musique
- Un seul niveau (niveau 2 en développement)
- Pas de sauvegarde de progression
- Interface en français uniquement

### Améliorations Prévues
- Système audio complet
- Multiples niveaux
- Sauvegarde des scores
- Paramètres configurables
- Support multilingue

---

💡 **Astuce** : Utilisez toujours `./run_game.sh` pour un lancement sans problème !

🆘 **Besoin d'aide ?** Vérifiez d'abord ce guide, puis consultez les fichiers README.md et FEATURES.md 