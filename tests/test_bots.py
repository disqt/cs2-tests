import re
import time

import pytest


def get_bot_count(rcon) -> int:
    """Extract bot count from status output."""
    response = rcon.command("status")
    match = re.search(r"(\d+)\s*bots", response)
    return int(match.group(1)) if match else 0


@pytest.mark.destructive
class TestBots:
    def test_bot_add_and_kick(self, rcon, clean_server):
        """Add a bot, verify it exists, kick it, verify it's gone."""
        rcon.command("bot_kick")
        time.sleep(1)
        rcon.command("css_bot add 1")
        time.sleep(2)
        count = get_bot_count(rcon)
        assert count >= 1, f"Bot was not added, got {count}"
        rcon.command("bot_kick")
        time.sleep(2)
        count = get_bot_count(rcon)
        assert count == 0, f"Bots not cleaned up: {count}"

    def test_bot_kick(self, rcon, clean_server):
        """Kicking bots when none exist doesn't error."""
        response = rcon.command("bot_kick")
        assert response is not None
