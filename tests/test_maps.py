import pytest

from conftest import wait_for_map


@pytest.mark.slow
@pytest.mark.destructive
class TestMaps:
    def test_current_map_reports(self, rcon):
        """css_currentmap returns a map name."""
        response = rcon.command("css_currentmap")
        assert response, "Empty response from css_currentmap"

    def test_changemap_mirage(self, rcon, clean_server):
        """Change to de_mirage."""
        rcon.command("css_changemap de_mirage")
        assert wait_for_map(rcon, "de_mirage"), "Map did not change to de_mirage"

    def test_changemap_inferno(self, rcon, clean_server):
        """Change to de_inferno."""
        rcon.command("css_changemap de_inferno")
        assert wait_for_map(rcon, "de_inferno"), "Map did not change to de_inferno"

    def test_workshop_map_load(self, rcon, clean_server):
        """Load a known workshop map (aim_botz)."""
        rcon.command("host_workshop_map 243702660")
        assert wait_for_map(rcon, "workshop", timeout=30.0), (
            "Workshop map did not load"
        )

    def test_invalid_map_no_crash(self, rcon):
        """Invalid map name doesn't crash the server."""
        pre_status = rcon.command("status")
        rcon.command("css_changemap de_nonexistent_map_xyz")
        post_status = rcon.command("status")
        assert "map" in post_status.lower(), "Server not responding after bad map"
