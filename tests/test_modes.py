import pytest

from conftest import wait_for_reconnect


@pytest.mark.destructive
class TestModes:
    """Test game mode switching via DisqtModes commands.

    Modes: !1v1 (fast rounds, no bomb), !practice (sv_cheats, grenades).
    Each mode executes a cfg that triggers mp_restartgame, dropping RCON.
    """

    def test_switch_to_1v1(self, rcon, clean_server):
        """1v1 mode disables sv_cheats and removes bomb."""
        rcon.command("css_1v1")
        wait_for_reconnect(rcon)
        cheats = rcon.command("sv_cheats")
        assert "false" in cheats.lower() or "0" in cheats

    def test_switch_to_practice(self, rcon, clean_server):
        """Practice mode enables sv_cheats and infinite ammo."""
        rcon.command("css_practice")
        wait_for_reconnect(rcon)
        cheats = rcon.command("sv_cheats")
        assert "true" in cheats.lower() or "1" in cheats

    def test_1v1_then_practice(self, rcon, clean_server):
        """Can switch from 1v1 to practice."""
        rcon.command("css_1v1")
        wait_for_reconnect(rcon)
        rcon.command("css_practice")
        wait_for_reconnect(rcon)
        cheats = rcon.command("sv_cheats")
        assert "true" in cheats.lower() or "1" in cheats
