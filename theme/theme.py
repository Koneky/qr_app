from kivy.utils import get_color_from_hex
from kivy.logger import Logger

try:
    # Старые версии kivymd
    from kivymd.theming import ThemeManager
except Exception:
    ThemeManager = None


class QRumiXTheme:
    """
    Безопасно применяет тему QRumiX к app.theme_cls, не удаляя обязательные ключи,
    которые ожидает KivyMD (например, 'Light', 'Dark')
    """
    
    def __init__(self):
        # фрменные цвета (hex строки)
        self.brand_primary = "#4CAF50"
        self.brand_accent = "#FFEB3B"
        self.background_dark = "#121212"
        self.text_primary = "#FFFFFF"
        self.text_secondary = "#B0B3C5"

        # дополнительные настройки по умолчанию
        self.theme_style = "Dark"
        self.primary_palette = "Green"
        self.primary_hue = "500"
        self.accent_palette = "Yellow"

        # Опциональная расширенная карта цветов, на случай, если нужно
        # задать AppBrand / Background / CardsDialogs и т.д.
        self._qr_colors_dark = {
            "StatusBar": "#0D0D0D",
            "AppBar": self.background_dark,
            "Background": self.background_dark,
            "CardsDialog": "#1E1E1E",
            "FlatButtonDown": "#2E7D32",
        }
        self._qr_colors_light = {
            "StatusBar": "#FFFFFF",
            "AppBar": "#F5F5F5",
            "Background": "#FFFFFF",
            "CardsDialog": "#FFFFFF",
            "FlatButtonDown": "#E0E0E0",
        }

    def _ensure_theme_cls(self, app):
        # Получаю theme_cls; если нет - создаём (максимально безопасно)
        theme = getattr(app, "theme_cls", None)

        if theme is None:
            
            if ThemeManager:
                theme = ThemeManager()
                app.theme_cls = theme
            else:
                # В KivyMD 2.x ThemeManager может располагаться по-другому,
                # но обычно app.theme_cls уже создан MDApp'ом. Делаем лог
                Logger.warning("QRumiXTheme: app.theme_cls отсутствует и ThemeManager недоступен.")
                return None
        return theme
    
    def apply(self, app):
        theme = self._ensure_theme_cls(app)

        if theme is None:
            return
        
        # базовые свойства (буду присвоивать, не заменять полностью)
        try:
            theme.theme_style = self.theme_style
        except Exception:
            # в 2.x это всегда доступон, но на всякий случай логируем
            Logger.info("QRumiXTheme: не удалось установить theme_style напрямую")

        # попытка установить палитры (совместимо с 1.x)
        try:
            theme.primary_palette = self.primary_palette
            theme.primary_hue = self.primary_hue
            theme.accent_palette = self.accent_palette
        except Exception:
            Logger.info("QRumiXTheme: не удалось установить палитры (возможно другая версия KivyMD)")

        # безопасное слияние colors
        existing = getattr(theme, 'colors', None)

        if not isinstance(existing, dict):
            # если colors отсутствует или имеет другой тип - создаём минимальую структуру
            existing = {}

        # убедимся, что ключи Light и Dark присутствуют и имеют минимальные подключи
        if "Light" not in existing:
            existing["Light"] = {
                "StatusBar": self._qr_colors_light["StatusBar"],
                "AppBar": self._qr_colors_light["AppBar"],
                "Background": self._qr_colors_light["Background"],
                "CardsDialogs": self._qr_colors_light["CardsDialogs"],
                "FlatButtonDown": self._qr_colors_light["FlatButtonDown"],
            }
        else:
            # merge - не затираем существующие значения
            for k, v in self._qr_colors_light.items():
                existing["Light"].setdefault(k, v)

        if "Dark" not in existing:
            existing["Dark"] = {
                "StatusBar": self._qr_colors_dark["StatusBar"],
                "AppBar": self._qr_colors_dark["AppBar"],
                "Background": self._qr_colors_dark["Background"],
                "CardsDialogs": self._qr_colors_dark["CardsDialogs"],
                "FlatButtonDown": self._qr_colors_dark["FlatButtonDown"],
            }
        else:
            for k, v in self._qr_colors_dark.items():
                existing["Dark"].setdefault(k, v)

        # добавляем брендовые цвета в отдельный namespace, чтобы не ломать структуру
        existing.setdefault("QRumiX", {})
        existing["QRumiX"].update({
            "Primary": self.brand_primary,
            "Accent": self.brand_accent,
            "Background": self.background_dark,
            "Text": self.text_primary,
            "TextSecondary": self.text_secondary,
        })

        # присваиваем обрабно theme.colors
        try:
            theme.colors = existing
        except Exception:
            # иногда в 2.x объект theme.colors может быть read-only или иной структуры
            Logger.info("QRumiXTheme: не удалось напрямую присвоить theme.colors, попробуем обновить по ключам")
            # Попробуем обновлять по отдельным атрибутам, если они есть
            for key in ("bg_dark", "bg_light"):
                if hasattr(theme, key):
                    # пример theme.bg_dark = get_color_from_hex(self.background_dark)
                    try:
                        setattr(theme, key, get_color_from_hex(self.background_dark))
                    except Exception:
                        pass

        # наконец, можно установить пару удобных shortcut-атрибутов
        try:
            # в коде часто обращаются к theme_cls.primary_color
            theme.primary_color = get_color_from_hex(self.brand_primary)
            theme.accent_color = get_color_from_hex(self.brand_accent)
        except Exception:
            pass

        Logger.info("QRumiXTheme: тема успешно применена")

    def set_style(self, style):
        """Устанавливает стиль темы ('Light' или 'Dark') и применяет изменения."""
        style = style.capitalize()
        if style not in ("Light", "Dark"):
            Logger.warning(f"QRumiXTheme: неизвестный стиль '{style}', оставляю {self.theme_style}")
            return
        self.theme_style = style