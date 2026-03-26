import os


class Config:
    DEBUG: bool = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    TESTING: bool = False
    FRANKFURTER_BASE_URL: str = os.getenv(
        "FRANKFURTER_BASE_URL", "https://api.frankfurter.app"
    )
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "5"))


class TestingConfig(Config):
    TESTING: bool = True
    DEBUG: bool = True
