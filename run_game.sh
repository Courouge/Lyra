#!/bin/bash

# Script de lancement pour Éclats d'Astralis
echo "🌟 Lancement d'Éclats d'Astralis..."

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
    
    echo "📥 Installation de Pygame..."
    source venv/bin/activate
    pip install pygame
else
    echo "✅ Environnement virtuel trouvé"
fi

# Activer l'environnement virtuel et lancer le jeu
echo "🚀 Démarrage du jeu..."
source venv/bin/activate
python main.py

echo "🌙 Merci d'avoir joué !" 