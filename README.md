@startuml

class Game {
    - data : dict
    - scores : dict
    - player1_nickname : str
    - player2_nickname : str
    - scores_partie : dict
    - joueur : int
    - barillet : list
    - game_started : bool
    - game_over : bool
    - entering_nicknames : bool
    + start_game() : void
    + shoot() : void
    + restart() : void
    + run() : void
}

class Player {
    - x : int
    - y : int
    - width : int
    - height : int
    - color : tuple
    + draw(surface) : void
    + reset_position() : void
}

class Button {
    - rect : pygame.Rect
    - color : tuple
    - text : str
    + draw(surface) : void
    + handle_event(event) : void
}

class TextBox {
    - rect : pygame.Rect
    - text : str
    + draw(surface) : void
    + handle_event(event) : void
}

class EventLog {
    - messages : list
    + add_message(message) : void
    + draw(surface) : void
}

Game --> Player : "has players"
Game --> Button : "has buttons"
Game --> TextBox : "has text inputs"
Game --> EventLog : "has event log"

@enduml
