import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    host: str
    port: int
    password: str


def get_config() -> Config:
    load_dotenv()
    password = os.environ.get("CS2_RCON_PASSWORD", "")
    if not password:
        raise ValueError("CS2_RCON_PASSWORD is required")
    return Config(
        host=os.environ.get("CS2_RCON_HOST", "localhost"),
        port=int(os.environ.get("CS2_RCON_PORT", "27015")),
        password=password,
    )
