import pygame
from pynput import keyboard
import json
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_settings():
    config_path = resource_path('config.json')
    default_settings = {
        'keyboard_layout': 'QWERTY',
        'background_color': [30, 30, 30],
        'keypress_color': [0, 120, 215],
        'keypress_opacity': 180,
        'font_size': 30
    }

    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                settings = json.load(f)
            required_keys = ['keyboard_layout', 'background_color', 'keypress_color', 'keypress_opacity', 'font_size']
            if not all(k in settings for k in required_keys):
                raise ValueError("Missing keys in config.json.")
            for color_key in ['background_color', 'keypress_color']:
                if (not isinstance(settings[color_key], list) or
                    len(settings[color_key]) != 3 or
                    not all(isinstance(c, int) and 0 <= c <= 255 for c in settings[color_key])):
                    raise ValueError(f"Invalid color format for {color_key}.")
            if (not isinstance(settings['keypress_opacity'], int) or
                not 0 <= settings['keypress_opacity'] <= 255):
                raise ValueError("Invalid opacity value.")
            if (not isinstance(settings['font_size'], int) or
                not 20 <= settings['font_size'] <= 100):
                raise ValueError("Font size should be between 20 and 100.")
            return settings
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading config.json: {e}")
            print("Loading default settings.")

    save_settings(default_settings)
    return default_settings

def save_settings(settings):
    with open('config.json', 'w') as f:
        json.dump(settings, f, indent=4)

# init and load settings
pygame.init()
settings = load_settings()

