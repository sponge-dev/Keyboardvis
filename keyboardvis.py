import pygame
from pynput import keyboard
import json
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_settings():
    config_path = resource_path('config.json')
    default_settings = {
        'keyboard_layout': 'QWERTY',               # Default layout
        'background_color': [30, 30, 30],          # Dark Gray
        'keypress_color': [0, 120, 215],           # Blue
        'keypress_opacity': 180,                   # Semi-transparent
        'font_size': 30                            # Larger font size for key labels
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                settings = json.load(f)
            # (Validation code remains unchanged)
            # ...
            return settings
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading config.json: {e}")
            print("Loading default settings.")
    
    # Save default settings if config.json doesn't exist or is invalid
    save_settings(default_settings)
    return default_settings

# Path to the configuration file
CONFIG_FILE = 'config.json'

# Initialize Pygame
pygame.init()

# Define multiple keyboard layouts
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

# Define shifted mappings for each layout
shifted_mappings = {
    "QWERTY": {
        '`': '~',
        '1': '!',
        '2': '@',
        '3': '#',
        '4': '$',
        '5': '%',
        '6': '^',
        '7': '&',
        '8': '*',
        '9': '(',
        '0': ')',
        '-': '_',
        '=': '+',
        '[': '{',
        ']': '}',
        '\\': '|',
        ';': ':',
        "'": '"',
        ',': '<',
        '.': '>',
        '/': '?'
    },
    "AZERTY": {
        '²': '',
        '&': '1',
        'é': '2',
        '"': '3',
        "'": '4',
        '(': '5',
        '-': '6',
        'è': '7',
        '_': '8',
        'ç': '9',
        'à': '0',
        ')': '°',
        '=': '+',
        '^': '¨',
        '$': '£',
        '\\': 'µ',
        'ù': '%',
        ';': '.',
        ':': '/',
        ',': '?',
        '!': '1'
    },
    "Dvorak": {
        '`': '~',
        '1': '!',
        '2': '@',
        '3': '#',
        '4': '$',
        '5': '%',
        '6': '^',
        '7': '&',
        '8': '*',
        '9': '(',
        '0': ')',
        '[': '{',
        ']': '}',
        '\\': '|',
        ';': ':',
        "'": '"',
        ',': '<',
        '.': '>',
        '/': '?'
    }
}

# Function to load settings from config.json
def load_settings():
    default_settings = {
        'keyboard_layout': 'QWERTY',               # Default layout
        'background_color': [30, 30, 30],          # Dark Gray
        'keypress_color': [0, 120, 215],           # Blue
        'keypress_opacity': 180,                   # Semi-transparent
        'font_size': 30                            # Larger font size for key labels
    }
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                settings = json.load(f)
            # Validate required keys
            required_keys = ['keyboard_layout', 'background_color', 'keypress_color', 'keypress_opacity', 'font_size']
            if not all(k in settings for k in required_keys):
                raise ValueError("Missing keys in config.json.")
            # Validate keyboard_layout
            if settings['keyboard_layout'] not in keyboard_layouts:
                raise ValueError("Unsupported keyboard_layout in config.json.")
            # Ensure color values are lists of three integers
            for color_key in ['background_color', 'keypress_color']:
                if (not isinstance(settings[color_key], list) or
                    len(settings[color_key]) != 3 or
                    not all(isinstance(c, int) and 0 <= c <= 255 for c in settings[color_key])):
                    raise ValueError(f"Invalid color format for {color_key} in config.json.")
            # Ensure opacity is an integer within range
            if (not isinstance(settings['keypress_opacity'], int) or
                not 0 <= settings['keypress_opacity'] <= 255):
                raise ValueError("Invalid opacity value in config.json.")
            # Ensure font_size is an integer within a reasonable range
            if (not isinstance(settings['font_size'], int) or
                not 20 <= settings['font_size'] <= 100):
                raise ValueError("Invalid font_size in config.json. It should be an integer between 20 and 100.")
            return settings
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading config.json: {e}")
            print("Loading default settings.")
    
    # Save default settings if config.json doesn't exist or is invalid
    save_settings(default_settings)
    return default_settings

# Function to save settings to config.json
def save_settings(settings):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

# Load settings
settings = load_settings()

# Set up display
WIDTH, HEIGHT = 1400, 800  # Adjust as needed
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Real-Time Keystroke Visualizer")

# Select the keyboard layout based on settings
selected_layout = keyboard_layouts[settings['keyboard_layout']]
current_shifted_mapping = shifted_mappings[settings['keyboard_layout']]

# Define key rectangles
key_rects = {}
key_width = 60    # Consider increasing if needed
key_height = 60   # Consider increasing if needed
padding = 5
start_x = 50
start_y = 50

def create_key_rects():
    for row_index, row in enumerate(selected_layout):
        x = start_x
        y = start_y + row_index * (key_height + padding)
        for key in row:
            width = key_width
            # Adjust width for special keys
            if key in ['Backspace', 'Enter', 'Shift', 'Caps Lock', 'Tab', 'Ctrl', 'Alt', 'Win', 'Menu', 'Space', 'Alt Gr']:
                if key == 'Space':
                    width = key_width * 5
                elif key == 'Alt Gr':
                    width = int(key_width * 1.75)
                else:
                    width = int(key_width * 1.75)
            rect = pygame.Rect(x, y, width, key_height)
            # To handle duplicate keys like 'Shift', 'Ctrl', etc., append row and x position for uniqueness
            unique_key = f"{key.upper()}_{row_index}_{x}"
            key_rects[unique_key] = (rect, key.upper())
            x += width + padding

create_key_rects()

# Create a set of allowed keys for quick lookup
allowed_keys = set()
for _, (_, actual_key) in key_rects.items():
    allowed_keys.add(actual_key)

# Store currently pressed keys
pressed_keys = set()

# Store active modifier keys
active_modifiers = set()

# Define modifier keys
modifier_keys = {'SHIFT', 'CTRL', 'ALT', 'WIN', 'MENU', 'ALT GR'}

# Mapping pynput keys to our layout keys
def map_pynput_key(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            # Return the character in uppercase (e.g., '1', 'A', etc.)
            return key.char.upper()
    except AttributeError:
        pass
    # Handle special keys
    special_keys = {
        keyboard.Key.backspace: 'BACKSPACE',
        keyboard.Key.tab: 'TAB',
        keyboard.Key.caps_lock: 'CAPS LOCK',
        keyboard.Key.enter: 'ENTER',
        keyboard.Key.shift: 'SHIFT',
        keyboard.Key.shift_r: 'SHIFT',    # Treat right shift as 'SHIFT'
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

# Function to listen to keyboard events
def on_press(key):
    key_mapped = map_pynput_key(key)
    if not key_mapped:
        return
    if key_mapped in modifier_keys:
        active_modifiers.add(key_mapped)
        pressed_keys.add(key_mapped)
    else:
        if 'SHIFT' in active_modifiers and key_mapped != 'SHIFT':
            # When Shift is held, show both Shift and the key
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

# Start the keyboard listener in a separate thread
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Initialize font with larger size and bold style
font_size = settings['font_size']  # Loaded from config.json
font = pygame.font.SysFont(None, font_size, bold=True)

# Function to calculate brightness for text color (Not used anymore)
def calculate_brightness(color):
    return (color[0]*299 + color[1]*587 + color[2]*114) / 1000

# Function to render text with optional transparency
def render_text(text, color, alpha=255):
    text_surface = font.render(text, True, color)
    if alpha < 255:
        text_surface.set_alpha(alpha)
    return text_surface

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background with the selected color
    win.fill(settings['background_color'])

    # Draw keys
    for unique_key, (rect, actual_key) in key_rects.items():
        if actual_key in pressed_keys:
            # Apply opacity to keypress color
            keypress_color_with_opacity = (*settings['keypress_color'], settings['keypress_opacity'])
            # Create a semi-transparent surface for the pressed key
            pressed_key_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pressed_key_surface.fill(keypress_color_with_opacity)
            # Blit the semi-transparent surface onto the main window
            win.blit(pressed_key_surface, (rect.x, rect.y))
            # Draw thicker white border for pressed keys
            pygame.draw.rect(win, (255, 255, 255), rect, 4, border_radius=5)  # White border with rounded corners
        else:
            # Draw the key as a solid rectangle with a slight shadow
            pygame.draw.rect(win, (50, 50, 50), rect, border_radius=5)
            # Draw thinner dark gray border for unpressed keys
            pygame.draw.rect(win, (30, 30, 30), rect, 2, border_radius=5)

        # Determine what to display on the key
        display_key = actual_key
        if actual_key == 'BACKSPACE':
            display_key = 'Bksp'
        elif actual_key == 'SPACE':
            display_key = 'Space'
        elif actual_key == 'CAPS LOCK':
            display_key = 'Cpslck'
        elif actual_key in ['CTRL', 'WIN', 'ALT', 'MENU', 'SHIFT', 'ALT GR']:
            # Keep the key name as is for other modifiers
            display_key = actual_key

        # If Shift is held and the key has a shifted symbol, display the symbol
        if actual_key in pressed_keys and 'SHIFT' in active_modifiers:
            if actual_key in current_shifted_mapping and current_shifted_mapping[actual_key]:
                display_key = current_shifted_mapping[actual_key]

        # Determine text color based on key state
        if actual_key in pressed_keys:
            # Text color for pressed keys (white for visibility)
            text_color = (255, 255, 255)
        else:
            # Text color for unpressed keys (light gray)
            text_color = (200, 200, 200)

        # Render the text with full opacity
        text = render_text(display_key, text_color, alpha=255)
        text_rect = text.get_rect(center=rect.center)
        win.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

# Clean up
listener.stop()
pygame.quit()
