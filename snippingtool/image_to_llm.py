import webbrowser
import time
from PIL import Image
from typing import Optional
import pyperclipimg
from pynput.keyboard import Key, Controller as KeyboardController

def open_chatgpt_and_drop_image(image: Image.Image) -> bool:
    """
    Opens ChatGPT in browser and pastes the given image using clipboard.
    
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
        webbrowser.open("https://chat.openai.com")
        time.sleep(1)  # Wait for page to load
        
        # Paste image
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
