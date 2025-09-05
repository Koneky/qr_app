import os
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.filemanager import MDFileManager

from viewmodel.user_viewmodel import UserViewModel

# Если ты хранишь KV-правила для EditProfileContent в отдельном .kv - не нужно,
# но если нет, можно явно load_string / load_file. Предположим, что правило <EditProfileContent>
# находится в app.kv(таким образом KV создаст шаблон).
# Builder.load_string(...) можно вызвать здесь, если тебе удобно.

class EditProfileContent(MDBoxLayout):
    pass


class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Не создаём ViewModel в __init__ - делаем это в on_kv_post, чтобы DB уже была инициализирована.
        self.vm: UserViewModel = None
        self.dialog = None
        self.file_manager = None

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
        """Обновляет все текста и аватар"""
        app = self.get_app()
        user_data = self.vm.get_user_dict()

        # Full name и username
        full_name = user_data.get("full_name") or ""
        username = user_data.get("name") or app.translate("guest")
        self.ids.fullname_label.text = full_name
        self.ids.username_label.text = f"({username})" if full_name else username

        # Bio
        self.ids.bio_label.text = user_data.get("bio", "") or ""

        # Премиум
        self.ids.premium_badge.opacity = 1 if user_data.get("is_premium") else 0

        # Статус с переводом
        scans_text = app.translate("scans")
        generates_text = app.translate("generates")
        self.ids.scans_label.text = f"{scans_text}: {user_data.get('scan_count', 0)}"
        self.ids.generates_label.text = f"{generates_text}: {user_data.get('generate_count', 0)}"

        # Кнопки
        self.ids.edit_profile_btn.text = app.translate("edit_profile")
        self.ids.logout_btn.text = app.translate("logout")

        # Аватар
        awatar_widget = self.ids.get("avatar_img")
        if awatar_widget:
            awatar_widget.source = user_data.get("avatar_path") or "assets/avatars/default.png"

    def open_edit_profile_dialog(self):
        """Открывает MDDialog с контентом, определенный в KV (<EditProfileContent>)"""
        data = self.vm.get_user_dict()
        app = self.get_app()

        # Создаём экземпляр контента, который описан в KV
        content = EditProfileContent()

        # Заполняем поля значениями
        content.ids.name_field.hint_text = app.translate("name")
        content.ids.fullname_field.hint_text = app.translate("fullname")
        content.ids.email_field.hint_text = app.translate("email")
        content.ids.phone_field.hint_text = app.translate("phone")
        content.ids.bio_field.hint_text = app.translate("bio")
        content.ids.upload_avatar_btn.text = app.translate("upload_avatar_btn")
        content.ids.dark_mode_label.text = app.translate("dark_theme")
        content.ids.lang_label.text = app.translate("language")

        content.ids.name_field.text = data.get("name") or ""
        content.ids.fullname_field.text = data.get("full_name") or ""
        content.ids.email_field.text = data.get("email") or ""
        content.ids.phone_field.text = data.get("phone") or ""
        content.ids.bio_field.text = data.get("bio") or ""
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
        full_name = (content.ids.fullname_field.text or "").strip() or None
        email = (content.ids.email_field.text or "").strip() or None
        phone = (content.ids.phone_field.text or "").strip() or None
        bio = (content.ids.bio_field.text or "").strip() or None
        theme = "dark" if content.ids.theme_switch.active else "light"
        language = "en" if content.ids.lang_switch.active else "ru"

        # update через ViewModel
        self.vm.update_user(name=name, full_name=full_name, email=email, phone=phone, bio=bio, theme=theme, language=language)
        # переключаем язык в приложении
        self.get_app().switch_language(language)
        # переключаю тему в приложении
        self.get_app().switch_theme(theme)
        # обновляем UI
        self._refresh_ui()

        # закрываем диалог
        if self.dialog:
            self.dialog.dismiss()

    def select_avatar(self):
        if not self.file_manager:
            self.file_manager = MDFileManager(
                exit_manager=self.close_file_manager,
                select_path=self.set_avatar
            )
        self.file_manager.show(os.path.expanduser("~"))
    
    def close_file_manager(self, *args):
        self.file_manager.close()
    
    def set_avatar(self, path):
        self.vm.update_user(avatar_path=path)
        self.ids.avatar_img.source = path
        self.close_file_manager()

    def user_logout(self):
        """Сброс локального пользователя на дефолтного (Guest)."""
        if self.vm:
            self.vm.reset_user()
        self._refresh_ui()
        self.get_app().switch_language(self.vm.language)
        self.get_app().switch_theme(self.vm.theme)

    def get_app(self):
        from kivymd.app import MDApp
        return MDApp.get_running_app()