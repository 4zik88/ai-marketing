"""
Конфигурация приложения для AI Marketing
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # API ключи
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = ""
    groq_api_key: str = ""
    
    # Провайдер AI
    ai_provider: Literal["openai", "anthropic", "google", "ollama", "groq"] = "google"
    ai_model: str = "gemini-2.0-flash"
    
    # Директории
    base_dir: Path = Path(__file__).parent
    output_dir: Path = base_dir / "output"
    
    # Параметры парсинга
    request_timeout: int = 30
    max_retries: int = 3
    
    # Параметры Google Ads
    google_ads_developer_token: str = ""
    google_ads_client_id: str = ""
    google_ads_client_secret: str = ""
    google_ads_refresh_token: str = ""
    google_ads_login_customer_id: str = ""
    google_ads_config_path: str = ""  # Path to google-ads.yaml
    
    # Google Ads MCP Server
    google_ads_mcp_enabled: bool = False
    
    # Ограничения символов для Google Ads
    headline_max_length: int = 30
    description_max_length: int = 90
    path_max_length: int = 15
    
    # Authentication (HTTP Basic Auth)
    auth_enabled: bool = False  # Set to True to enable authentication
    auth_username: str = "admin"  # Default username
    auth_password: str = ""  # Set via environment variable AUTH_PASSWORD
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Создаем output директорию если её нет
        self.output_dir.mkdir(exist_ok=True)


# Глобальный экземпляр настроек
settings = Settings()

