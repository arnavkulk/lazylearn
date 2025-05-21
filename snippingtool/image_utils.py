import time
from PIL import Image
import platform
import subprocess
from typing import Optional
import pyperclipimg
from pynput.keyboard import Key, Controller as KeyboardController

def get_chrome_path() -> str:
    """
    Returns the appropriate Chrome executable path for the current OS.
    
    Returns:
        str: Path to Chrome executable
    """
    if platform.system() == "Darwin":  # macOS
        return '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    elif platform.system() == "Windows":
        return 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    else:  # Linux and other systems
        return 'google-chrome'

def open_browser(url: str) -> None:
    """
    Opens the specified URL in a new Chrome window.
    
    Args:
        url (str): The URL to open
    """
    chrome_path = get_chrome_path()
    subprocess.Popen([chrome_path, '--new-window', url])

def open_chatgpt_and_drop_image(image: Image.Image) -> bool:
    """
    Opens ChatGPT in a new Chrome window and pastes the given image using clipboard.
    
    Args:
        image (PIL.Image): The image to be pasted
        
    Returns:
        bool: True if operation was successful, False otherwise
    """
    keyboard = KeyboardController()
    
    try:
        # Save image to clipboard
        pyperclipimg.copy(image)
        
        # Open browser
        open_browser("https://chat.openai.com")
        time.sleep(1)  # Wait for page to load
        
        # Paste image directly using pyperclip
        keyboard.press(Key.cmd)
        keyboard.press('v')
        keyboard.release('v')
        keyboard.release(Key.cmd)
        time.sleep(1)  # Wait for paste to complete
        
        # Press enter to send
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        
        return True
        
    except Exception as e:
        print(f"Error during paste operation: {str(e)}")
        return False

if __name__ == "__main__":
    # Example usage
    test_image = Image.new('RGB', (100, 100), color='red')
    open_chatgpt_and_drop_image(test_image)