#!/usr/bin/env python3
"""
Script pour débloquer tous les niveaux d'Éclats d'Astralis
Utile pour tester les nouveaux niveaux 3 et 4
"""

import json
import os
from datetime import datetime

def unlock_all_levels():
    """Débloque tous les niveaux et donne suffisamment de fragments"""
    
    save_file = "save_data.json"
    
    # Charger les données existantes ou créer nouvelles données
    if os.path.exists(save_file):
        with open(save_file, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        print(f"📊 Données actuelles chargées:")
        print(f"   Niveaux débloqués: {save_data.get('levels_unlocked', 1)}")
        print(f"   Fragments totaux: {save_data.get('total_fragments', 0)}")
    else:
        save_data = {
            'player_name': 'Testeur Astral',
            'session_count': 1,
            'playtime': '0m',
            'last_played': datetime.now().isoformat()
        }
        print("📊 Création de nouvelles données de sauvegarde")
    
    # Débloquer tous les niveaux (4 niveaux au total : 0, 1, 2, 3)
    save_data['levels_unlocked'] = 4
    save_data['total_fragments'] = 100  # Plus que suffisant pour tous les niveaux
    save_data['achievements_count'] = 0
    save_data['levels_completed'] = 4
    save_data['distance_total'] = 50000
    save_data['jumps_total'] = 1000
    save_data['deaths_total'] = 0
    
    # Sauvegarder
    with open(save_file, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, indent=2, ensure_ascii=False)
    
    print("✅ Tous les niveaux débloqués !")
    print(f"📊 Nouvelles données:")
    print(f"   Niveaux débloqués: {save_data['levels_unlocked']}/4")
    print(f"   Fragments totaux: {save_data['total_fragments']}")
    print(f"   Niveaux disponibles:")
    print(f"   0: Ruines Lunaires (0 fragments requis)")
    print(f"   1: Forêt Spectrale (15 fragments requis)")
    print(f"   2: Miroirs Célestes (50 fragments requis)")
    print(f"   3: Cœur d'Astralis (75 fragments requis)")
    print()
    print("🎮 Vous pouvez maintenant accéder à tous les niveaux !")
    print("🚀 Lancez le jeu avec: python main.py")

if __name__ == "__main__":
    unlock_all_levels() 