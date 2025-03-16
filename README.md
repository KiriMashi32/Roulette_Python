# Roulette Russe Adventure

<div align="center">

  <img src="public/game-preview.png" alt="Aperçu du jeu" width="600"/>
</div>

<p align="center">
  <em>Une version graphique et animée du jeu classique de la roulette russe créée avec PyGame</em>
</p>

<p align="center">
  <a href="#fonctionnalités">Fonctionnalités</a> •
  <a href="#gameplay">Gameplay</a> •
  <a href="#installation">Installation</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#développement">Développement</a>
</p>

## Fonctionnalités

- **Expérience de jeu immersive** : Animations, musique de fond et retour visuel
- **Mode deux joueurs** : Affrontez un ami avec des pseudos personnalisés
- **Système de défi de mots** : Tapez rapidement des mots pour survivre face à une chambre chargée
- **Scores persistants** : Suivez et sauvegardez les performances des joueurs sur plusieurs parties
- **Journal d'événements dynamique** : Mises à jour du jeu en temps réel affichées dans une console défilante
- **Contrôles musicaux personnalisables** : Ajustez le volume ou activez/désactivez la musique de fond

## Gameplay

Roulette Russe Adventure offre une version moderne du concept classique de la roulette russe :

1. **Configuration** : Les joueurs entrent leurs pseudos et sélectionnent le nombre de balles pour la partie
2. **Tour par tour** : Les joueurs alternent pour appuyer sur la détente d'un revolver virtuel
3. **Défi de mots** : Face à une chambre chargée, les joueurs doivent rapidement taper un mot affiché pour survivre
4. **Score** : Les joueurs gagnent des points lorsque leurs adversaires sont éliminés
5. **Classement global** : Les performances sont suivies à travers les sessions dans un tableau des scores persistant

![Diagramme de Gameplay](https://www.plantuml.com/plantuml/png/pPCzyjCm4CLxdM8lG87A5CoV951a9WtX0egydeZHXrcjFCCHk0KbFeSlXfJns2WcanGfS2VjRzy-wSblaHLnSbOepO7W418cUb-jfEWoOxJfb6SuOAhMNx0FjaUgDlVOccDW8IOzUFUXD6xWasT2WYvYQi9KbNUhTUzf72ngDi7x3FdWpeJG89oLjHXNOhlWMqCkexaAsProus-cJ0eRGWUxY_gU43Wa4f2_PTnyfWryxBhq0mbYoZ8Acd5Wz8pN1cKPjcKsDCf7iCK9cRpcKYxVB5H4fplPm7uSd2Aw6YkAhIcdS65fcz3IDRdAJjhMw4jfgja9g2PyLTqQB7QBg0v4g9VzUmDFYNhJ4yuWseXGAEEVrHX_MkEC7uT5n3TY5jjEzmMzQN1rQRKRPJnaCghKYh-5Rb_9vymrwJPM-L_6AX_5AbySgtn1hF9biSg7iSf_nbeOaNUh1t94Pa8OVy6tp815Y3eGrfnyXbl_Rzgg6D6XvvNS7UmjUqpE_W40)

## Installation

```bash
# Clonez le dépôt
git clone https://github.com/KiriMashi32/Roulette_Python

# Installez les dépendances requises
pip install pygame

# Lancez le jeu
python main.py
```

## Architecture

Le jeu est construit avec une architecture modulaire comprenant ces composants principaux :

- **Classe Game** : Contrôleur central gérant l'état et la logique du jeu
- **Classe Player** : Gère la représentation et les animations des joueurs
- **Composants UI** : Classes Button, TextBox et EventLog pour l'interface
- **Système d'animation** : Gère les effets visuels comme le recul, les secousses d'écran et les transitions
- **Stockage persistant** : Système basé sur JSON pour sauvegarder les scores et l'historique des parties

### Diagramme de classes

```
┌─────────────┐      ┌────────────┐      ┌──────────────┐
│    Game     │◄─────┤   Player   │      │   Button     │
├─────────────┤      ├────────────┤      ├──────────────┤
│ - barillet  │      │ - x, y     │      │ - rect       │
│ - joueur    │      │ - angle    │      │ - color      │
│ - scores    │      │ - image    │      │ - text       │
├─────────────┤      ├────────────┤      ├──────────────┤
│ + shoot()   │      │ + draw()   │      │ + draw()     │
│ + restart() │      │ + reset()  │      │ + is_hovered │
└─────────────┘      └────────────┘      └──────────────┘
      ▲                                          ▲
      │                                          │
      │               ┌─────────────┐            │
      └───────────────┤  EventLog   ├────────────┘
                      ├─────────────┤
                      │ - messages  │
                      │ - rect      │
                      ├─────────────┤
                      │ + draw()    │
                      │ + add_msg() │
                      └─────────────┘
```

## Développement

### Défis techniques

- **Fluidité des animations** : Création de transitions fluides entre les états du jeu
- **Système de défi de mots** : Équilibrage de la difficulté et du timing pour la survie basée sur les compétences
- **Journal d'événements** : Conception d'une interface défilante réactive avec un impact minimal sur les performances
- **Gestion des états** : Gestion des transitions entre plusieurs états du jeu sans problèmes

### Philosophie de conception

Le jeu a été développé avec ces principes à l'esprit :

1. **Retour visuel** : Chaque action fournit une réponse visuelle et auditive immédiate
2. **Difficulté progressive** : Le défi augmente naturellement au cours du gameplay
3. **Tolérance aux erreurs** : Gestion robuste des erreurs pour les entrées utilisateur inattendues
4. **Performance** : Rendu et gestion des événements optimisés pour un gameplay fluide

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
