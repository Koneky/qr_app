from ui.screens.translatable_screen import TranslatableScreen
from viewmodel.user_viewmodel import UserViewModel


class EditProfileScreen(TranslatableScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = self.get_app()
        self.vm: UserViewModel = None

    def update_translations(self):
        self.ids.name_field.hint_text = self.app.translate("name")
        self.ids.fullname_field.hint_text = self.app.translate("fullname")
        self.ids.email_field.hint_text = self.app.translate("email")
        self.ids.phone_field.hint_text = self.app.translate("phone")
        self.ids.bio_field.hint_text = self.app.translate("bio")
        self.ids.cancel.text = self.app.translate("cancel")
        self.ids.save.text = self.app.translate("save")

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.populate_fields()

    def on_kv_post(self, base):
        self.vm = self.app.user_vm

    def populate_fields(self):
        data = self.vm.get_user_dict()
        self.ids.name_field.text = data.get("name") or ""
        self.ids.fullname_field.text = data.get("full_name") or ""
        self.ids.phone_field.text = data.get("phone") or ""
        self.ids.email_field.text = data.get("email") or ""
        self.ids.bio_field.text = data.get("bio") or ""
    
    def save(self):
        name = (self.ids.name_field.text or "").strip() or "Гость"
        full_name = (self.ids.fullname_field.text or "").strip() or None
        phone = (self.ids.phone_field.text or "").strip() or None
        email = (self.ids.email_field.text or "").strip() or None
        bio = (self.ids.bio_field.text or "").strip() or None

        self.vm.update_user(name=name, full_name=full_name, phone=phone, email=email, bio=bio)

        # Возвращаюсь на главный экран и обновляю профиль
        self.app.root.current = "main"
        
        try:
            main_screen = self.app.root.get_screen("main")
            profile_widget = main_screen.ids.profile_screen
            profile_widget._refresh_ui()
        except Exception:
            pass

    def get_app(self):
        from kivymd.app import MDApp
        return MDApp.get_running_app()