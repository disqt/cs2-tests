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
    def test_bot_add(self, rcon, clean_server):
        """Adding a bot increases player count."""
        rcon.command("bot_kick")
        time.sleep(1)
        before = get_bot_count(rcon)
        rcon.command("css_bot add 1")
        time.sleep(2)
        after = get_bot_count(rcon)
        assert after > before, f"Bot count didn't increase: {before} -> {after}"

    def test_bot_add_ct(self, rcon, clean_server):
        """Adding a CT bot works."""
        rcon.command("bot_kick")
        time.sleep(1)
        rcon.command("css_bot add 1 ct")
        time.sleep(2)
        count = get_bot_count(rcon)
        assert count >= 1, f"Expected at least 1 bot, got {count}"

    def test_bot_add_t(self, rcon, clean_server):
        """Adding a T bot works."""
        rcon.command("bot_kick")
        time.sleep(1)
        rcon.command("css_bot add 1 t")
        time.sleep(2)
        count = get_bot_count(rcon)
        assert count >= 1, f"Expected at least 1 bot, got {count}"

    def test_bot_kick_all(self, rcon, clean_server):
        """Kicking all bots removes them."""
        rcon.command("css_bot add 1")
        time.sleep(2)
        rcon.command("bot_kick")
        time.sleep(2)
        count = get_bot_count(rcon)
        assert count == 0, f"Expected 0 bots after kick, got {count}"

    def test_bot_difficulty(self, rcon, clean_server):
        """Setting bot difficulty doesn't error."""
        response = rcon.command("css_bot difficulty 3")
        assert "unknown" not in response.lower()
        assert "error" not in response.lower()

    def test_bot_add_kick_cycle(self, rcon, clean_server):
        """Add then kick bots cleanly."""
        rcon.command("bot_kick")
        time.sleep(1)
        rcon.command("css_bot add 1")
        time.sleep(2)
        mid = get_bot_count(rcon)
        assert mid >= 1, "Bot was not added"
        rcon.command("bot_kick")
        time.sleep(2)
        final = get_bot_count(rcon)
        assert final == 0, f"Bots not cleaned up: {final}"
