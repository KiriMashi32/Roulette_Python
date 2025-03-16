# Roulette Russe Adventure

<div align="center">
  <img src="public/game-preview.png" alt="Game Preview" width="600"/>
</div>

<p align="center">
  <em>An elegant, animated take on the classic Russian Roulette game built with PyGame</em>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#gameplay">Gameplay</a> •
  <a href="#installation">Installation</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#development-insights">Development Insights</a>
</p>

## Features

- **Immersive Gameplay Experience**: Elegant animations, sound effects, and visual feedback
- **Two-Player Mode**: Compete against a friend with personalized nicknames
- **Word Challenge System**: Type words quickly to survive when facing a loaded chamber
- **Persistent Scoring**: Track and save player performances across multiple games
- **Dynamic Event Log**: Real-time game updates displayed in a scrollable console
- **Customizable Music Controls**: Adjust volume or toggle background music

## Gameplay

Roulette Russe Adventure offers a modern twist on the classic Russian Roulette concept:

1. **Setup**: Players enter their nicknames and select the number of bullets for the game
2. **Taking Turns**: Players alternate pulling the trigger on a virtual revolver
3. **Word Challenge**: When facing a loaded chamber, players must quickly type a displayed word to survive
4. **Scoring**: Players earn points by surviving while their opponents are eliminated
5. **Global Ranking**: Performance is tracked across sessions in a persistent leaderboard

<div align="center">
  <img src="public/gameplay-diagram.png" alt="Gameplay Diagram" width="650"/>
</div>

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/roulette-russe-adventure.git

# Navigate to the project directory
cd roulette-russe-adventure

# Install the required dependencies
pip install pygame

# Run the game
python main.py
```

## Architecture

The game is built with a modular architecture featuring these core components:

- **Game Class**: Central controller managing game state and logic
- **Player Class**: Handles player representation and animations
- **UI Components**: Button, TextBox, and EventLog classes for the interface
- **Animation System**: Manages visual effects like recoil, screen shake, and transitions
- **Persistent Storage**: JSON-based system for saving scores and game history

### Class Diagram

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

## Development Insights

### Technical Challenges

- **Smoothing Animations**: Creating fluid transitions between game states
- **Word Challenge System**: Balancing difficulty and timing for skill-based survival
- **Event Logging**: Designing a responsive scrollable interface with minimal performance impact
- **State Management**: Handling transitions between multiple game states without glitches

### Design Philosophy

The game was developed with these principles in mind:

1. **Visual Feedback**: Every action provides immediate visual and auditory response
2. **Progressive Difficulty**: Challenge increases naturally through gameplay
3. **Fault Tolerance**: Robust error handling for unexpected user inputs
4. **Performance**: Optimized rendering and event handling for smooth gameplay

## License

This project is licensed under the MIT License - see the LICENSE file for details.
