import time
from kivy.app import App
from kivy.uix.image import Image
import threading
from backup import *

class MainApp(App):
    class MyThread(threading.Thread):
        def __init__(self, transcriber):
            super().__init__()
            self.transcriber = transcriber
            self.stop_flag = threading.Event()

        def run(self):
            while not self.stop_flag.is_set():
                print("Thread is running...")
                self.transcriber.transcribe_audio()  # Corrected this line
            print("Thread stopped.")

        def stop(self):
            self.stop_flag.set()

    def build(self):
        self.img = Image(source='/home/user/Documents/EEE/kivy/assets/mic_plain.png',
                         size_hint=(1, .5),
                         pos_hint={'center_x': .5, 'center_y': .5})

        self.img.bind(on_touch_down=self.on_image_tap)  # Bind the event handler

        return self.img

    def on_image_tap(self, instance, touch):
        if instance.collide_point(*touch.pos):  # Check if the touch point is within the image bounds
            # Change the image source or any other properties
            if not hasattr(self, 'audio_thread') or not self.audio_thread.is_alive():
                self.img.source = '/home/user/Documents/EEE/kivy/assets/mic_active.png'
                self.audio_thread = self.MyThread(transcriber)
                self.audio_thread.start()  # Use start() instead of run()
            else:
                self.img.source = '/home/user/Documents/EEE/kivy/assets/mic_grey.png'
                self.audio_thread.stop()
                self.audio_thread.join()
                print("disconnected")

if __name__ == '__main__':
    app = MainApp()
    app.run()
