import pyautogui
import time
from PIL import Image
import platform
import os
import tempfile
import subprocess
from typing import Tuple, Optional

def save_image_to_temp(image: Image.Image) -> str:
    """
    Saves a PIL Image to a temporary file and returns the path.
    
    Args:
        image (PIL.Image): The image to save
        
    Returns:
        str: Path to the temporary file
    """
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_path = temp_file.name
        image.save(temp_path, 'PNG')
    return temp_path

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
    time.sleep(3)  # Wait for window to load

def get_screen_center() -> Tuple[int, int]:
    """
    Calculates the center coordinates of the screen.
    
    Returns:
        Tuple[int, int]: (x, y) coordinates of screen center
    """
    screen_width, screen_height = pyautogui.size()
    return (screen_width // 2, screen_height // 2)

def find_and_select_file_macos(file_path: str) -> None:
    """
    Uses Spotlight to find and select a file on macOS.
    
    Args:
        file_path (str): Path to the file to find
    """
    pyautogui.hotkey('command', 'space')
    time.sleep(1)
    pyautogui.write(file_path)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)

def find_and_select_file_windows(file_path: str) -> None:
    """
    Opens file location and selects file on Windows/Linux.
    
    Args:
        file_path (str): Path to the file to find
    """
    os.startfile(os.path.dirname(file_path))
    time.sleep(2)
    pyautogui.click()
    time.sleep(0.5)

def drag_to_center(center_x: int, center_y: int) -> None:
    """
    Performs drag and drop operation to the specified center coordinates.
    
    Args:
        center_x (int): X coordinate of center
        center_y (int): Y coordinate of center
    """
    pyautogui.mouseDown()
    time.sleep(0.5)
    pyautogui.moveTo(center_x, center_y, duration=0.5)
    pyautogui.mouseUp()

def cleanup_temp_file(file_path: str) -> None:
    """
    Safely removes a temporary file.
    
    Args:
        file_path (str): Path to the file to remove
    """
    try:
        os.unlink(file_path)
    except Exception as e:
        print(f"Warning: Could not remove temporary file: {str(e)}")

def open_chatgpt_and_drop_image(image: Image.Image) -> bool:
    """
    Opens ChatGPT in a new Chrome window and drags/drops the given image to the center.
    
    Args:
        image (PIL.Image): The image to be dragged and dropped
        
    Returns:
        bool: True if operation was successful, False otherwise
    """
    temp_path: Optional[str] = None
    
    try:
        # Save image to temp file
        temp_path = save_image_to_temp(image)
        
        # Open browser and get screen center
        open_browser("https://chat.openai.com")
        center_x, center_y = get_screen_center()
        
        # Find and select file based on OS
        if platform.system() == "Darwin":
            find_and_select_file_macos(temp_path)
        else:
            find_and_select_file_windows(temp_path)
        
        # Perform drag and drop
        drag_to_center(center_x, center_y)
        
        return True
        
    except Exception as e:
        print(f"Error during drag and drop operation: {str(e)}")
        return False
        
    finally:
        # Clean up temp file if it was created
        if temp_path:
            cleanup_temp_file(temp_path)

if __name__ == "__main__":
    # Example usage
    test_image = Image.new('RGB', (100, 100), color='red')
    open_chatgpt_and_drop_image(test_image)