# Define keyboard layouts
keyboard_layouts = {
    "QWERTY": [
        ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
        ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
        ['Caps Lock', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", 'Enter'],
        ['Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift'],
        ['Ctrl', 'Win', 'Alt', 'Space', 'Alt', 'Win', 'Menu', 'Ctrl']
    ],
    "AZERTY": [
        ['²', '&', 'é', '"', "'", '(', '-', 'è', '_', 'ç', 'à', ')', '=', 'Backspace'],
        ['Tab', 'A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '^', '$', '\\'],
        ['Caps Lock', 'Q', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'ù', 'Enter'],
        ['Shift', 'W', 'X', 'C', 'V', 'B', 'N', ',', ';', ':', '!', 'Shift'],
        ['Ctrl', 'Win', 'Alt', 'Space', 'Alt Gr', 'Win', 'Menu', 'Ctrl']
    ],
    "Dvorak": [
        ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '[', ']', 'Bksp'],
        ['Tab', "'", ',', '.', 'P', 'Y', 'F', 'G', 'C', 'R', 'L', '/', '=', '\\'],
        ['Caps Lock', 'A', 'O', 'E', 'U', 'I', 'D', 'H', 'T', 'N', 'S', '-', 'Enter'],
        ['Shift', ';', 'Q', 'J', 'K', 'X', 'B', 'M', 'W', 'V', 'Z', 'Shift'],
        ['Ctrl', 'Win', 'Alt', 'Space', 'Alt', 'Win', 'Menu', 'Ctrl']
    ]
}

# Shifted character mappings for each layout
shifted_mappings = {
    "QWERTY": {
        '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
        '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '-': '_',
        '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', "'": '"',
        ',': '<', '.': '>', '/': '?'
    },
    "AZERTY": {
        '²': '', '&': '1', 'é': '2', '"': '3', "'": '4', '(': '5',
        '-': '6', 'è': '7', '_': '8', 'ç': '9', 'à': '0', ')': '°',
        '=': '+', '^': '¨', '$': '£', '\\': 'µ', 'ù': '%',
        ';': '.', ':': '/', ',': '?', '!': '1'
    },
    "Dvorak": {
        '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
        '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '[': '{',
        ']': '}', '\\': '|', ';': ':', "'": '"', ',': '<', '.': '>',
        '/': '?'
    }
}

# Set up display
WIDTH, HEIGHT = 1400, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Real-Time Keystroke Visualizer")

selected_layout = keyboard_layouts[settings['keyboard_layout']]
current_shifted_mapping = shifted_mappings[settings['keyboard_layout']]

# Define key dimensions and positions
key_rects = {}
key_width = 60
key_height = 60
padding = 5
start_x = 50
start_y = 50

def create_key_rects():
    for row_index, row in enumerate(selected_layout):
        x = start_x
        y = start_y + row_index * (key_height + padding)
        for key in row:
            width = key_width
            if key in ['Backspace', 'Enter', 'Shift', 'Caps Lock', 'Tab', 'Ctrl', 'Alt', 'Win', 'Menu', 'Space', 'Alt Gr']:
                if key == 'Space':
                    width = key_width * 5
                elif key == 'Alt Gr':
                    width = int(key_width * 1.75)
                else:
                    width = int(key_width * 1.75)
            rect = pygame.Rect(x, y, width, key_height)
            unique_key = f"{key.upper()}_{row_index}_{x}"
            key_rects[unique_key] = (rect, key.upper())
            x += width + padding

create_key_rects()

allowed_keys = {actual_key for _, (_, actual_key) in key_rects.items()}

pressed_keys = set()
active_modifiers = set()
modifier_keys = {'SHIFT', 'CTRL', 'ALT', 'WIN', 'MENU', 'ALT GR'}

def map_pynput_key(key):
    try:
        if hasattr(key, 'char') and key.char:
            return key.char.upper()
    except AttributeError:
        pass
    special_keys = {
        keyboard.Key.backspace: 'BACKSPACE',
        keyboard.Key.tab: 'TAB',
        keyboard.Key.caps_lock: 'CAPS LOCK',
        keyboard.Key.enter: 'ENTER',
        keyboard.Key.shift: 'SHIFT',
        keyboard.Key.shift_r: 'SHIFT',
        keyboard.Key.ctrl: 'CTRL',
        keyboard.Key.ctrl_r: 'CTRL',
        keyboard.Key.alt: 'ALT',
        keyboard.Key.alt_r: 'ALT',
        keyboard.Key.alt_gr: 'ALT GR',
        keyboard.Key.space: 'SPACE',
        keyboard.Key.cmd: 'WIN',
        keyboard.Key.cmd_r: 'WIN',
        keyboard.Key.menu: 'MENU',
    }
    return special_keys.get(key, None)

def on_press(key):
    key_mapped = map_pynput_key(key)
    if not key_mapped:
        return
    if key_mapped in modifier_keys:
        active_modifiers.add(key_mapped)
        pressed_keys.add(key_mapped)
    else:
        if 'SHIFT' in active_modifiers and key_mapped != 'SHIFT':
            pressed_keys.add('SHIFT')
        if key_mapped in allowed_keys:
            pressed_keys.add(key_mapped)

def on_release(key):
    key_mapped = map_pynput_key(key)
    if not key_mapped:
        return
    if key_mapped in modifier_keys:
        active_modifiers.discard(key_mapped)
        pressed_keys.discard(key_mapped)
    else:
        if 'SHIFT' in active_modifiers and key_mapped != 'SHIFT':
            pressed_keys.discard('SHIFT')
        if key_mapped in allowed_keys:
            pressed_keys.discard(key_mapped)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

font_size = settings['font_size']
font = pygame.font.SysFont(None, font_size, bold=True)

def render_text(text, color, alpha=255):
    text_surface = font.render(text, True, color)
    if alpha < 255:
        text_surface.set_alpha(alpha)
    return text_surface

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    win.fill(settings['background_color'])

    for unique_key, (rect, actual_key) in key_rects.items():
        if actual_key in pressed_keys:
            overlay = (*settings['keypress_color'], settings['keypress_opacity'])
            pressed_key_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pressed_key_surface.fill(overlay)
            win.blit(pressed_key_surface, (rect.x, rect.y))
            pygame.draw.rect(win, (255, 255, 255), rect, 4, border_radius=5)
        else:
            pygame.draw.rect(win, (50, 50, 50), rect, border_radius=5)
            pygame.draw.rect(win, (30, 30, 30), rect, 2, border_radius=5)

        display_key = actual_key
        if actual_key == 'BACKSPACE':
            display_key = 'Bksp'
        elif actual_key == 'SPACE':
            display_key = 'Space'
        elif actual_key == 'CAPS LOCK':
            display_key = 'Cpslck'
        elif actual_key in ['CTRL', 'WIN', 'ALT', 'MENU', 'SHIFT', 'ALT GR']:
            display_key = actual_key

        if actual_key in pressed_keys and 'SHIFT' in active_modifiers:
            display_key = current_shifted_mapping.get(actual_key, display_key)

        text_color = (255, 255, 255) if actual_key in pressed_keys else (200, 200, 200)
        text = render_text(display_key, text_color)
        text_rect = text.get_rect(center=rect.center)
        win.blit(text, text_rect)

    pygame.display.flip()

listener.stop()
pygame.quit()
