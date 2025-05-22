import rumps
from threading import Thread
from keyboard_listener import GlobalHotkeyListener
from image_to_llm import open_chatgpt_and_drop_image

class RumpsAddOn(rumps.App):
    def __init__(self, deps = []):
        super(RumpsAddOn, self).__init__("LazyLearn", "🎯", quit_button=None)
        self.menu = ["Quit"]
        self.deps = deps

    @rumps.clicked("Quit")
    def quit_app(self, _):
        for dep in self.deps:
            dep.stop()
        rumps.quit_application()

class LazyLearnApp:
    def __init__(self):
        self.keyboard_listener = GlobalHotkeyListener(self.handle_screenshot)
        self.keyboard_thread = Thread(target=self.keyboard_listener.run, daemon=True)
        self.menu_app = RumpsAddOn(deps=[self.keyboard_listener])
        # self.menu_app_thread = Thread(target=self.menu_app.run, daemon=True)
    
    def run(self):
        self.keyboard_thread.start()
        self.menu_app.run()
        # RumpsAddOn(deps=[self.keyboard_listener]).run()

    def handle_screenshot(self, img):
        """
        Handle the screenshot by opening ChatGPT and pasting the image.
        
        Args:
            img (PIL.Image): The screenshot image to process
        """
        Thread(target=open_chatgpt_and_drop_image, args=[img]).start()
        # success = open_chatgpt_and_drop_image(img)
        # if not success:
        #     print("Failed to process screenshot with ChatGPT")


if __name__ == "__main__":
    app = LazyLearnApp()
    app.run() 