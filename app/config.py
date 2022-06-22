import os
from functools import lru_cache
from typing import Optional, Union

from pydantic import BaseSettings
from starlette.config import Config

getenv = Config('.env.example')


class GlobalConfig(BaseSettings):
    DESCRIPTION: str = (
        'Вступительное задание в Летнюю Школу Бэкенд Разработки Яндекса 2022'
    )
    DEBUG: bool = False
    TESTING: bool = False
    SERVICE_NAME: str = 'Mega Market Open API'
    VERSION: str = '1.0'
    ENVIRONMENT: Optional[str] = getenv(
        'ENVIRONMENT', cast=str, default=os.environ.get('ENVIRONMENT')
    )
    DATABASE_URL: str = getenv(
        'DATABASE_URL', cast=str, default=os.environ.get('DATABASE_URL')
    )


class DevConfig(GlobalConfig):
    DESCRIPTION: str = 'ATTENTION: DevConfig are on'
    DEBUG: bool = True


class TestConfig(GlobalConfig):
    DESCRIPTION: str = 'ATTENTION: TestConfig are on'
    DEBUG: bool = True
    TESTING: bool = True


class FactoryConfig:
    """Returns a config instance depends on the ENV_STATE variable."""

    def __init__(self, environment: Optional[str]):
        self.environment = environment

    def __call__(self) -> Union[TestConfig, DevConfig]:
        if self.environment == 'TEST':
            return TestConfig()
        return DevConfig()  # pragma: no cover


@lru_cache()
def get_configuration() -> Union[TestConfig, DevConfig]:
    return FactoryConfig(GlobalConfig().ENVIRONMENT)()


config = get_configuration()
