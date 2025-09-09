import os
from kivymd.uix.filemanager import MDFileManager
from ui.screens.translatable_screen import TranslatableScreen
from viewmodel.user_viewmodel import UserViewModel


class ProfileScreen(TranslatableScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vm: UserViewModel = None
        self.file_manager = None
        self.dialog = None
        self.app = self.get_app()

    def on_kv_post(self, base):
        if self.vm is None:
            self.vm = self.app.user_vm
        self._refresh_ui()
    
    def on_pre_enter(self):
        self._refresh_ui()
    
    def _refresh_ui(self):
        user = self.vm.get_user_dict()

        full_name = user.get("full_name") or ""
        username = user.get("name") or self.app.translate("guest")
        self.ids.fullname_label.text = full_name
        self.ids.username_label.text = f"({username})" if full_name else username
        self.ids.phone_label.text = user.get("phone") or ""
        self.ids.email_label.text = user.get("email") or ""
        self.ids.bio_label.text = user.get("bio") or ""
        self.ids.premium_badge.opacity = 1 if user.get("is_premium") else 0

        scans_text = self.app.translate("scans")
        generates_text = self.app.translate("generates")
        self.ids.scans_label.text = f"{scans_text}: {user.get('scan_count', 0)}"
        self.ids.generates_label.text = f"{generates_text}: {user.get('generate_count', 0)}"

        self.ids.edit_profile_btn.text = self.app.translate("edit_profile")
        self.ids.logout_btn.text = self.app.translate("logout")

        avatar = self.ids.get("avatar_img")
        if avatar:
            avatar.source = user.get("avatar_path") or "assets/avatars/default.png"
    
    def open_edit_profile(self):
        # Переключение на отдельный экран редактирования
        self.app.root.current = 'edit_profile'
    
    def select_avatar(self):
        # Открытие file manager
        if not self.file_manager:
            self.file_manager = MDFileManager(
                exit_manager=self.close_file_manager,
                select_path=self.set_avatar
            )
        self.file_manager.show(os.path.expanduser("~"))
    
    def close_file_manager(self, *args):
        if self.file_manager:
            self.file_manager.close()
        
    def set_avatar(self, path):
        self.vm.update_user(avatar_path=path)
        self.ids.avatar_img.source = path
        self.close_file_manager()
    
    def user_logout(self):
        self.vm.reset_user()
        self._refresh_ui()
        self.app.switch_language(self.vm.language)
        self.app.switch_theme(self.vm.theme)
    
    def get_app(self):
        from kivymd.app import MDApp
        return MDApp.get_running_app()