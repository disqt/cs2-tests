import pytest

from conftest import wait_for_map


@pytest.mark.slow
@pytest.mark.destructive
class TestMaps:
    """Test map changes via native changelevel command.

    GameModeManager's css_changemap is CLIENT_ONLY (third-party
    compiled plugin), so we use native changelevel + status.
    """

    def test_current_map_reports(self, rcon):
        """Status shows current map."""
        response = rcon.command("status")
        assert "de_" in response or "workshop" in response, (
            f"No map name in status: {response[:200]}"
        )

    def test_changemap_mirage(self, rcon, clean_server):
        """Change to de_mirage."""
        rcon.command("changelevel de_mirage")
        assert wait_for_map(rcon, "de_mirage"), "Map did not change to de_mirage"

    def test_changemap_inferno(self, rcon, clean_server):
        """Change to de_inferno."""
        rcon.command("changelevel de_inferno")
        assert wait_for_map(rcon, "de_inferno"), "Map did not change to de_inferno"

    @pytest.mark.skip(
        reason="Workshop maps set game_type=custom which breaks status "
        "output and requires full server restart to recover"
    )
    def test_workshop_map_load(self, rcon, clean_server):
        """Download and load a workshop map (aim_botz)."""
        rcon.command("host_workshop_map 3070244462")
        assert wait_for_map(rcon, "aim_botz", timeout=60.0), (
            "Workshop map did not load"
        )

    def test_invalid_map_no_crash(self, rcon):
        """Invalid map name doesn't crash the server."""
        rcon.command("changelevel de_nonexistent_map_xyz")
        response = rcon.command("status")
        assert "map" in response.lower(), "Server not responding after bad map"
