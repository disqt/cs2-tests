import re


def test_server_responds(rcon):
    """Server responds to status command with map and player info."""
    response = rcon.command("status")
    assert response, "Empty response from status"
    assert "map" in response.lower()


def test_max_players(rcon):
    """Server reports max players in status (launched with -maxplayers 10)."""
    response = rcon.command("status")
    # CS2 status format: "players  : 0 humans, 2 bots (10 max)"
    match = re.search(r"\((\d+)\s*max\)", response)
    assert match, f"Could not find max players in: {response}"


def test_sv_cheats_on(rcon):
    """sv_cheats is enabled (server boots in practice mode)."""
    response = rcon.command("sv_cheats")
    assert "true" in response.lower() or "1" in response


def test_server_cfg_applied(rcon):
    """sv_minrate is set to 128000 per server.cfg."""
    response = rcon.command("sv_minrate")
    assert "128000" in response
