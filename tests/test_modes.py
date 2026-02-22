import time

import pytest


@pytest.mark.destructive
class TestModes:
    def test_current_mode_reports(self, rcon):
        """css_currentmode returns a mode name."""
        response = rcon.command("css_currentmode")
        assert response, "Empty response from css_currentmode"

    def test_switch_to_competitive(self, rcon, clean_server):
        """Switch to competitive mode."""
        rcon.command("css_changemode comp")
        time.sleep(3)
        response = rcon.command("css_currentmode")
        assert "comp" in response.lower(), f"Mode not competitive: {response}"

    def test_switch_to_wingman(self, rcon, clean_server):
        """Switch to wingman mode."""
        rcon.command("css_changemode wingman")
        time.sleep(3)
        response = rcon.command("css_currentmode")
        assert "wingman" in response.lower(), f"Mode not wingman: {response}"

    def test_switch_to_retakes(self, rcon, clean_server):
        """Switch to retakes mode."""
        rcon.command("css_changemode retakes")
        time.sleep(3)
        response = rcon.command("css_currentmode")
        assert "retake" in response.lower(), f"Mode not retakes: {response}"

    def test_switch_to_gungame(self, rcon, clean_server):
        """Switch to gun game mode."""
        rcon.command("css_changemode gungame")
        time.sleep(3)
        response = rcon.command("css_currentmode")
        assert "gungame" in response.lower() or "gun" in response.lower(), (
            f"Mode not gungame: {response}"
        )

    def test_return_to_casual(self, rcon, clean_server):
        """Switch to another mode then back to casual."""
        rcon.command("css_changemode comp")
        time.sleep(3)
        rcon.command("css_changemode casual")
        time.sleep(3)
        response = rcon.command("css_currentmode")
        assert "casual" in response.lower(), f"Mode not casual: {response}"
