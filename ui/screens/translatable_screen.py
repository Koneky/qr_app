from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class TranslatableScreen(MDScreen):
    def get_app(self):
        return MDApp.get_running_app()
    
    def update_translations(self):
        """Переопределяется в наследниках"""
        pass

    def on_pre_enter(self, *args):
        self.update_translations()
        return super().on_pre_enter(*args)