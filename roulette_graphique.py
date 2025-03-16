import pygame
import sys
import random
import json
import os
import requests
from datetime import datetime

# Base configuration
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Roulette Russe - PyGame Edition")

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
DARK_BLUE = (44, 62, 80)
LIGHT_BLUE = (52, 73, 94)
WHITE = (236, 240, 241)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
PURPLE = (155, 89, 182)
ORANGE = (243, 156, 18)
GRAY = (149, 165, 166)
RED = (231, 76, 60)
BLACK = (0, 0, 0)

# Score file
SCORES_FILE = "web/scores.json"

# Sound effects paths
SOUNDS = {
    "click": "click.wav",
    "gunshot": "gunshot.wav",
    "empty": "empty.wav",
    "reload": "reload.wav",
    "event": "event.wav",
    "win": "win.wav"
}

# Load sound effects
def load_sounds():
    loaded_sounds = {}
    for name, path in SOUNDS.items():
        if os.path.exists(path):
            try:
                loaded_sounds[name] = pygame.mixer.Sound(path)
            except:
                print(f"Could not load sound: {path}")
    return loaded_sounds

def init_barillet(nb_balles=1):
    barillet = [0] * (6 - nb_balles) + [1] * nb_balles
    random.shuffle(barillet)
    return barillet

def tirer(barillet):
    if barillet.pop(0) == 1:
        return True  # Game over
    else:
        return False  # Game continues

def charger_scores():
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Error reading {SCORES_FILE}. Creating new score file.")
    return {"parties": [], "scores": {}}

def sauvegarder_scores(data):
    try:
        with open(SCORES_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving scores: {e}")

class Button:
    def __init__(self, x, y, width, height, color, text, text_color=WHITE, font_size=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.original_color = color
        self.hover_color = self.get_hover_color(color)
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)
        self.active = True
        self.is_hovering = False
        self.transition_progress = 0
        
    def get_hover_color(self, color):
        r, g, b = color
        return (min(r+20, 255), min(g+20, 255), min(b+20, 255))
        
    def draw(self, surface):
        if self.is_hovering and self.transition_progress < 1:
            self.transition_progress += 0.1
        elif not self.is_hovering and self.transition_progress > 0:
            self.transition_progress -= 0.1
        
        self.transition_progress = max(0, min(1, self.transition_progress))
        
        if self.active:
            r1, g1, b1 = self.original_color
            r2, g2, b2 = self.hover_color
            current_color = (
                int(r1 + (r2 - r1) * self.transition_progress),
                int(g1 + (g2 - g1) * self.transition_progress),
                int(b1 + (b2 - b1) * self.transition_progress)
            )
        else:
            current_color = GRAY
        
        shadow_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width, self.rect.height)
        pygame.draw.rect(surface, (0, 0, 0, 128), shadow_rect, border_radius=8)
        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
        
        pygame.draw.rect(surface, (0, 0, 0, 64), self.rect, 1, border_radius=8)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        surface.blit(text_surface, text_rect)
        
    def is_hovered(self, pos):
        return self.rect.collidepoint(pos) and self.active
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovering = self.rect.collidepoint(event.pos) and self.active
    
    def set_active(self, active):
        self.active = active
        if not active:
            self.is_hovering = False
            self.transition_progress = 0

