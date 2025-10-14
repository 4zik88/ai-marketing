"""
Валидаторы для Google Ads и других форматов
"""
from typing import List, Tuple


class GoogleAdsValidator:
    """Валидатор для объявлений Google Ads"""
    
    # Технические ограничения Google Ads
    HEADLINE_MAX_LENGTH = 30
    DESCRIPTION_MAX_LENGTH = 90
    PATH_MAX_LENGTH = 15
    
    @classmethod
    def validate_headline(cls, headline: str) -> Tuple[bool, str]:
        """
        Валидирует заголовок
        
        Returns:
            (valid, message)
        """
        if not headline:
            return False, "Заголовок не может быть пустым"
        
        if len(headline) > cls.HEADLINE_MAX_LENGTH:
            return False, f"Заголовок слишком длинный: {len(headline)} символов (макс. {cls.HEADLINE_MAX_LENGTH})"
        
        return True, "OK"
    
    @classmethod
    def validate_description(cls, description: str) -> Tuple[bool, str]:
        """
        Валидирует описание
        
        Returns:
            (valid, message)
        """
        if not description:
            return False, "Описание не может быть пустым"
        
        if len(description) > cls.DESCRIPTION_MAX_LENGTH:
            return False, f"Описание слишком длинное: {len(description)} символов (макс. {cls.DESCRIPTION_MAX_LENGTH})"
        
        return True, "OK"
    
    @classmethod
    def validate_path(cls, path: str) -> Tuple[bool, str]:
        """
        Валидирует путь
        
        Returns:
            (valid, message)
        """
        if not path:
            return True, "OK"  # Путь опционален
        
        if len(path) > cls.PATH_MAX_LENGTH:
            return False, f"Путь слишком длинный: {len(path)} символов (макс. {cls.PATH_MAX_LENGTH})"
        
        # Проверка на специальные символы
        if not path.replace('-', '').replace('_', '').isalnum():
            return False, "Путь может содержать только буквы, цифры, дефисы и подчеркивания"
        
        return True, "OK"
    
    @classmethod
    def validate_ad(cls, headline: str, description: str, 
                   path1: str = "", path2: str = "") -> List[str]:
        """
        Валидирует полное объявление
        
        Returns:
            Список ошибок (пустой список если все ок)
        """
        errors = []
        
        valid, msg = cls.validate_headline(headline)
        if not valid:
            errors.append(f"Заголовок: {msg}")
        
        valid, msg = cls.validate_description(description)
        if not valid:
            errors.append(f"Описание: {msg}")
        
        if path1:
            valid, msg = cls.validate_path(path1)
            if not valid:
                errors.append(f"Путь 1: {msg}")
        
        if path2:
            valid, msg = cls.validate_path(path2)
            if not valid:
                errors.append(f"Путь 2: {msg}")
        
        return errors
    
    @classmethod
    def truncate_headline(cls, headline: str) -> str:
        """Обрезает заголовок до максимальной длины"""
        if len(headline) <= cls.HEADLINE_MAX_LENGTH:
            return headline
        return headline[:cls.HEADLINE_MAX_LENGTH-3] + "..."
    
    @classmethod
    def truncate_description(cls, description: str) -> str:
        """Обрезает описание до максимальной длины"""
        if len(description) <= cls.DESCRIPTION_MAX_LENGTH:
            return description
        return description[:cls.DESCRIPTION_MAX_LENGTH-3] + "..."


def validate_url(url: str) -> bool:
    """
    Проверяет валидность URL
    
    Args:
        url: URL для проверки
        
    Returns:
        True если URL валиден
    """
    from urllib.parse import urlparse
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

