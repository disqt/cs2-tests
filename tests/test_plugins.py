import pytest

# Display names as reported by css_plugins list (not folder names)
EXPECTED_PLUGINS = [
    "CS2Rcon",
    "Disqt Modes",
    "FixRandomSpawn",
    "InventorySimulator",
    "SimpleAdmin",
]


def test_counterstrikesharp_loaded(rcon):
    """CounterStrikeSharp responds to css_plugins list."""
    response = rcon.command("css_plugins list")
    assert response, "Empty response from css_plugins list"
    assert any(p in response for p in EXPECTED_PLUGINS)


@pytest.mark.parametrize("plugin_name", EXPECTED_PLUGINS)
def test_plugin_loaded(rcon, plugin_name):
    """Each expected plugin appears in the plugin list."""
    response = rcon.command("css_plugins list")
    assert plugin_name in response, (
        f"{plugin_name} not found in plugin list:\n{response}"
    )


def test_no_plugins_in_error_state(rcon):
    """No plugins are in error or unloaded state."""
    response = rcon.command("css_plugins list").lower()
    assert "error" not in response, f"Plugin error found:\n{response}"


def test_metamod_loaded(rcon):
    """MetaMod responds to meta list."""
    response = rcon.command("meta list")
    assert response, "Empty response from meta list"


def test_disqtmodes_commands_registered(rcon):
    """DisqtModes help command responds."""
    response = rcon.command("css_help")
    assert response, "Empty response from css_help"
