import time

import pytest

from config import get_config
from rcon_client import RconClient


@pytest.fixture(scope="session")
def rcon():
    """Session-scoped RCON connection. Reused across all tests."""
    cfg = get_config()
    client = RconClient(cfg.host, cfg.port, cfg.password)
    client.connect()
    yield client
    client.close()


@pytest.fixture()
def clean_server(rcon):
    """Reset server state after each destructive test.

    Kicks bots, switches to casual, changes map to de_dust2.
    Used as explicit fixture on tests that mutate state.
    """
    yield
    rcon.command("bot_kick")
    rcon.command("css_changemode casual")
    time.sleep(2)


def wait_for_map(rcon, expected_map: str, timeout: float = 15.0) -> bool:
    """Poll status until map matches or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        response = rcon.command("status")
        for line in response.splitlines():
            if line.strip().startswith("map"):
                if expected_map in line:
                    return True
        time.sleep(1)
    return False
