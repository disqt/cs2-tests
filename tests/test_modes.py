import pytest

from conftest import wait_for_reconnect


@pytest.mark.destructive
class TestModes:
    """Test game mode switching via DisqtModes commands.

    Modes: !practice (sv_cheats), !1v1 (K4-Arenas), !casual (default).
    Each mode executes a cfg that may trigger a map change, dropping RCON.
    """

    def test_switch_to_practice(self, rcon, clean_server):
        """Practice mode enables sv_cheats and infinite ammo."""
        rcon.command("css_practice")
        wait_for_reconnect(rcon)
        cheats = rcon.command("sv_cheats")
        assert "true" in cheats.lower() or "1" in cheats

    def test_switch_to_casual(self, rcon, clean_server):
        """Casual mode returns server to default state."""
        rcon.command("css_practice")
        wait_for_reconnect(rcon)
        rcon.command("css_casual")
        wait_for_reconnect(rcon)
        response = rcon.command("status")
        assert response, "Server not responding after returning to casual"

    def test_practice_cheats_disabled_after_casual(self, rcon, clean_server):
        """sv_cheats disabled after returning from practice to casual."""
        rcon.command("css_practice")
        wait_for_reconnect(rcon)
        rcon.command("css_casual")
        wait_for_reconnect(rcon)
        cheats = rcon.command("sv_cheats")
        assert "false" in cheats.lower() or "0" in cheats
