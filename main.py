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
from ui.screens.editprofile_screen import EditProfileScreen
from ui.screens.scan_screen import ScanScreen
from ui.screens.history_screen import HistoryScreen
from ui.screens.settings_screen import SettingsScreen
from ui.screens.auth_screen import AuthScreen
from ui.screens.registration_screen import RegistrationScreen


KV_DIR = os.path.join(os.path.dirname(__file__), "ui", "kv")

class QRumiXApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_lang = None
        self.user_vm: UserViewModel = None
        self.theme = QRumiXTheme()

    def build(self):
        # Применяю тему и инициализирую БД/VM
        self.theme.apply(self)
        db_path = os.path.join(self.user_data_dir, "qr_app.db")
        init_db(db_path)
        create_tables()
        self.user_vm = UserViewModel()
        self.current_lang = self.user_vm.language

        # Загрузка всех kv из ui/kv (чтобы классы экранов были определены до app.kv)
        if os.path.isdir(KV_DIR):
            for fname in sorted(os.listdir(KV_DIR)):
                if fname.endswith(".kv"):
                    Builder.load_file(os.path.join(KV_DIR, fname))

        # Загрузка основного app.kv(корень приложения)
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
        
        def find_all_widgets_by_id(widget, id_name, result=None):
            """Ищет все виджеты с данным id рекурсивно"""
            if result is None:
                result = []
            # Проверка виджета
            if hasattr(widget, 'ids') and id_name in widget.ids:
                result.append(widget.ids[id_name])
            # Рекурсивно обхожу детей
            for child in getattr(widget, 'children', []):
                find_all_widgets_by_id(child, id_name, result)
            return result
        
        # Словарь соответствия id -> ключ перевода
        translations_map = {
            'top_appbar': ('title', "app_title"),
            'welcome_label': ('text', "welcome"),
            'home_tab': ('text', "home"),
            'scan_tab': ('text', "scan"),
            'generate_tab': ('text', "generate"),
            'history_tab': ('text', "history"),
            'profile_tab': ('text', "profile"),
            'history_soon_label': ('text', "history_soon"),
            'home_coming_soon': ('text', "coming_soon"),
            'scan_coming_soon': ('text', "coming_soon"),
            'generate_coming_soon': ('text', "coming_soon"),
            'history_coming_soon': ('text', "coming_soon"),
            'name_field': ('hint_text', "name"),
            'fullname_field': ('hint_text', "fullname"),
            'email_field': ('hint_text', "email"),
            'phone_field': ('hint_text', "phone"),
            'bio_field': ('hint_text', "bio"),
            'upload_avatar_btn': ('text', "upload_avatar_btn"),
            'dark_mode_label': ('text', "dark_theme"),
            'lang_label': ('text', "language"),
        }

        for id_name, (attr, key) in translations_map.items():
            widgets = find_all_widgets_by_id(self.root, id_name)
            for widget in widgets:
                setattr(widget, attr, self.translate(key))




if __name__ == "__main__":
    QRumiXApp().run()