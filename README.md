# LazyLearn

A macOS tool that makes it easy to capture screenshots and send them directly to ChatGPT for analysis. Available in both Python and AppleScript versions.

## Features

### AppleScript Version
- 📸 Native macOS screenshot tool integration
- 🤖 Direct ChatGPT browser integration
- ⚡ Lightweight and fast
- 🔄 Automatic clipboard handling

### Python Version
- 🎯 Menu bar app with a clean interface
- ⌨️ Global hotkey support (Cmd+Shift+G)
- 📸 Interactive screenshot selection
- 🤖 Direct integration with ChatGPT
- 🖱️ Smart clipboard handling
- 🚀 Fast and reliable

## Installation

### AppleScript Version
1. Open Script Editor on your Mac
2. Open `apple_script/screenshot_to_chatgpt.applescript`
3. Save as an Application
4. (Optional) Add to your Applications folder
5. (Optional) Set up a keyboard shortcut in System Settings > Keyboard > Shortcuts

### Python Version
1. Clone the repository:
   ```bash
   git clone https://github.com/arnavkulk/lazylearn.git
   cd lazylearn
   ```

2. Install uv (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Create and activate a virtual environment:
   ```bash
   cd snippingtool
   uv venv
   source .venv/bin/activate  # On macOS/Linux
   ```

4. Install dependencies:
   ```bash
   uv pip install -r pyproject.toml
   ```

5. Run the app:
   ```bash
   uv run keyboard_listener.py
   ```

## Usage

### AppleScript Version
1. Run the saved application
2. Select the area to capture
3. The screenshot will be automatically sent to ChatGPT

### Python Version
1. Click the 🎯 icon in the menu bar
2. Use Cmd+Shift+G to trigger screenshot
3. Select the area you want to capture
4. The screenshot will be automatically sent to ChatGPT

## Requirements

### AppleScript Version
- macOS
- Chrome browser

### Python Version
- macOS
- Python 3.8+
- Chrome browser
- Required Python packages (see requirements.txt)

## Development

The project uses:
- `rumps` for the menu bar app
- `pynput` for keyboard monitoring
- `pyperclipimg` for clipboard handling
- `PIL` for image processing

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- ChatGPT for the AI integration
- The rumps library for the menu bar functionality
- The macOS screenshot tool for the capture functionality 