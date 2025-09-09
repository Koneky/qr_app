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
    def create_user(
        name="Гость", full_name=None, email=None, phone=None, avatar_path=None,
        bio=None, theme='dark', language='ru'
    ) -> User:
        return User.create(
            name=name, full_name=full_name, email=email, phone=phone,
            avatar_path=avatar_path, bio=bio, theme=theme, language=language
        )
    
    @staticmethod
    def update_user(
        name=None, full_name=None, email=None, phone=None,
        avatar_path=None, bio=None, theme=None, language=None,
        is_premium=None, scan_count=None, generate_count=None,
        history_enabled=None
    ) -> User | None:
        user = UserRepository.ensure_default_user()
        
        if name is not None:
            user.name = name
        if full_name is not None:
            user.full_name = full_name
        if email is not None:
            user.email = email
        if phone is not None:
            user.phone = phone
        if avatar_path is not None:
            user.avatar_path = avatar_path
        if bio is not None:
            user.bio = bio
        if theme is not None:
            user.theme = theme
        if language is not None:
            user.language = language
        if is_premium is not None:
            user.is_premium = is_premium
        if scan_count is not None:
            user.scan_count = scan_count
        if generate_count is not None:
            user.generate_count = generate_count
        if history_enabled is not None:
            user.history_enabled = history_enabled
        
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