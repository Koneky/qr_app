import os
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from theme.theme import QRumiXTheme
from data.database import init_db, create_tables
from data.translations import translations
from viewmodel.user_viewmodel import UserViewModel

# Виджеты
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.card import MDCard
from kivy.uix.image import AsyncImage
from ui.widgets.custom_switch import CustomSwitch

# Экраны
from ui.screens.generate_screen import GenerateScreen
from ui.screens.home_screen import HomeScreen
from ui.screens.profile_screen import ProfileScreen
from ui.screens.scan_screen import ScanScreen


class QRumiXApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_lang = None
        self.user_vm: UserViewModel = None
        self.theme = QRumiXTheme()

    def build(self):
        self.theme.apply(self) # Применяем кастомную тему

        # Инициализация БД
        db_path = os.path.join(self.user_data_dir, "qr_app.db")
        init_db(db_path)
        create_tables()

        # Инициализация ViewModel
        self.user_vm = UserViewModel()

        # Язык из бд
        self.current_lang = self.user_vm.language

        # Загрузка KV
        return Builder.load_file('app.kv')
    
    def on_start(self):
        """Вызов после полной загрузки интерфейса"""
        user_data = self.user_vm.get_user_dict()
        theme = user_data.get("theme", "light")
        self.switch_theme(theme)
        self.update_ui()

    def translate(self, key):
        return translations.get(self.current_lang, {}).get(key, key)
    
    def switch_language(self, lang):
        self.current_lang = lang
        if self.user_vm:
            self.user_vm.language = lang
            # Сохраняем в базе
            self.user_vm.update_user(language=lang)
        self.update_ui()

    def switch_theme(self, theme: str):
        """theme: 'light' или 'dark'"""
        style = "Dark" if theme == "dark" else "Light"
        self.theme.set_style(style)
        self.theme.apply(self)

        # Горячее обновление всех виджетов после применения темы
        if self.root:
            # ставимна следующую итерацию цикла Kivy, чтобы все виджеты были готовы
            Clock.schedule_once(lambda dt: self._reload_theme(self.root))

    def _reload_theme(self, widget):
        """Рекурсивно обновляет все виджеты, которые используют theme_cls"""
        if hasattr(widget, 'on_theme_style'):
            try:
                widget.on_theme_style(widget.theme_cls)
            except Exception:
                pass # некотрые виджеты могут не поддерживать on_theme_cls

        # рекурсия по дочерним виджетам
        for child in getattr(widget, 'children', []):
            self._reload_theme(child)

    def update_ui(self):
        if not self.root:
            return
        
        def find_widget_by_id(widget, id_name):
            if hasattr(widget, 'ids') and id_name in widget.ids:
                return widget.ids[id_name]
            for child in widget.children:
                result = find_widget_by_id(child, id_name)
                if result:
                    return result
            return None
        
        def safe_set(id_name, attr, value):
            widget = find_widget_by_id(self.root, id_name)
            if widget:
                setattr(widget, attr, value)
        
        # Применяем переводы
        safe_set('top_appbar', 'title', self.translate("app_title"))
        safe_set('welcome_label', 'text', self.translate("welcome"))
        safe_set('home_tab', 'text', self.translate("home"))
        safe_set('scan_tab', 'text', self.translate("scan"))
        safe_set('generate_tab', 'text', self.translate("generate"))
        safe_set('history_tab', 'text', self.translate("history"))
        safe_set('profile_tab', 'text', self.translate("profile"))
        safe_set('history_soon_label', 'text', self.translate("history_soon"))
        safe_set('name_field', 'hint_text', self.translate("name"))
        safe_set('fullname_field', 'hint_text', self.translate("fullname"))
        safe_set('email_field', 'hint_text', self.translate("email"))
        safe_set('phone_field', 'hint_text', self.translate("phone"))
        safe_set('bio_field', 'hint_text', self.translate("bio"))
        safe_set('dark_mode_label', 'text', self.translate("dark_theme"))
        safe_set('lang_label', 'text', self.translate("language"))




if __name__ == "__main__":
    QRumiXApp().run()