from datetime import datetime
from models.user_model import User


class UserRepository:
    @staticmethod
    def get_user() -> User | None:
        return User.select().first()
    
    @staticmethod
    def ensure_default_user() -> User:
        user = UserRepository.get_user()
        
        if not user:
            user = User.create(name="Гость", last_login=datetime.now())
        return user
    
    @staticmethod
    def create_user(name="Гость", email=None, phone=None, avatar_path=None, theme='dark', language='ru') -> User:
        return User.create(name=name, email=email, phone=phone, avatar_path=avatar_path, theme=theme, language=language)
    
    @staticmethod
    def update_user(name=None, email=None, phone=None, avatar_path=None, theme=None, language=None) -> User | None:
        user = UserRepository.ensure_default_user()
        
        if name is not None: user.name = name
        if email is not None: user.email = email
        if phone is not None: user.phone = phone
        if avatar_path is not None: user.avatar_path = avatar_path
        if theme is not None: user.theme = theme
        if language is not None: user.language = language
        
        user.last_login = datetime.now()
        user.save()
        
        return user
    
    @staticmethod
    def delete_user():
        user = UserRepository.get_user()
        
        if user:
            user.delete_instance()

    @staticmethod
    def inc_scan_count(n: int = 1):
        u = UserRepository.ensure_default_user()
        u.scan_count += n
        u.save()
        return u
    
    @staticmethod
    def inc_generate_count(n: int = 1):
        u = UserRepository.ensure_default_user()
        u.generate_count += n
        u.save()
        return u
    
    @staticmethod
    def set_history_enabled(enabled: bool):
        u = UserRepository.ensure_default_user()
        u.history_enabled = enabled
        u.save()
        return u