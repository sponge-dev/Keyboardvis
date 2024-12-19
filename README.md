## Introduction

The **Real-Time Keystroke Visualizer** is a Python-based application that graphically displays your keyboard inputs in real-time. Whether you're streaming, presenting, or simply curious about your typing patterns, this visualizer provides an interactive and customizable interface to monitor key presses.

---

## Features

- **Multiple Keyboard Layouts**: Supports QWERTY, AZERTY, and Dvorak layouts.
- **Customizable Appearance**:
  - Change background and keypress colors.
  - Adjust keypress opacity and font sizes.
- **Interactive Feedback**: Keys visually respond when pressed, including shifted characters (e.g., `!` when pressing `Shift + 1`).
- **Configuration File**: Easily modify settings via `config.json`.
- **Executable Creation**: Package the application into a standalone executable for distribution.

## Installation

### Prerequisites

Before setting up the **Real-Time Keystroke Visualizer**, ensure you have the following installed on your system:

- **Python**: Version 3.6 or higher. [Download Python](https://www.python.org/downloads/)
- **Git**: For cloning the repository. [Download Git](https://git-scm.com/downloads)

### Clone the Repository

```bash
git clone https://github.com/yourusername/keyboard-visualizer.git
cd keyboard-visualizer
```

### Set Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

1. **Create a Virtual Environment**:

    ```bash
    python -m venv venv
    ```

2. **Activate the Virtual Environment**:

    - **Windows**:

        ```bash
        venv\Scripts\activate
        ```

    - **macOS/Linux**:

        ```bash
        source venv/bin/activate
        ```

### Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

> **Note**: If a `requirements.txt` file is not present, you can install the dependencies manually:

```bash
pip install pygame pynput appdirs
```

---

## Configuration

### `config.json`

The application uses a `config.json` file to store customizable settings. If the file does not exist or is invalid, default settings will be applied.

**Default Configuration**:

```json
{
    "keyboard_layout": "QWERTY",
    "background_color": [30, 30, 30],
    "keypress_color": [0, 120, 215],
    "keypress_opacity": 180,
    "font_size": 30
}
```

**Configuration Options**:

- **`keyboard_layout`**: Defines the keyboard layout. Supported options:
  - `"QWERTY"`
  - `"AZERTY"`
  - `"Dvorak"`

- **`background_color`**: RGB array for the background color. Example: `[30, 30, 30]` for dark gray.

- **`keypress_color`**: RGB array for the color overlay when a key is pressed. Example: `[0, 120, 215]` for blue.

- **`keypress_opacity`**: Integer value (0-255) defining the opacity of the keypress color. `180` provides a semi-transparent effect.

- **`font_size`**: Integer value defining the font size for key labels. Example: `30`.

> **Tip**: Modify `config.json` to customize the appearance and behavior of the visualizer. Ensure that color values are valid RGB arrays and that numerical values fall within appropriate ranges.

---

## Usage

### Running the Script

After setting up the environment and configuring settings:

1. **Activate the Virtual Environment** (if not already active):

    - **Windows**:

        ```bash
        venv\Scripts\activate
        ```

    - **macOS/Linux**:

        ```bash
        source venv/bin/activate
        ```

2. **Run the Application**:

    ```bash
    python main.py
    ```

> **Note**: Replace `main.py` with the actual name of your Python script if different.

### Creating an Executable

To distribute your application without requiring users to install Python and dependencies, you can create a standalone executable using **PyInstaller**.

#### Steps to Create an Executable:

1. **Ensure PyInstaller is Installed**:

    ```bash
    pip install pyinstaller
    ```

2. **Navigate to the Project Directory**:

    ```bash
    cd path/to/keyboard-visualizer
    ```

3. **Run PyInstaller with Appropriate Options**:

    - **Basic Command**:

        ```bash
        pyinstaller --onefile --windowed main.py
        ```

    - **With Custom Icon** (Optional):

        ```bash
        pyinstaller --onefile --windowed --icon=assets/icon.ico main.py
        ```

    - **Including `config.json`**:

        ```bash
        pyinstaller --onefile --windowed --icon=assets/icon.ico --add-data "config.json;." main.py
        ```

        > **Note**: 
        >
        > - Use a semicolon `;` as the separator on **Windows**.
        > - Use a colon `:` as the separator on **macOS/Linux**.
        >
        > Example for **macOS/Linux**:

        ```bash
        pyinstaller --onefile --windowed --icon=assets/icon.ico --add-data "config.json:." main.py
        ```

4. **Locate the Executable**:

    After the build process completes, find the executable in the `dist/` folder.

    - **Windows**: `dist/main.exe`
    - **macOS/Linux**: `dist/main`

5. **Run the Executable**:

    - **Windows**: Double-click `main.exe`.
    - **macOS/Linux**: Use the terminal to execute `./main`.

> **Important**: Ensure that `config.json` is accessible to the executable. The provided script handles path resolution using the `resource_path` function, which allows the executable to locate `config.json` whether running as a script or as a bundled application.

---

## Customization

### Changing Keyboard Layouts

To switch between different keyboard layouts:

1. **Open `config.json`**:

    ```json
    {
        "keyboard_layout": "QWERTY",
        ...
    }
    ```

2. **Modify the `keyboard_layout` Value**:

    - `"QWERTY"`
    - `"AZERTY"`
    - `"Dvorak"`

3. **Save the File** and **Restart the Application** to apply changes.

### Adjusting Colors and Opacity

Customize the visual appearance by modifying the following in `config.json`:

- **Background Color**:

    ```json
    "background_color": [30, 30, 30]
    ```

    - Replace with desired RGB values.

- **Keypress Color**:

    ```json
    "keypress_color": [0, 120, 215]
    ```

    - Replace with desired RGB values.

- **Keypress Opacity**:

    ```json
    "keypress_opacity": 180
    ```

    - Set between `0` (fully transparent) and `255` (fully opaque).

### Modifying Font Size

Change the size of the key labels:

```json
"font_size": 30
```

- Adjust the integer value to increase or decrease the font size.

---

## Contributing

Contributions are welcome! If you'd like to enhance the **Real-Time Keystroke Visualizer**, please follow these steps:

1. **Fork the Repository**

2. **Create a New Branch**

    ```bash
    git checkout -b feature/YourFeatureName
    ```

3. **Commit Your Changes**

    ```bash
    git commit -m "Add feature X"
    ```

4. **Push to the Branch**

    ```bash
    git push origin feature/YourFeatureName
    ```

5. **Open a Pull Request**

Please ensure that your contributions adhere to the project's coding standards and include appropriate documentation.

## Acknowledgements

- [Pygame](https://www.pygame.org/) – For providing a robust library for game development and graphical applications.
- [pynput](https://pynput.readthedocs.io/en/latest/) – For enabling keyboard event listening.
- [PyInstaller](https://www.pyinstaller.org/) – For simplifying the process of creating executables from Python scripts.
- [AppDirs](https://pypi.org/project/appdirs/) – For handling configuration file paths across different operating systems.

## Known Issues:

I know that shift + numberkeys do not currently show as a button press, I'm trying to fix this but havent for the first iteration.
