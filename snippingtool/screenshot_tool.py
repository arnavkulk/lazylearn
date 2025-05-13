import os
import pyautogui
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime
from pathlib import Path
from pynput import keyboard
import threading
import sys

class ScreenshotTool:
    def __init__(self):
        print("Initializing ScreenshotTool...")
        # Initialize screenshot variables
        self.selection_window = None
        self.preview_window = None
        self.start_x = None
        self.start_y = None
        self.current_rect = None

        # Initialize hotkey state
        self.cmd_pressed = False
        self.shift_pressed = False
        self.g_pressed = False

        # Create root window (hidden)
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        
        # Start keyboard listener
        print("Starting keyboard listener...")
        self.keyboard_thread = threading.Thread(target=self.start_keyboard_listener, daemon=True)
        self.keyboard_thread.start()
        print("Initialization complete!")

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
                
                # Check for hotkey combination
                if self.cmd_pressed and self.shift_pressed and self.g_pressed:
                    print("Hotkey combination detected!")
                    # Schedule the selection window creation in the main thread
                    self.root.after(0, self.start_selection)
            except AttributeError:
                pass

        def on_release(key):
            try:
                if key == keyboard.Key.cmd:
                    self.cmd_pressed = False
                    print("Cmd released")
                elif key == keyboard.Key.shift:
                    self.shift_pressed = False
                    print("Shift released")
                elif hasattr(key, 'char') and key.char == 'g':
                    self.g_pressed = False
                    print("G released")
            except AttributeError:
                pass

        # Start the keyboard listener
        print("Setting up keyboard listener...")
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
        print("Keyboard listener started successfully")

    def start_selection(self):
        print("Starting selection process...")
        try:
            # Create a fullscreen transparent window using Toplevel
            self.selection_window = tk.Toplevel(self.root)
            print("Created selection window")
            
            self.selection_window.attributes('-fullscreen', True, '-alpha', 0.3)
            self.selection_window.configure(bg='grey')
            
            # Create canvas for drawing
            self.canvas = tk.Canvas(
                self.selection_window,
                highlightthickness=0,
                bg='grey'
            )
            self.canvas.pack(fill='both', expand=True)
            print("Canvas created and packed")

            # Bind mouse events
            self.canvas.bind('<Button-1>', self.on_mouse_down)
            self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
            self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
            self.selection_window.bind('<Escape>', lambda e: self.cancel_selection())
            print("Mouse events bound")

            # Make window stay on top
            self.selection_window.attributes('-topmost', True)
            
            # Get screen dimensions
            screen_width = self.selection_window.winfo_screenwidth()
            screen_height = self.selection_window.winfo_screenheight()
            
            # Set window size to screen size
            self.selection_window.geometry(f"{screen_width}x{screen_height}+0+0")
            print(f"Selection window configured with dimensions: {screen_width}x{screen_height}")
            
            # Make the window modal
            self.selection_window.grab_set()
            self.selection_window.focus_set()
            print("Selection window ready")
            
        except Exception as e:
            print(f"Error in start_selection: {str(e)}")
            import traceback
            traceback.print_exc()
            if self.selection_window:
                self.selection_window.destroy()
                self.selection_window = None

    def on_mouse_down(self, event):
        print(f"Mouse down at coordinates: ({event.x}, {event.y})")
        self.start_x = event.x
        self.start_y = event.y
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2
        )

    def on_mouse_drag(self, event):
        if self.current_rect:
            self.canvas.coords(
                self.current_rect,
                self.start_x, self.start_y, event.x, event.y
            )

    def on_mouse_up(self, event):
        print(f"Mouse up at coordinates: ({event.x}, {event.y})")
        if self.current_rect:
            # Get the coordinates of the selection
            coords = self.canvas.coords(self.current_rect)
            x1, y1, x2, y2 = map(int, coords)
            print(f"Selection coordinates: ({x1}, {y1}) to ({x2}, {y2})")
            
            # Ensure coordinates are in the correct order
            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x2 - x1)
            height = abs(y2 - y1)

            print(f"Taking screenshot of region: ({left}, {top}, {width}, {height})")
            # Take screenshot of the selected area
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            
            # Close selection window
            self.selection_window.destroy()
            self.selection_window = None
            
            # Save screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshots/screenshot_{timestamp}.png"
            os.makedirs("screenshots", exist_ok=True)
            screenshot.save(filename)
            print(f"Screenshot saved to: {filename}")
            
            # Show preview window
            self.show_preview(screenshot, filename)

    def show_preview(self, image, filename):
        print("Creating preview window...")
        # Create preview window
        self.preview_window = tk.Tk()
        self.preview_window.title("Screenshot Preview")
        self.preview_window.geometry("800x600")
        
        # Create main frame
        main_frame = ttk.Frame(self.preview_window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create image preview
        preview_frame = ttk.Frame(main_frame)
        preview_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Create label for image preview
        image_label = ttk.Label(preview_frame)
        image_label.pack(expand=True, fill=tk.BOTH)
        
        # Configure grid weights
        self.preview_window.columnconfigure(0, weight=1)
        self.preview_window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        print("Updating image preview...")
        # Update image preview
        self.update_image_preview(image, image_label)
        
        # Add close button
        close_btn = ttk.Button(
            main_frame,
            text="Close",
            command=self.preview_window.destroy
        )
        close_btn.grid(row=1, column=0, pady=10)
        print("Preview window setup complete")

    def update_image_preview(self, image, label):
        print("Resizing image for preview...")
        # Get the size of the preview area
        preview_width = 780  # Fixed width for preview
        preview_height = 500  # Fixed height for preview
        
        # Calculate scaling factor to fit the image in the preview area
        width_ratio = preview_width / image.width
        height_ratio = preview_height / image.height
        scale_factor = min(width_ratio, height_ratio)
        
        # Calculate new dimensions
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        
        print(f"Resizing image to: {new_width}x{new_height}")
        # Resize image
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(resized_image)
        
        # Update label
        label.configure(image=photo)
        label.image = photo  # Keep a reference!
        print("Image preview updated")

    def cancel_selection(self):
        print("Cancelling selection...")
        if self.selection_window:
            self.selection_window.destroy()
            self.selection_window = None
            print("Selection cancelled")

def main():
    print("Starting main application...")
    app = ScreenshotTool()
    try:
        print("Entering main loop...")
        # Keep the main thread running
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    main() 