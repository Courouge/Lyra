import json
import os
from datetime import datetime
from settings import *

class SaveSystem:
    """Système de sauvegarde pour conserver les progrès du joueur"""
    
    def __init__(self):
        self.save_file = "save_data.json"
        self.backup_file = "save_data_backup.json"
        self.default_save_data = {
            "version": "2.2",
            "player_name": "Voyageur Astral",
            "created_date": None,
            "last_played": None,
            "total_playtime": 0,  # en secondes
            
            # Progression des niveaux
            "levels_unlocked": 1,
            "current_level": 0,
            "levels_completed": [],
            
            # Statistiques globales
            "total_fragments_collected": 0,
            "total_score": 0,
            "total_distance_traveled": 0,
            "total_deaths": 0,
            "total_jumps": 0,
            
            # Succès débloqués
            "achievements_unlocked": [],
            "achievement_progress": {},
            
            # Statistiques par niveau
            "level_stats": {
                "0": {"best_score": 0, "best_time": 0, "fragments_collected": 0, "completed": False},
                "1": {"best_score": 0, "best_time": 0, "fragments_collected": 0, "completed": False},
                "2": {"best_score": 0, "best_time": 0, "fragments_collected": 0, "completed": False},
                "3": {"best_score": 0, "best_time": 0, "fragments_collected": 0, "completed": False}
            },
            
            # Options du jeu
            "settings": {
                "music_volume": 0.7,
                "sound_volume": 0.8,
                "fullscreen": False,
                "difficulty": "normal",
                "show_fps": False,
                "particle_effects": True
            },
            
            # Données de session
            "session_count": 0,
            "favorite_level": 0,
            "longest_session": 0
        }
        
        # Charger les données existantes
        self.save_data = self.load_save_data()
    
    def load_save_data(self):
        """Charge les données de sauvegarde depuis le fichier"""
        try:
            # Essayer de charger le fichier principal
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Vérifier la version et migrer si nécessaire
                if data.get("version") != "2.2":
                    data = self.migrate_save_data(data)
                
                # Fusionner avec les données par défaut pour les nouvelles clés
                merged_data = self.merge_with_defaults(data)
                return merged_data
            
            # Essayer le fichier de sauvegarde
            elif os.path.exists(self.backup_file):
                print("⚠️ Fichier principal corrompu, chargement de la sauvegarde...")
                with open(self.backup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return self.merge_with_defaults(data)
            
            # Aucun fichier trouvé, créer une nouvelle sauvegarde
            else:
                print("📁 Création d'une nouvelle sauvegarde...")
                new_data = self.default_save_data.copy()
                new_data["created_date"] = datetime.now().isoformat()
                new_data["last_played"] = datetime.now().isoformat()
                return new_data
                
        except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
            print(f"❌ Erreur lors du chargement de la sauvegarde: {e}")
            print("🔄 Création d'une nouvelle sauvegarde...")
            new_data = self.default_save_data.copy()
            new_data["created_date"] = datetime.now().isoformat()
            new_data["last_played"] = datetime.now().isoformat()
            return new_data
    
    def merge_with_defaults(self, loaded_data):
        """Fusionne les données chargées avec les valeurs par défaut"""
        merged = self.default_save_data.copy()
        
        def deep_merge(default, loaded):
            for key, value in loaded.items():
                if key in default:
                    if isinstance(value, dict) and isinstance(default[key], dict):
                        default[key] = deep_merge(default[key], value)
                    else:
                        default[key] = value
                else:
                    default[key] = value
            return default
        
        result = deep_merge(merged, loaded_data)
        
        # Correction spéciale pour levels_completed qui pourrait être un entier dans les anciennes sauvegardes
        if not isinstance(result.get("levels_completed"), list):
            result["levels_completed"] = []
        
        return result
    
    def migrate_save_data(self, old_data):
        """Migre les anciennes données vers le nouveau format"""
        print(f"🔄 Migration de la sauvegarde version {old_data.get('version', 'inconnue')} vers 2.2...")
        
        # Ajouter les nouvelles clés manquantes
        migrated = self.default_save_data.copy()
        
        # Conserver les données importantes de l'ancienne version
        if "levels_unlocked" in old_data:
            migrated["levels_unlocked"] = old_data["levels_unlocked"]
        if "total_fragments_collected" in old_data:
            migrated["total_fragments_collected"] = old_data["total_fragments_collected"]
        if "achievements_unlocked" in old_data:
            migrated["achievements_unlocked"] = old_data["achievements_unlocked"]
        
        # Mettre à jour la version
        migrated["version"] = "2.2"
        migrated["last_played"] = datetime.now().isoformat()
        
        return migrated
    
    def save_data_to_file(self):
        """Sauvegarde les données dans le fichier"""
        try:
            # Créer une sauvegarde du fichier existant
            if os.path.exists(self.save_file):
                import shutil
                shutil.copy2(self.save_file, self.backup_file)
            
            # Mettre à jour la date de dernière partie
            self.save_data["last_played"] = datetime.now().isoformat()
            self.save_data["session_count"] += 1
            
            # Sauvegarder dans le fichier principal
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.save_data, f, indent=2, ensure_ascii=False)
            
            print("💾 Sauvegarde réussie !")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            return False
    
    def update_level_progress(self, level_index, score, time_taken, fragments_collected, completed=False):
        """Met à jour les statistiques d'un niveau"""
        level_key = str(level_index)
        
        if level_key not in self.save_data["level_stats"]:
            self.save_data["level_stats"][level_key] = {
                "best_score": 0, "best_time": 0, "fragments_collected": 0, "completed": False
            }
        
        level_stats = self.save_data["level_stats"][level_key]
        
        # Mettre à jour les meilleurs scores
        if score > level_stats["best_score"]:
            level_stats["best_score"] = score
        
        if time_taken > 0 and (level_stats["best_time"] == 0 or time_taken < level_stats["best_time"]):
            level_stats["best_time"] = time_taken
        
        # Mettre à jour les fragments
        if fragments_collected > level_stats["fragments_collected"]:
            level_stats["fragments_collected"] = fragments_collected
        
        # Marquer comme complété
        if completed:
            level_stats["completed"] = True
            
            # S'assurer que levels_completed est une liste
            if not isinstance(self.save_data["levels_completed"], list):
                self.save_data["levels_completed"] = []
            
            if level_index not in self.save_data["levels_completed"]:
                self.save_data["levels_completed"].append(level_index)
        
        # Mettre à jour les statistiques globales
        self.save_data["total_score"] = max(self.save_data["total_score"], score)
        self.save_data["total_fragments_collected"] = max(
            self.save_data["total_fragments_collected"], 
            sum(stats["fragments_collected"] for stats in self.save_data["level_stats"].values())
        )
    
    def unlock_level(self, level_index):
        """Débloque un niveau"""
        if level_index >= self.save_data["levels_unlocked"]:
            self.save_data["levels_unlocked"] = level_index + 1
            print(f"🔓 Niveau {level_index + 1} débloqué !")
    
    def unlock_achievement(self, achievement_id):
        """Débloque un succès"""
        if achievement_id not in self.save_data["achievements_unlocked"]:
            self.save_data["achievements_unlocked"].append(achievement_id)
            print(f"🏆 Succès débloqué: {achievement_id}")
    
    def update_achievement_progress(self, achievement_id, progress):
        """Met à jour le progrès d'un succès"""
        self.save_data["achievement_progress"][achievement_id] = progress
    
    def update_global_stats(self, distance_traveled=0, deaths=0, jumps=0):
        """Met à jour les statistiques globales"""
        self.save_data["total_distance_traveled"] += distance_traveled
        self.save_data["total_deaths"] += deaths
        self.save_data["total_jumps"] += jumps
    
    def update_settings(self, setting_name, value):
        """Met à jour une option du jeu"""
        if setting_name in self.save_data["settings"]:
            self.save_data["settings"][setting_name] = value
    
    def get_level_stats(self, level_index):
        """Retourne les statistiques d'un niveau"""
        level_key = str(level_index)
        return self.save_data["level_stats"].get(level_key, {
            "best_score": 0, "best_time": 0, "fragments_collected": 0, "completed": False
        })
    
    def get_total_fragments(self):
        """Retourne le nombre total de fragments collectés"""
        return sum(stats["fragments_collected"] for stats in self.save_data["level_stats"].values())
    
    def is_level_unlocked(self, level_index):
        """Vérifie si un niveau est débloqué"""
        return level_index < self.save_data["levels_unlocked"]
    
    def is_achievement_unlocked(self, achievement_id):
        """Vérifie si un succès est débloqué"""
        return achievement_id in self.save_data["achievements_unlocked"]
    
    def get_achievement_progress(self, achievement_id):
        """Retourne le progrès d'un succès"""
        return self.save_data["achievement_progress"].get(achievement_id, 0)
    
    def get_playtime_formatted(self):
        """Retourne le temps de jeu formaté"""
        total_seconds = self.save_data["total_playtime"]
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
    
    def get_save_summary(self):
        """Retourne un résumé de la sauvegarde"""
        return {
            "player_name": self.save_data["player_name"],
            "levels_unlocked": self.save_data["levels_unlocked"],
            "total_fragments": self.get_total_fragments(),
            "achievements_count": len(self.save_data["achievements_unlocked"]),
            "playtime": self.get_playtime_formatted(),
            "last_played": self.save_data["last_played"],
            "session_count": self.save_data["session_count"]
        }
    
    def reset_save_data(self):
        """Remet à zéro toutes les données de sauvegarde"""
        confirmation = input("⚠️ Êtes-vous sûr de vouloir effacer toutes les données ? (oui/non): ")
        if confirmation.lower() in ['oui', 'yes', 'y']:
            self.save_data = self.default_save_data.copy()
            self.save_data["created_date"] = datetime.now().isoformat()
            self.save_data["last_played"] = datetime.now().isoformat()
            self.save_data_to_file()
            print("🗑️ Données de sauvegarde effacées !")
            return True
        return False
    
    def export_save_data(self, filename=None):
        """Exporte les données de sauvegarde"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"astralis_save_export_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.save_data, f, indent=2, ensure_ascii=False)
            print(f"📤 Sauvegarde exportée vers {filename}")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'export: {e}")
            return False
    
    def import_save_data(self, filename):
        """Importe des données de sauvegarde"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            # Valider les données importées
            if self.validate_save_data(imported_data):
                self.save_data = self.merge_with_defaults(imported_data)
                self.save_data_to_file()
                print(f"📥 Sauvegarde importée depuis {filename}")
                return True
            else:
                print("❌ Fichier de sauvegarde invalide")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de l'import: {e}")
            return False
    
    def validate_save_data(self, data):
        """Valide la structure des données de sauvegarde"""
        required_keys = ["version", "levels_unlocked", "total_fragments_collected", "level_stats"]
        return all(key in data for key in required_keys)
    
    def start_session(self):
        """Démarre une nouvelle session de jeu"""
        self.session_start_time = datetime.now()
        print(f"🎮 Session démarrée: {self.session_start_time.strftime('%H:%M:%S')}")
    
    def end_session(self):
        """Termine la session de jeu"""
        if hasattr(self, 'session_start_time'):
            session_duration = (datetime.now() - self.session_start_time).total_seconds()
            self.save_data["total_playtime"] += int(session_duration)
            
            if session_duration > self.save_data["longest_session"]:
                self.save_data["longest_session"] = int(session_duration)
            
            print(f"⏱️ Session terminée: {int(session_duration // 60)}m {int(session_duration % 60)}s")
        
        # Sauvegarder automatiquement à la fin de la session
        self.save_data_to_file()
    
    def get_statistics_summary(self):
        """Retourne un résumé des statistiques"""
        # Gérer le cas où levels_completed pourrait être un entier (ancienne sauvegarde)
        levels_completed = self.save_data.get("levels_completed", [])
        if isinstance(levels_completed, int):
            # Convertir l'entier en liste (probablement le nombre de niveaux complétés)
            levels_completed_count = levels_completed
        elif isinstance(levels_completed, list):
            levels_completed_count = len(levels_completed)
        else:
            levels_completed_count = 0
        
        return {
            "Temps de jeu total": self.get_playtime_formatted(),
            "Sessions jouées": self.save_data["session_count"],
            "Plus longue session": f"{self.save_data['longest_session'] // 60}m",
            "Niveaux débloqués": f"{self.save_data['levels_unlocked']}/4",
            "Niveaux complétés": levels_completed_count,
            "Fragments totaux": self.get_total_fragments(),
            "Succès débloqués": len(self.save_data["achievements_unlocked"]),
            "Distance totale": f"{self.save_data['total_distance_traveled']:.0f}m",
            "Sauts effectués": self.save_data["total_jumps"],
            "Morts": self.save_data["total_deaths"]
        } 