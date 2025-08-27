from data.user_repo import UserRepository
from data.translations import translations


class UserViewModel:
    def __init__(self):
        self.user = UserRepository.ensure_default_user()
        self.language = self.user.language
        self.theme = self.user.theme
    
    def refresh(self):
        self.user = UserRepository.ensure_default_user()
        self.language = self.user.language
        self.theme = self.user.theme
        return self.user
        
    def get_user_dict(self) -> dict:
        u = self.refresh()
        
        return {
            "name": u.name,
            "full_name": u.full_name or "",
            "email": u.email or "",
            "phone": u.phone or "",
            "avatar_path": u.avatar_path or "",
            "bio": u.bio or "",
            "theme": u.theme,
            "language": u.language,
            "is_premium": u.is_premium,
            "scan_count": u.scan_count,
            "generate_count": u.generate_count,
            "history_enabled": u.history_enabled,
            "created_at": str(u.created_at),
            "updated_at": str(u.updated_at),
            "last_login": str(u.last_login) if u.last_login else ""
        }
    
    def update_user(self, **kwargs) -> dict:
        self.user = UserRepository.update_user(**kwargs)
        self.language = self.user.language
        self.theme = self.user.theme
        return self.get_user_dict()
    
    def reset_user(self):
        UserRepository.delete_user()
        self.user = UserRepository.ensure_default_user()
        self.language = self.user.language
        self.theme = self.user.theme
        return self.get_user_dict()
    
    def get_translation(self, key: str) -> str:
        return translations.get(self.language, {}).get(key, key)