from pynput import keyboard
import threading
import queue
import time
from screenshot import ScreenshotTool
from image_utils import open_chatgpt_and_drop_image

class GlobalHotkeyListener:
    def __init__(self):
        # Initialize hotkey state
        self.cmd_pressed = False
        self.shift_pressed = False
        self.g_pressed = False
        
        # Create a queue for thread-safe communication
        self.event_queue = queue.Queue()
        
        # Start keyboard listener in a separate thread
        self.keyboard_thread = threading.Thread(target=self.start_keyboard_listener, daemon=True)
        self.keyboard_thread.start()
        self.is_screenshot_tool_running = False
        # Start the main application loop
        self.run()

    def start_keyboard_listener(self):
        def on_press(key):
            try:
                if key == keyboard.Key.cmd:
                    self.cmd_pressed = True
                    print("Cmd pressed")
                elif key == keyboard.Key.shift:
                    self.shift_pressed = True
                    print("Shift pressed")
                elif hasattr(key, 'char') and key.char == 'g':
                    self.g_pressed = True
                    print("G pressed")
                
                if self.cmd_pressed and self.shift_pressed and self.g_pressed and not self.is_screenshot_tool_running:
                    print("Hotkey combination detected!")
                    self.event_queue.put('start_screenshot')
                    self.is_screenshot_tool_running = True
            except AttributeError:
                pass

        def on_release(key):
            try:
                if key == keyboard.Key.cmd:
                    self.cmd_pressed = False
                    self.is_screenshot_tool_running = False
                    print("Cmd released")
                elif key == keyboard.Key.shift:
                    self.shift_pressed = False
                    self.is_screenshot_tool_running = False
                    print("Shift released")
                elif hasattr(key, 'char') and key.char == 'g':
                    self.g_pressed = False
                    self.is_screenshot_tool_running = False
                    print("G released")
            except AttributeError:
                pass

        # Start the keyboard listener
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    
    def handle_screenshot(self, img):
        """
        Handle the screenshot by opening ChatGPT and pasting the image.
        
        Args:
            img (PIL.Image): The screenshot image to process
        """
        success = open_chatgpt_and_drop_image(img)
        if not success:
            print("Failed to process screenshot with ChatGPT")

    def run(self):
        try:
            while True:
                try:
                    # Check for messages in the queue
                    event = self.event_queue.get_nowait()
                    if event == 'start_screenshot':
                        print("Starting screenshot tool...")
                        sst = ScreenshotTool(self.handle_screenshot)
                        sst.start()
                except queue.Empty:
                    pass
                time.sleep(0.1)  # Small delay to prevent high CPU usage
        except KeyboardInterrupt:
            print("\nExiting...")

if __name__ == "__main__":
    print("Starting global hotkey listener...")
    print("Press Cmd+Shift+G to start screenshot tool")
    GlobalHotkeyListener() 