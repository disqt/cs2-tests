import pytest

from conftest import wait_for_reconnect


@pytest.mark.destructive
class TestModes:
    """Test game mode switching via exec <mode>.cfg.

    GameModeManager's css_changemode/css_currentmode are CLIENT_ONLY
    (third-party compiled plugin), so we use native exec + status.
    """

    def test_switch_to_competitive(self, rcon, clean_server):
        """Switch to competitive mode."""
        rcon.command("exec comp.cfg")
        wait_for_reconnect(rcon)
        response = rcon.command("status")
        assert response, "Server not responding after mode switch"

    def test_switch_to_wingman(self, rcon, clean_server):
        """Switch to wingman mode."""
        rcon.command("exec wingman.cfg")
        wait_for_reconnect(rcon)
        response = rcon.command("status")
        assert response, "Server not responding after mode switch"

    def test_switch_to_retakes(self, rcon, clean_server):
        """Switch to retakes mode."""
        rcon.command("exec retakes.cfg")
        wait_for_reconnect(rcon)
        response = rcon.command("status")
        assert response, "Server not responding after mode switch"

    def test_switch_to_gungame(self, rcon, clean_server):
        """Switch to gun game mode."""
        rcon.command("exec gungame.cfg")
        wait_for_reconnect(rcon)
        response = rcon.command("status")
        assert response, "Server not responding after mode switch"

    def test_return_to_casual(self, rcon, clean_server):
        """Switch to another mode then back to casual."""
        rcon.command("exec comp.cfg")
        wait_for_reconnect(rcon)
        rcon.command("exec casual.cfg")
        wait_for_reconnect(rcon)
        response = rcon.command("status")
        assert response, "Server not responding after returning to casual"
