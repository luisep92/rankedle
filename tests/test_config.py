import os
from src.rankedle.config import Config


def test_read_config():
    config = Config()
    assert config.get("bot", "token") == os.getenv("BOT_TOKEN")
