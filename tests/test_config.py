from config import get_config


def test_config_has_required_fields():
    cfg = get_config()
    assert cfg.host
    assert cfg.port > 0
    assert cfg.password


def test_config_defaults():
    """Host defaults to localhost, port defaults to 27015."""
    import os
    from unittest.mock import patch

    env_override = {
        "CS2_RCON_PASSWORD": "test",
    }
    remove_keys = ["CS2_RCON_HOST", "CS2_RCON_PORT"]

    with patch("config.load_dotenv"), \
         patch.dict(os.environ, env_override, clear=False):
        for k in remove_keys:
            os.environ.pop(k, None)
        cfg = get_config()
        assert cfg.host == "localhost"
        assert cfg.port == 27015
