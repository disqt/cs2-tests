import pytest


@pytest.mark.destructive
class TestModifiers:
    def test_headshot_toggle(self, rcon, clean_server):
        """css_headshot command is accepted."""
        response = rcon.command("css_headshot")
        assert "unknown" not in response.lower(), f"Command unknown: {response}"

    def test_pistol_toggle(self, rcon, clean_server):
        """css_pistol command is accepted."""
        response = rcon.command("css_pistol")
        assert "unknown" not in response.lower(), f"Command unknown: {response}"

    def test_awp_toggle(self, rcon, clean_server):
        """css_awp command is accepted."""
        response = rcon.command("css_awp")
        assert "unknown" not in response.lower(), f"Command unknown: {response}"
