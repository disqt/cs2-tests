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

    def test_vampire_toggle(self, rcon, clean_server):
        """css_vampire command is accepted."""
        response = rcon.command("css_vampire")
        assert "unknown" not in response.lower(), f"Command unknown: {response}"

    def test_ammo_toggle(self, rcon, clean_server):
        """css_ammo command is accepted."""
        response = rcon.command("css_ammo")
        assert "unknown" not in response.lower(), f"Command unknown: {response}"
