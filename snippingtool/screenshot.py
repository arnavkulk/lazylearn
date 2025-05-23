import tkinter as tk
from PIL import ImageGrab

class ScreenshotTool:
    def __init__(self, on_screenshot_complete):
        self.root = tk.Tk()
        # self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.15)  # semi-transparent
        # self.root.configure(background='black')
        self.root.attributes("-topmost", True)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.canvas = tk.Canvas(self.root, cursor="cross", bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.root.bind('<Escape>', self.quit)

        self.on_screenshot_complete = on_screenshot_complete
        
    def start(self):
        self.root.mainloop()
    
    def quit(self, event):
        print("quit")
        self.root.withdraw()  # hide window before capturing
        self.root.destroy()

    def on_mouse_down(self, event):
        print("on_mouse_down")
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y,
                                                 self.start_x, self.start_y,
                                                 outline='gray', width=2)
        print(self.start_x, self.start_y)
        
    def on_mouse_drag(self, event):
        print("on_mouse_drag")
        cur_x, cur_y = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)
        print(cur_x, cur_y)
        
    def on_mouse_up(self, event):
        print("on_mouse_up")
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        x1 = int(min(self.start_x, end_x))
        y1 = int(min(self.start_y, end_y))
        x2 = int(max(self.start_x, end_x))
        y2 = int(max(self.start_y, end_y))
        print(x1, y1, x2, y2)
        self.root.withdraw()  # hide window before capturing
        self.root.update()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.root.destroy()
        if img.size != (0, 0):
            self.on_screenshot_complete(img)