import time

import pytest

from config import get_config
from rcon_client import RconClient, RconError


def wait_for_reconnect(rcon, timeout: float = 20.0) -> None:
    """Wait for server to accept RCON connections after a map/mode change.

    Map changes drop the TCP connection. This polls until the server
    is back up and we can reconnect + send a command.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            rcon.reconnect()
            # CS2 may return empty on the first command after reconnect.
            # Retry a couple of times before considering the server ready.
            for _ in range(3):
                resp = rcon.command("status")
                if resp:
                    return
                time.sleep(0.5)
        except (TimeoutError, RconError, OSError):
            pass
        time.sleep(2)
    raise RconError(f"Server did not come back within {timeout}s")


def reset_server(rcon):
    """Full server reset: modifiers, mode, bots.

    Resets DisqtModes modifier state (internal booleans + cvars),
    switches back to practice (default mode), then kicks bots.
    """
    rcon.command("css_reset")
    rcon.command("exec practice.cfg")
    wait_for_reconnect(rcon)
    rcon.command("bot_kick")


@pytest.fixture(scope="session")
def rcon():
    """Session-scoped RCON connection. Reused across all tests."""
    cfg = get_config()
    client = RconClient(cfg.host, cfg.port, cfg.password)
    client.connect()
    yield client
    # Session teardown: leave server in clean state
    try:
        reset_server(client)
    except (TimeoutError, RconError, OSError):
        pass
    client.close()


@pytest.fixture()
def clean_server(rcon):
    """Reset server state after each destructive test."""
    yield
    reset_server(rcon)


def wait_for_map(rcon, expected_map: str, timeout: float = 30.0) -> bool:
    """Wait for server to load expected map (reconnects if needed)."""
    # Map change drops connection -- wait for server to come back first
    time.sleep(3)
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            response = rcon.command("status")
            if expected_map in response.lower():
                return True
        except (TimeoutError, RconError, OSError):
            try:
                rcon.reconnect()
            except (TimeoutError, RconError, OSError):
                pass
        time.sleep(2)
    return False
