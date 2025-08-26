from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout

from viewmodel.user_viewmodel import UserViewModel

# Если ты хранишь KV-правила для EditProfileContent в отдельном .kv - не нужно,
# но если нет, можно явно load_string / load_file. Предположим, что правило <EditProfileContent>
# находится в app.kv(таким образом KV создаст шаблон).
# Builder.load_string(...) можно вызвать здесь, если тебе удобно.

class EditProfileContent(MDBoxLayout):
    """пустой класс-контейнер - его разметка определена в KV (ids: name_field, email_field, ...)"""
    pass


class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Не создаём ViewModel в __init__ - делаем это в on_kv_post, чтобы DB уже была инициализирована.
        self.vm: UserViewModel = None
        self.dialog = None

    def on_kv_post(self, base_widget):
        """Вызывается после того, как KV привязан к классу - безопасно создавать ViewModel."""
        # Инициализируем ViewModel (она может обращаться к репозиторию)
        if self.vm is None:
            self.vm = self.get_app().user_vm
        self._refresh_ui()

    def on_pre_enter(self):
        # каждый раз перед показом экрана обновляе ui
        if self.vm:
            self._refresh_ui()

    def _refresh_ui(self):
        """Обновляет все тексты и аватар"""
        app = self.get_app()
        user_data = self.vm.get_user_dict()

        # Имя или перевод 'Гость'
        name = user_data.get("name") or app.translate("guest")
        self.ids.username_label.text = name

        # Кнопки
        self.ids.edit_profile_btn.text = app.translate("edit_profile")
        self.ids.logout_btn.text = app.translate("logout")

        # Аватар
        avatar_widget = self.ids.get("avatar_img")
        if avatar_widget:
            avatar_widget.source = user_data.get("avatar_path") or "assets/avatars/default.png"

    def open_edit_profile_dialog(self):
        """Открывает MDDialog с контентом, определенный в KV (<EditProfileContent>)"""
        data = self.vm.get_user_dict()
        app = self.get_app()

        # Создаём экземпляр контента, который описан в KV
        content = EditProfileContent()

        # Заполняем поля значениями
        content.ids.name_field.hint_text = app.translate("name")
        content.ids.email_field.hint_text = app.translate("email")
        content.ids.phone_field.hint_text = app.translate("phone")
        content.ids.dark_mode_label.text = app.translate("dark_theme")
        content.ids.lang_label.text = app.translate("language")

        content.ids.name_field.text = data.get("name") or ""
        content.ids.email_field.text = data.get("email") or ""
        content.ids.phone_field.text = data.get("phone") or ""
        content.ids.theme_switch.active = (data.get("theme") == "dark")
        content.ids.lang_switch.active = (data.get("language") != "ru")

        # Создаём диалог
        self.dialog = MDDialog(
            title=app.translate("edit_profile"),
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text=app.translate("cancel"),
                    on_release=self._cancel_edit
                ),
                MDRaisedButton(
                    text=app.translate("save"),
                    on_release=lambda btn: self._save_profile(content)
                ),
            ],
        )

        self.dialog.open()
    
    def _cancel_edit(self, instance):
        if self.dialog:
            self.dialog.dismiss()

    def _save_profile(self, content):
        """Сохраняет изменеия из content (EditProfileContent)."""
        name = (content.ids.name_field.text or "").strip() or "Гость"
        email = (content.ids.email_field.text or "").strip() or None
        phone = (content.ids.phone_field.text or "").strip() or None
        theme = "dark" if content.ids.theme_switch.active else "light"
        language = "en" if content.ids.lang_switch.active else "ru"

        # update через ViewModel
        self.vm.update_user(name=name, email=email, phone=phone, theme=theme, language=language)
        # переключаем язык в приложении
        self.get_app().switch_language(language)
        # переключаю тему в приложении
        self.get_app().switch_theme(theme)
        # обновляем UI
        self._refresh_ui()

        # закрываем диалог
        if self.dialog:
            self.dialog.dismiss()

    def user_logout(self):
        """Сброс локального пользователя на дефолтного (Guest)."""
        if self.vm:
            self.vm.reset_user()
        self._refresh_ui()
        self.get_app().switch_language(self.vm.language)

    def get_app(self):
        from kivymd.app import MDApp
        return MDApp.get_running_app()