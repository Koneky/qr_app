from data.user_repo import UserRepository
from data.translations import translations


class UserViewModel:
    def __init__(self):
        # Гарантируемя, что пользователь существует
        self.user = UserRepository.ensure_default_user()
        self.language = "ru"
        self.theme = "dark"
    
    def refresh(self):
        self.user = UserRepository.ensure_default_user()
        return self.user
        
    def get_user_dict(self) -> dict:
        u = self.refresh()
        
        return {
            "name": u.name,
            "email": u.email or "",
            "phone": u.phone or "",
            "avatar_path": u.avatar_path or "",
            "theme": u.theme,
            "language": u.language,
        }
    
    def update_user(self, **kwargs) -> dict:
        self.user = UserRepository.update_user(**kwargs)
        return self.get_user_dict()
    
    def reset_user(self):
        UserRepository.delete_user()
        self.user = UserRepository.ensure_default_user()
        return self.get_user_dict()
    
    def get_translation(self, key: str) -> str:
        return translations.get(self.language, {}).get(key, key)