class TextBox:
    def __init__(self, x, y, width, height, font_size=20, max_chars=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = WHITE
        self.text = ""
        self.font = pygame.font.SysFont("Arial", font_size)
        self.active = False
        self.max_chars = max_chars
        self.blink_timer = 0
        self.cursor_visible = True
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)
        
        border_color = BLUE if self.active else LIGHT_BLUE
        border_width = 2 if self.active else 1
        pygame.draw.rect(surface, border_color, self.rect, border_width, border_radius=5)
        
        text_surface = self.font.render(self.text, True, DARK_BLUE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        surface.blit(text_surface, text_rect)
        
        if self.active:
            self.blink_timer += 1
            if self.blink_timer >= 30:
                self.cursor_visible = not self.cursor_visible
                self.blink_timer = 0
                
            if self.cursor_visible:
                cursor_x = text_rect.right + 2
                if cursor_x > self.rect.right - 5:
                    cursor_x = self.rect.right - 5
                pygame.draw.line(
                    surface, 
                    DARK_BLUE, 
                    (cursor_x, text_rect.top + 2), 
                    (cursor_x, text_rect.bottom - 2),
                    2
                )
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.cursor_visible = True
                self.blink_timer = 0
            else:
                self.active = False
                
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif len(self.text) < self.max_chars:
                self.text += event.unicode

class EventLog:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = DARK_BLUE
        self.border_color = LIGHT_BLUE
        self.font = pygame.font.SysFont("Consolas", 14)
        self.messages = []
        self.max_messages = 12
        self.scroll_offset = 0
        self.scroll_bar_width = 15
        self.scroll_bar_rect = pygame.Rect(x + width - self.scroll_bar_width, y, self.scroll_bar_width, height)
        self.dragging_scrollbar = False
        self.line_height = 22
        
    def add_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        scroll_was_at_bottom = self.scroll_offset == 0
        self.messages.insert(0, f"[{timestamp}] {message}")
        
        if len(self.messages) > self.max_messages:
            self.messages.pop()
        
        if scroll_was_at_bottom:
            self.scroll_to_bottom()
        
        if pygame.display.get_surface():
            self.draw(pygame.display.get_surface())
            pygame.display.flip()
    
    def scroll_to_bottom(self):
        self.scroll_offset = 0
        if pygame.display.get_surface():
            self.draw(pygame.display.get_surface())
            pygame.display.flip()
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if event.button == 4:
                    self.scroll_offset = min(len(self.messages) - self.max_messages, self.scroll_offset + 1) if len(self.messages) > self.max_messages else 0
                elif event.button == 5:
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=10)
        
        total_messages = len(self.messages)
        visible_messages = self.messages[max(0, total_messages - self.max_messages - self.scroll_offset):total_messages - self.scroll_offset]
        
        clip_rect = pygame.Rect(
            self.rect.x + 5, 
            self.rect.y + 5, 
            self.rect.width - self.scroll_bar_width - 10, 
            self.rect.height - 10
        )
        surface.set_clip(clip_rect)
        
        for i, message in enumerate(visible_messages):
            y_pos = self.rect.y + 10 + i * self.line_height
            
            if y_pos < self.rect.bottom - 10:
                if i % 2 == 0:
                    row_bg = pygame.Rect(
                        self.rect.x + 5,
                        y_pos - 2,
                        self.rect.width - self.scroll_bar_width - 10,
                        self.line_height
                    )
                    pygame.draw.rect(surface, (60, 80, 100, 128), row_bg, border_radius=3)
                
                text_color = ORANGE if "⭐" in message else RED if "BOUM" in message else WHITE
                text_surface = self.font.render(message, True, text_color)
                surface.blit(text_surface, (self.rect.x + 10, y_pos))
        
        surface.set_clip(None)
        
        if total_messages > self.max_messages:
            visible_ratio = min(1, self.max_messages / total_messages)
            scroll_height = max(30, visible_ratio * self.rect.height)
            
            max_scroll = total_messages - self.max_messages
            if max_scroll > 0:
                scroll_ratio = 1 - (self.scroll_offset / max_scroll)
                scroll_pos = scroll_ratio * (self.rect.height - scroll_height)
            else:
                scroll_pos = 0
                
            scroll_bar = pygame.Rect(
                self.rect.right - self.scroll_bar_width + 2,
                self.rect.y + scroll_pos,
                self.scroll_bar_width - 4,
                scroll_height
            )
            pygame.draw.rect(surface, LIGHT_BLUE, scroll_bar, border_radius=5)
            pygame.draw.rect(surface, WHITE, scroll_bar, 1, border_radius=5)

