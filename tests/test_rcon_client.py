import struct

import pytest

from rcon_client import RconClient


def test_encode_packet():
    """Packet format: [4B size LE][4B id LE][4B type LE][body\\0][\\0]"""
    pkt = RconClient._encode_packet(42, 3, "password")
    size, pkt_id, pkt_type = struct.unpack_from("<iii", pkt, 0)
    assert size == 18
    assert pkt_id == 42
    assert pkt_type == 3
    assert pkt[12:] == b"password\x00\x00"


def test_decode_packet():
    """Decode a well-formed response packet (data after the size field)."""
    body = b"response text"
    # _decode_packet receives the payload after the 4-byte size prefix
    raw = struct.pack("<ii", 1, 0) + body + b"\x00\x00"
    pkt_id, pkt_type, pkt_body = RconClient._decode_packet(raw)
    assert pkt_id == 1
    assert pkt_type == 0
    assert pkt_body == "response text"


@pytest.mark.integration
def test_rcon_connect_and_status():
    """Integration: connect to real server and run status."""
    from config import get_config
    cfg = get_config()
    with RconClient(cfg.host, cfg.port, cfg.password) as rcon:
        response = rcon.command("status")
        assert "map" in response.lower()
