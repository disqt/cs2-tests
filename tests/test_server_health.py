import re


def test_server_responds(rcon):
    """Server responds to status command with map and player info."""
    response = rcon.command("status")
    assert response, "Empty response from status"
    assert "map" in response.lower()


def test_max_players(rcon):
    """Server is configured for 10 max players."""
    response = rcon.command("status")
    match = re.search(r"maxplayers\s*:\s*(\d+)", response)
    assert match, f"Could not find maxplayers in: {response}"
    assert int(match.group(1)) == 10


def test_sv_cheats_off(rcon):
    """sv_cheats is 0."""
    response = rcon.command("sv_cheats")
    assert "0" in response


def test_server_cfg_applied(rcon):
    """mp_warmuptime is set to 10 per server.cfg."""
    response = rcon.command("mp_warmuptime")
    assert "10" in response