class Player:
    def __init__(self, x, y, image_path=None, color=None):
        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.width = 60
        self.height = 120
        self.angle = 0
        
        if image_path and os.path.exists(image_path):
            self.original_image = pygame.image.load(image_path)
            self.original_image = pygame.transform.scale(self.original_image, (self.width, self.height))
            self.image = self.original_image.copy()
        else:
            self.original_image = None
            self.image = None
            self.color = color or BLUE
    
    def draw(self, surface):
        if self.image:
            if self.angle != 0:
                rotated_image = pygame.transform.rotate(self.original_image, self.angle)
                rotated_rect = rotated_image.get_rect(center=(self.x, self.y))
                surface.blit(rotated_image, rotated_rect.topleft)
            else:
                image_rect = self.image.get_rect(center=(self.x, self.y))
                surface.blit(self.image, image_rect.topleft)
        else:
            if self.angle == 0:
                body_rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
                pygame.draw.rect(surface, self.color, body_rect)
                pygame.draw.circle(surface, self.color, (self.x, self.y - self.height//2 + 15), 15)
    
    def reset_position(self):
        self.x = self.original_x
        self.y = self.original_y
        self.angle = 0

class Game:
    def __init__(self):
        self.data = charger_scores()
        self.scores = self.data["scores"]
        self.player1_nickname = ""
        self.player2_nickname = ""
        self.scores_partie = {}
        self.joueur = 1  # Initialiser avec le joueur 1
        self.barillet = []
        self.music_files = ["background_music.mp3", "background_music1.mp3", "background_music2.mp3" , "background_music3.mp3" , "background_music4.mp3"]
        self.current_music_index = 0
        self.game_started = False
        self.game_over = False
        self.entering_nicknames = False
        
        self.gun_image = pygame.image.load("gun.png")
        self.gun_image = pygame.transform.scale(self.gun_image, (100, 50))
        
        # Initialiser l'image du pistolet en mode miroir si le joueur actif est le joueur 2
        if self.joueur == 2:
            self.gun_image = pygame.transform.flip(self.gun_image, True, False)
        
        self.word_challenge_active = False
        self.challenge_word = ""
        self.challenge_input = ""
        self.challenge_timer = 0
        self.challenge_time_limit = 5
        
        self.api_url = "https://random-word-api.herokuapp.com/word?number=1&lang=fr"
        
        self.french_words = [
            "bonjour", "merci", "voiture", "maison", "chat", "chien", "livre",
            "bibliothèque", "restaurant", "université", "appartement", "ordinateur",
            "développement", "anticonstitutionnellement", "parallélépipède", "chrysanthème",
            "psychologique", "extraordinaire", "métaphysique", "philosophique",
            "encyclopédie", "rhinocéros", "hippopotame", "xylophone", "zoologique",
            "archéologie", "astronomie", "chlorophylle", "démocratie", "économique",
            "géographie", "hémisphère", "intelligence", "journalisme", "kilogramme",
            "laboratoire", "magnétique", "neurologie", "orthographe", "pneumonie",
            "quintessence", "révolution", "synchroniser", "technologie", "ultraviolet"
        ]


        self.sounds = load_sounds()
        self.music_enabled = True
        self.music_volume = 0.5
        self.music_initialized = False
        self.initialize_music()

        self.animations = {
            "gun_recoil": False,
            "gun_angle": 0,
            "player_falling": False,
            "fade_alpha": 0,
            "shake_amount": 0
        }

        self.create_ui_components()
        
        arena_x = 280
        arena_width = 570
        arena_center_x = arena_x + arena_width // 2
        
        arena_y = 120
        arena_height = 250
        arena_center_y = arena_y + arena_height // 2
        
        player_spacing = 200
        
        self.player1 = Player(
            arena_center_x - player_spacing//2,
            arena_center_y,
            "joueur1.png", 
            BLUE
        )
        
        self.player2 = Player(
            arena_center_x + player_spacing//2,
            arena_center_y,
            "joueur2.png", 
            RED
        )

        self.gun_rect = pygame.Rect(arena_center_x-25, arena_center_y-60, 50, 50)
        self.gun_original_pos = (arena_center_x, arena_center_y-60)
        self.gun_pos = list(self.gun_original_pos)
    
    def initialize_music(self):
        music_file = self.music_files[self.current_music_index]
        
        if os.path.exists(music_file):
            try:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)
                self.music_initialized = True
                if hasattr(self, 'event_log'):
                    self.event_log.add_message(f"Playing: {music_file}")
            except Exception as e:
                print(f"Error loading music: {e}")
                self.music_initialized = False
        else:
            print(f"Music file not found: {music_file}")
            self.music_initialized = False
    
    def toggle_music(self):
        self.music_enabled = not self.music_enabled
        
        if self.music_enabled:
            if hasattr(self, 'music_initialized') and self.music_initialized:
                pygame.mixer.music.unpause()
            else:
                self.initialize_music()
            self.event_log.add_message("Music enabled")
        else:
            pygame.mixer.music.pause()
            self.event_log.add_message("Music disabled")
            
    def next_music(self):
        self.current_music_index = (self.current_music_index + 1) % len(self.music_files)
        self.initialize_music()
        self.event_log.add_message(f"Next music: {self.music_files[self.current_music_index]}")
            
    def increase_volume(self):
        self.music_volume = min(1.0, self.music_volume + 0.1)
        pygame.mixer.music.set_volume(self.music_volume)
        volume_percent = int(self.music_volume * 100)
        self.event_log.add_message(f"Music volume: {volume_percent}%")

    def decrease_volume(self):
        self.music_volume = max(0.0, self.music_volume - 0.1)
        pygame.mixer.music.set_volume(self.music_volume)
        volume_percent = int(self.music_volume * 100)
        self.event_log.add_message(f"Music volume: {volume_percent}%")
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds and self.music_enabled:
            self.sounds[sound_name].play()
    
    def create_ui_components(self):
        button_width = 180
        button_height = 40
        button_margin = 10
        button_x = 50
        
        y_start = 200
        y_spacing = button_height + button_margin
        
        self.start_button = Button(button_x, y_start, button_width, button_height, GREEN, "COMMENCER")
        self.tirer_button = Button(button_x, y_start + y_spacing, button_width, button_height, BLUE, "TIRER")
        self.rejouer_button = Button(button_x, y_start + y_spacing*2, button_width, button_height, PURPLE, "REJOUER")
        # Supprimer les boutons "CLASSEMENT" et "OPTIONS"
        # self.classement_button = Button(button_x, y_start + y_spacing*3, button_width, button_height, ORANGE, "CLASSEMENT")
        # self.options_button = Button(button_x, y_start + y_spacing*4, button_width, button_height, GRAY, "OPTIONS")
        self.music_button = Button(button_x, y_start + y_spacing*3, button_width, button_height, LIGHT_BLUE, "MUSIQUE ON/OFF")
        
        self.tirer_button.set_active(False)
        self.rejouer_button.set_active(False)
        
        self.nb_balles_textbox = TextBox(130, 150, 50, 30, max_chars=3)
        self.nb_balles_textbox.text = "1"
        
        self.event_log = EventLog(250, 400, 600, 350)
        self.event_log.add_message("Bienvenue dans le jeu de la Roulette Russe !")
        self.event_log.add_message("Entrez le nombre de balles et cliquez sur COMMENCER.")
    
        self.player1_nickname_input = TextBox(350, 200, 200, 40, font_size=20, max_chars=15)
        self.player2_nickname_input = TextBox(350, 270, 200, 40, font_size=20, max_chars=15)
    
        self.continue_button = Button(0, 0, 200, 40, GREEN, "CONTINUER")
    
    def start_game(self):
        try:
            nb_balles = int(self.nb_balles_textbox.text)
            if nb_balles < 1:
                raise ValueError
        except ValueError:
            self.event_log.add_message("Erreur: Entrez un nombre supérieur à 0.")
            self.play_sound("empty")
            return
        
        self.entering_nicknames = True
        self.play_sound("click")
        self.event_log.add_message("Entrez vos pseudos pour commencer la partie.")
    
    def start_game_with_nicknames(self):
        nb_balles = int(self.nb_balles_textbox.text)
        
        self.player1_nickname = self.player1_nickname_input.text or "Joueur 1"
        self.player2_nickname = self.player2_nickname_input.text or "Joueur 2"
        
        self.play_sound("reload")
        
        if nb_balles <= 6:
            self.barillet = init_barillet(nb_balles)
        else:
            self.barillet = []
            while nb_balles > 0:
                if nb_balles >= 6:
                    self.barillet.extend(init_barillet(6))
                    nb_balles -= 6
                else:
                    self.barillet.extend(init_barillet(nb_balles))
                    nb_balles = 0
        
        self.joueur = 1
        self.game_started = True
        self.game_over = False
        self.scores_partie = {self.player1_nickname: 0, self.player2_nickname: 0}
        
        self.tirer_button.set_active(True)
        self.start_button.set_active(False)
        self.rejouer_button.set_active(False)
        
        self.event_log.add_message(f"Partie commencée avec {self.nb_balles_textbox.text} balle(s).")
        self.event_log.add_message(f"C'est au tour de {self.player1_nickname}.")
        
        self.player1.reset_position()
        self.player2.reset_position()
    
    def animate_gun_recoil(self):
        self.animations["gun_recoil"] = True
        self.animations["gun_angle"] = -15
        
        self.gun_pos = list(self.gun_original_pos)
        
        recoil_frames = 6
        recoil_amount = 15
        
        for i in range(recoil_frames):
            if i < recoil_frames // 2:
                self.gun_pos[0] -= recoil_amount / (recoil_frames // 2)
            else:
                self.gun_pos[0] += recoil_amount / (recoil_frames // 2)
            
            self.gun_rect.x = self.gun_pos[0] - 25
            self.gun_rect.y = self.gun_pos[1] - 25
            
            if self.animations["gun_angle"] < 0:
                self.animations["gun_angle"] += 3
            
            self.draw()
            pygame.time.delay(20)
        
        self.animations["gun_recoil"] = False
        self.animations["gun_angle"] = 0
        self.gun_pos = list(self.gun_original_pos)
        self.gun_rect.x = self.gun_pos[0] - 25
        self.gun_rect.y = self.gun_pos[1] - 25
    
    def animate_screen_shake(self):
        self.animations["shake_amount"] = 10
        
        for i in range(10):
            self.animations["shake_amount"] = max(0, self.animations["shake_amount"] - 1)
            self.draw()
            pygame.time.delay(30)
        
        self.animations["shake_amount"] = 0
    
    def shoot(self):
        self.play_sound("click")
        
        current_player = self.player1 if self.joueur == 1 else self.player2
        move_direction = 5 if self.joueur == 1 else -5
        
        for _ in range(10):
            current_player.x += move_direction
            self.draw()
            pygame.time.delay(20)
        for _ in range(10):
            current_player.x -= move_direction
            self.draw()
            pygame.time.delay(20)
        
        is_loaded_chamber = tirer(self.barillet)
        
        if is_loaded_chamber:
            self.start_word_challenge()
        else:
            self.play_sound("empty")
            current_nickname = self.player1_nickname if self.joueur == 1 else self.player2_nickname
            self.event_log.add_message(f"{current_nickname} : Clic... Rien ne se passe.")
            
            self.joueur = 2 if self.joueur == 1 else 1
            next_nickname = self.player1_nickname if self.joueur == 1 else self.player2_nickname
            self.event_log.add_message(f"C'est au tour de {next_nickname}.")
            
            if not self.barillet:
                self.event_log.add_message("Le barillet est vide ! Fin de la partie.")
                self.game_over = True
                self.tirer_button.set_active(False)
                self.rejouer_button.set_active(True)
                
    def eliminate_current_player(self):
        self.play_sound("gunshot")
        self.animate_gun_recoil()
        self.animate_screen_shake()
        
        current_nickname = self.player1_nickname if self.joueur == 1 else self.player2_nickname
        other_nickname = self.player2_nickname if self.joueur == 1 else self.player1_nickname
        
        self.scores_partie[other_nickname] += 1
        self.event_log.add_message(f"BOUM ! {current_nickname} est éliminé.")
        self.event_log.add_message(f"{other_nickname} gagne 1 point.")
        
        player = self.player1 if self.joueur == 1 else self.player2
        
        for i in range(30):
            player.y += 8
            player.angle += 12
            self.animations["fade_alpha"] = min(180, self.animations["fade_alpha"] + 6)
            self.draw()
            pygame.time.delay(20)
            
        self.play_sound("win")
            
        self.game_over = True
        self.tirer_button.set_active(False)
        self.rejouer_button.set_active(True)
        
        for nickname, score in self.scores_partie.items():
            if nickname in self.scores:
                self.scores[nickname] += score
            else:
                self.scores[nickname] = score
        
        self.data["parties"].append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "scores": self.scores_partie.copy()
        })
        self.data["scores"] = self.scores
        sauvegarder_scores(self.data)
        
        self.event_log.add_message("Partie terminée ! Cliquez sur REJOUER pour une nouvelle partie.")
        
        
    def get_random_word(self):
        try:
            response = requests.get(self.api_url)
            if response.status_code == 200:
                word = response.json()[0]
                return word
            else:
                print(f"Error fetching word: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception fetching word: {e}")
            return None
    
    def start_word_challenge(self):
        self.word_challenge_active = True
        self.challenge_word = self.get_random_word() or random.choice(self.french_words)
        self.challenge_input = ""
        self.challenge_timer = pygame.time.get_ticks()
        self.challenge_time_limit = 5
        self.play_sound("event")
        current_nickname = self.player1_nickname if self.joueur == 1 else self.player2_nickname
        self.event_log.add_message(f"{current_nickname}: Écrivez '{self.challenge_word}' pour survivre!")
        
    def handle_word_challenge(self):
        if not self.word_challenge_active:
            return
            
        elapsed = (pygame.time.get_ticks() - self.challenge_timer) / 1000
        time_left = self.challenge_time_limit - elapsed
        
        if time_left <= 0:
            self.word_challenge_active = False
            self.challenge_input = ""
            current_nickname = self.player1_nickname if self.joueur == 1 else self.player2_nickname
            self.event_log.add_message(f"Temps écoulé! {current_nickname} n'a pas écrit '{self.challenge_word}' assez rapidement.")
            self.eliminate_current_player()
    
    def restart(self):
        self.game_started = False
        self.game_over = False
        self.entering_nicknames = False
        self.scores_partie = {}
        self.player1_nickname = ""
        self.player2_nickname = ""
        
        self.player1_nickname_input.text = ""
        self.player2_nickname_input.text = ""
        
        self.start_button.set_active(True)
        self.tirer_button.set_active(False)
        self.rejouer_button.set_active(False)
        
        self.animations["fade_alpha"] = 0
        self.animations["shake_amount"] = 0
        
        self.event_log.add_message("Nouvelle partie ! Entrez le nombre de balles et cliquez sur COMMENCER.")
        
        self.player1.reset_position()
        self.player2.reset_position()
    
    def show_classement(self):
        self.play_sound("click")
        classement = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        messages = ["CLASSEMENT :"]
        
        for joueur, score in classement:
            messages.append(f"{joueur}: {score} points")
        
        self.event_log.add_message(messages)
    
    def show_options(self):
        self.play_sound("click")
        self.event_log.add_message("Options du jeu")

    def draw(self):
        shake_offset_x = random.randint(-self.animations["shake_amount"], self.animations["shake_amount"])
        shake_offset_y = random.randint(-self.animations["shake_amount"], self.animations["shake_amount"])
    
        SCREEN.fill(DARK_BLUE)
    
        title_font = pygame.font.SysFont("Impact", 36)
        shadow_surf = title_font.render("ROULETTE RUSSE", True, (0, 0, 0))
        title_surf = title_font.render("ROULETTE RUSSE", True, RED)
    
        SCREEN.blit(shadow_surf, (SCREEN_WIDTH // 2 - shadow_surf.get_width() // 2 + 2, 32))
        SCREEN.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 30))
    
        # Dessiner les éléments standard uniquement si nous ne sommes PAS en train d'entrer des pseudos
        if not self.entering_nicknames:
            if self.game_started and not self.game_over:
                subtitle_font = pygame.font.SysFont("Arial", 24)
                current_nickname = self.player1_nickname if self.joueur == 1 else self.player2_nickname
                subtitle_text = f"Tour de {current_nickname}"
                subtitle_surf = subtitle_font.render(subtitle_text, True, WHITE)
                SCREEN.blit(subtitle_surf, (SCREEN_WIDTH // 2 - subtitle_surf.get_width() // 2, 80))
    
            # Panneau de contrôles
            pygame.draw.rect(SCREEN, LIGHT_BLUE, pygame.Rect(30, 100, 220, 400), border_radius=10)
            controls_label = pygame.font.SysFont("Arial", 18, bold=True).render("CONTRÔLES", True, WHITE)
            SCREEN.blit(controls_label, (130 - controls_label.get_width() // 2, 110))
    
            label_font = pygame.font.SysFont("Arial", 16)
            nb_balles_label = label_font.render("Nombre de balles (1+):", True, WHITE)
            SCREEN.blit(nb_balles_label, (50, 120))
    
            # Afficher la textbox du nombre de balles
            self.nb_balles_textbox.draw(SCREEN)
    
            # Dessiner tous les boutons
            self.start_button.draw(SCREEN)
            self.tirer_button.draw(SCREEN)
            self.rejouer_button.draw(SCREEN)
            self.music_button.draw(SCREEN)
    
            # Zone de jeu
            pygame.draw.rect(SCREEN, LIGHT_BLUE, pygame.Rect(280, 120, 570, 250), border_radius=10)
            pygame.draw.rect(SCREEN, WHITE, pygame.Rect(280, 120, 570, 250), 1, border_radius=10)
            pygame.draw.ellipse(SCREEN, (40, 55, 70), pygame.Rect(350, 210, 430, 120))
            pygame.draw.ellipse(SCREEN, (35, 50, 65), pygame.Rect(350, 210, 430, 120), 2)
    
            # Joueurs et arme
            self.player1.draw(SCREEN)
            self.player2.draw(SCREEN)
    
            # Inverser l'image du pistolet horizontalement en fonction du joueur actif
            if self.joueur == 1:
                gun_image = self.gun_image
            else:
                gun_image = pygame.transform.flip(self.gun_image, True, False)
    
            # Dessiner l'image du pistolet
            if self.animations["gun_angle"] != 0:
                rotated_gun = pygame.transform.rotate(gun_image, self.animations["gun_angle"])
                rotated_rect = rotated_gun.get_rect(center=self.gun_rect.center)
                SCREEN.blit(rotated_gun, rotated_rect)
            else:
                SCREEN.blit(gun_image, self.gun_rect)
    
            # Indicateur de joueur actif
            if self.game_started and not self.game_over:
                indicator_pos = (self.player1.x, self.player1.y - 80) if self.joueur == 1 else (
                self.player2.x, self.player2.y - 80)
    
                pulse = (pygame.time.get_ticks() % 1000) / 1000
                pulse_size = 8 + int(4 * pulse)
    
                pygame.draw.circle(SCREEN, RED, indicator_pos, pulse_size)
                pygame.draw.circle(SCREEN, WHITE, indicator_pos, pulse_size, 1)
    
            # Scores
            score_font = pygame.font.SysFont("Arial", 16, bold=True)
            score_title = score_font.render("SCORES", True, ORANGE)
            SCREEN.blit(score_title, (130 - score_title.get_width() // 2, 505))
    
            if self.game_started:
                score1_color = BLUE if self.joueur == 1 and not self.game_over else WHITE
                score2_color = RED if self.joueur == 2 and not self.game_over else WHITE
    
                label_font = pygame.font.SysFont("Arial", 16)
                score1 = label_font.render(
                    f"{self.player1_nickname}: {self.scores_partie.get(self.player1_nickname, 0)}", True, score1_color)
                score2 = label_font.render(
                    f"{self.player2_nickname}: {self.scores_partie.get(self.player2_nickname, 0)}", True, score2_color)
    
                SCREEN.blit(score1, (130 - score1.get_width() // 2, 530))
                SCREEN.blit(score2, (130 - score2.get_width() // 2, 555))
    
            # Aide
            help_font = pygame.font.SysFont("Arial", 12)
            help_text = help_font.render("Flèches ↑/↓: Volume | 0: Musique | →: Musique suivante", True, WHITE)
            SCREEN.blit(help_text, (130 - help_text.get_width() // 2, 580))
    
            # Game over
            if self.game_over:
                go_font = pygame.font.SysFont("Impact", 40)
                winner_nickname = self.player2_nickname if self.joueur == 1 else self.player1_nickname
                go_text = "GAME OVER" if not self.barillet else f"{winner_nickname} GAGNE!"
    
                go_shadow = go_font.render(go_text, True, (0, 0, 0))
                go_surface = go_font.render(go_text, True, ORANGE)
    
                go_x = 280 + 570 // 2 - go_surface.get_width() // 2
                go_y = 120 + 250 // 2 - go_surface.get_height() // 2
    
                SCREEN.blit(go_shadow, (go_x + 2, go_y + 2))
                SCREEN.blit(go_surface, (go_x, go_y))
    
        # Afficher le panneau de saisie des pseudos (par-dessus tout le reste)
        if self.entering_nicknames:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            SCREEN.blit(overlay, (0, 0))
    
            input_box = pygame.Rect(280, 150, 570, 300)
            pygame.draw.rect(SCREEN, DARK_BLUE, input_box, border_radius=10)
            pygame.draw.rect(SCREEN, LIGHT_BLUE, input_box, 2, border_radius=10)
    
            font = pygame.font.SysFont("Arial", 28, bold=True)
            title = font.render("ENTREZ VOS PSEUDOS", True, WHITE)
            SCREEN.blit(title, (input_box.centerx - title.get_width() // 2, 170))
    
            font = pygame.font.SysFont("Arial", 20)
            player1_label = font.render("Joueur 1:", True, BLUE)
            player2_label = font.render("Joueur 2:", True, RED)
    
            # Dessiner les noms des joueurs à gauche des zones de texte
            SCREEN.blit(player1_label, (input_box.x + 10, 210))
            SCREEN.blit(player2_label, (input_box.x + 10, 280))
    
            self.player1_nickname_input.draw(SCREEN)
            self.player2_nickname_input.draw(SCREEN)
    
            # Mettez à jour la position du bouton continue
            self.continue_button.rect.x = input_box.centerx - 100
            self.continue_button.rect.y = input_box.bottom - 100 
            self.continue_button.draw(SCREEN)
    
        # Défi de mot (toujours par-dessus tout)
        if self.word_challenge_active:
            elapsed = (pygame.time.get_ticks() - self.challenge_timer) / 1000
            time_left = max(0, self.challenge_time_limit - elapsed)
    
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            SCREEN.blit(overlay, (0, 0))
    
            challenge_box = pygame.Rect(280, 150, 570, 200)
            pygame.draw.rect(SCREEN, DARK_BLUE, challenge_box, border_radius=10)
            pygame.draw.rect(SCREEN, LIGHT_BLUE, challenge_box, 2, border_radius=10)
    
            font = pygame.font.SysFont("Arial", 22, bold=True)
            current_nickname = self.player1_nickname if self.joueur == 1 else self.player2_nickname
            instructions = font.render(f"{current_nickname}, TAPEZ CE MOT POUR SURVIVRE:", True, WHITE)
            SCREEN.blit(instructions, (challenge_box.centerx - instructions.get_width() // 2, 170))
    
            word_font = pygame.font.SysFont("Arial", 36, bold=True)
            word_surf = word_font.render(self.challenge_word, True, ORANGE)
            SCREEN.blit(word_surf, (challenge_box.centerx - word_surf.get_width() // 2, 210))
    
            input_font = pygame.font.SysFont("Arial", 28)
            input_surf = input_font.render(self.challenge_input, True, GREEN)
            SCREEN.blit(input_surf, (challenge_box.centerx - input_surf.get_width() // 2, 270))
    
            timer_text = f"Temps restant: {time_left:.1f}s"
            timer_font = pygame.font.SysFont("Arial", 20)
            timer_color = RED if time_left < 2 else WHITE
            timer_surf = timer_font.render(timer_text, True, timer_color)
            SCREEN.blit(timer_surf, (challenge_box.centerx - timer_surf.get_width() // 2, 310))
    
        # Journal d'événements (toujours visible)
        self.event_log.draw(SCREEN)
    
        # Effet de fondu
        if self.animations["fade_alpha"] > 0:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self.animations["fade_alpha"]))
            SCREEN.blit(overlay, (0, 0))
    
        pygame.display.flip()
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Gestion prioritaire des saisies spéciales
        if self.entering_nicknames:
            self.player1_nickname_input.handle_event(event)
            self.player2_nickname_input.handle_event(event)
            self.continue_button.handle_event(event)
    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.continue_button.is_hovered(pos):
                    self.play_sound("click")
                    self.entering_nicknames = False
                    self.start_game_with_nicknames()
            return
        
        # Traitement prioritaire du défi de mot
        if self.word_challenge_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.challenge_input = self.challenge_input[:-1]
            elif event.key == pygame.K_RETURN:
                pass
            elif event.unicode.isalpha() or event.unicode == ' ' or event.unicode == '-':
                self.challenge_input += event.unicode
                if self.challenge_input.lower() == self.challenge_word.lower():
                    self.word_challenge_active = False
                    self.challenge_input = ""
                    self.play_sound("win")
                    current_nickname = self.player1_nickname if self.joueur == 1 else self.player2_nickname
                    self.event_log.add_message(f" Défi réussi! {current_nickname} survit au tir!")
                    
                    self.joueur = 2 if self.joueur == 1 else 1
                    next_nickname = self.player1_nickname if self.joueur == 1 else self.player2_nickname
                    self.event_log.add_message(f"C'est au tour de {next_nickname}.")
            
            # Mise à jour immédiate de l'affichage
            self.draw()
            pygame.display.flip()
            return  # Sortir pour ne pas traiter d'autres événements
        
        # Gestion standard des événements
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                
                if self.start_button.is_hovered(pos) and self.start_button.active:
                    self.play_sound("click")
                    self.start_game()
                elif self.tirer_button.is_hovered(pos) and self.tirer_button.active:
                    self.shoot()
                elif self.rejouer_button.is_hovered(pos) and self.rejouer_button.active:
                    self.play_sound("click")
                    self.restart()
                elif self.music_button.is_hovered(pos):
                    self.toggle_music()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.increase_volume()
            elif event.key == pygame.K_DOWN:
                self.decrease_volume()
            elif event.key == pygame.K_0:
                self.toggle_music()
            elif event.key == pygame.K_RIGHT:  # Add key to switch to the next music
                self.next_music()
        
        # Traitement normal des composants d'interface
        self.start_button.handle_event(event)
        self.tirer_button.handle_event(event)
        self.rejouer_button.handle_event(event)
        self.music_button.handle_event(event)
        self.nb_balles_textbox.handle_event(event)
        
        # L'event_log est traité en dernier pour ne pas interférer
        self.event_log.handle_event(event)

    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                self.handle_event(event)
            
            if self.word_challenge_active:
                self.handle_word_challenge()
            
            self.draw()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    try:
        game.run()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if pygame.mixer.get_init():  # Vérifiez si le mixer est initialisé
            pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()