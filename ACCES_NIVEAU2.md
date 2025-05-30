# 🎯 Guide Étape par Étape - Accès au Niveau 2

## 🔍 Diagnostic Confirmé ✅
- **Niveaux débloqués** : 2/4 ✅
- **Fragments collectés** : 17 (requis: 15) ✅
- **Forêt Spectrale** : ACCESSIBLE ✅

## 📋 Instructions Détaillées

### Étape 1 : Lancer le Jeu
```bash
python main.py
```

### Étape 2 : Menu Principal
Vous devriez voir :
```
ÉCLATS D'ASTRALIS
~ Un voyage à travers les royaumes stellaires ~

▶ Nouvelle Partie
  Continuer
  Sélection de Niveau    ← SÉLECTIONNEZ CECI
  Options
  Crédits
  Quitter
```

**Action** : Utilisez ↑↓ pour naviguer vers "Sélection de Niveau", puis appuyez sur **Entrée**

### Étape 3 : Écran de Sélection de Niveau
Vous devriez voir :
```
ÉCLATS D'ASTRALIS
Sélection de Niveau

▶ Ruines Lunaires                    ← NIVEAU ACTUEL
  Les vestiges d'une civilisation oubliée...

  Forêt Spectrale                    ← NIVEAU 2 DISPONIBLE
  Les arbres murmurent des secrets anciens...

🔒 Miroirs Célestes                  ← VERROUILLÉ
  La réalité se reflète à l'infini...

🔒 Cœur d'Astralis                   ← VERROUILLÉ
  Le sanctuaire final où tout a commencé...

Fragments totaux: 17
← → : Naviguer | Entrée/Espace : Jouer | Échap : Quitter
```

**Action** : Utilisez **→** (flèche droite) pour naviguer vers "Forêt Spectrale"

### Étape 4 : Sélection de la Forêt Spectrale
Après avoir appuyé sur →, vous devriez voir :
```
ÉCLATS D'ASTRALIS
Sélection de Niveau

  Ruines Lunaires
  Les vestiges d'une civilisation oubliée...

▶ Forêt Spectrale                    ← MAINTENANT SÉLECTIONNÉ
  Les arbres murmurent des secrets anciens...
  Fragments requis: 15

🔒 Miroirs Célestes
  La réalité se reflète à l'infini...
```

**Action** : Appuyez sur **Entrée** ou **Espace** pour lancer le niveau

### Étape 5 : Démarrage du Niveau 2
Vous devriez voir dans la console :
```
🎮 Niveau 2 démarré: Forêt Spectrale
```

Et dans le jeu :
- **Fond vert sombre** mystique
- **Plateformes vertes** organiques
- **Plateformes mobiles** qui bougent verticalement
- **Arbres fantômes** semi-transparents
- **Fragments d'étoiles verts** brillants

## 🚨 Problèmes Possibles et Solutions

### Problème 1 : "Sélection de Niveau" ne fait rien
**Solution** : Assurez-vous d'appuyer sur **Entrée** et non sur **Espace** dans le menu principal

### Problème 2 : Impossible de naviguer dans la sélection de niveau
**Solution** : Utilisez les **flèches directionnelles** ← → et non WASD

### Problème 3 : Le niveau 2 n'apparaît pas
**Solution** : Vérifiez que vous voyez "2/4 niveaux débloqués" dans les statistiques

### Problème 4 : Le jeu lance toujours le niveau 1
**Solution** : Assurez-vous de naviguer avec → vers "Forêt Spectrale" avant d'appuyer sur Entrée

## 🎮 Contrôles Exacts

### Dans le Menu Principal
- **↑↓** : Naviguer entre les options
- **Entrée** : Sélectionner l'option

### Dans la Sélection de Niveau
- **←→** : Naviguer entre les niveaux
- **Entrée/Espace** : Lancer le niveau sélectionné
- **Échap** : Retour au menu principal

### Dans le Jeu (Niveau 2)
- **←→** : Déplacer Lyra
- **Espace** : Sauter
- **Échap** : Pause
- **M** : Retour au menu (en fin de niveau)

## 🔧 Test Rapide

Si vous voulez tester rapidement, voici un script :

```bash
# Dans le terminal
python debug_level_select.py
```

Cela vous confirmera que le niveau 2 est bien accessible.

## 🌲 Ce que Vous Devriez Voir dans le Niveau 2

### Visuellement
- **Couleur dominante** : Vert mystique
- **Plateformes** : Vertes, largeur variable
- **Certaines plateformes bougent** verticalement (branches flottantes)
- **Arbres semi-transparents** en arrière-plan
- **Fragments verts** au lieu de dorés

### Mécaniques Nouvelles
- **Plateformes mobiles** : Attendez le bon timing pour sauter
- **Ombres spectrales** : Violettes, apparaissent/disparaissent
- **Plus de fragments** : 40% de chance vs 30% niveau 1

## ✅ Checklist de Vérification

Avant de lancer le jeu, vérifiez :
- [ ] Vous êtes dans le bon répertoire (`/home/dev/workspace/Lyra`)
- [ ] L'environnement virtuel est activé (`(venv)` visible)
- [ ] Le jeu se lance sans erreur
- [ ] Vous voyez "2 niveaux débloqués" dans les logs

---

**🎯 Si vous suivez exactement ces étapes, vous devriez pouvoir accéder au niveau 2 !**

*En cas de problème persistant, partagez-moi exactement ce que vous voyez à l'écran.* 🌲✨ 