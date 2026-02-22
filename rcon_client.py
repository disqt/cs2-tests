import socket
import struct


class RconError(Exception):
    pass


class RconAuthError(RconError):
    pass


class RconClient:
    SERVERDATA_AUTH = 3
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_RESPONSE_VALUE = 0

    def __init__(self, host: str, port: int, password: str, timeout: float = 10.0):
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout
        self._sock: socket.socket | None = None
        self._id = 0

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    @staticmethod
    def _encode_packet(pkt_id: int, pkt_type: int, body: str) -> bytes:
        payload = body.encode("utf-8") + b"\x00\x00"
        size = len(payload) + 8  # id(4) + type(4) + payload
        return struct.pack("<iii", size, pkt_id, pkt_type) + payload

    @staticmethod
    def _decode_packet(data: bytes) -> tuple[int, int, str]:
        pkt_id, pkt_type = struct.unpack_from("<ii", data, 0)
        body = data[8:-2].decode("utf-8", errors="replace")
        return pkt_id, pkt_type, body

    def _recv_packet(self) -> tuple[int, int, str]:
        raw_size = self._recv_bytes(4)
        size = struct.unpack("<i", raw_size)[0]
        data = self._recv_bytes(size)
        return self._decode_packet(data)

    def _recv_bytes(self, n: int) -> bytes:
        buf = b""
        while len(buf) < n:
            chunk = self._sock.recv(n - len(buf))
            if not chunk:
                raise RconError("Connection closed")
            buf += chunk
        return buf

    def _send_packet(self, pkt_id: int, pkt_type: int, body: str) -> None:
        self._sock.sendall(self._encode_packet(pkt_id, pkt_type, body))

    def connect(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(self.timeout)
        self._sock.connect((self.host, self.port))
        auth_id = self._next_id()
        self._send_packet(auth_id, self.SERVERDATA_AUTH, self.password)
        for _ in range(2):
            pkt_id, pkt_type, _ = self._recv_packet()
            if pkt_type == 2:  # AUTH_RESPONSE
                if pkt_id == -1:
                    raise RconAuthError("Authentication failed")
                return
        raise RconError("Unexpected auth response")

    def close(self) -> None:
        if self._sock:
            self._sock.close()
            self._sock = None

    def command(self, cmd: str) -> str:
        if not self._sock:
            raise RconError("Not connected")
        cmd_id = self._next_id()
        self._send_packet(cmd_id, self.SERVERDATA_EXECCOMMAND, cmd)
        end_id = self._next_id()
        self._send_packet(end_id, self.SERVERDATA_RESPONSE_VALUE, "")
        response = []
        while True:
            pkt_id, _, body = self._recv_packet()
            if pkt_id == end_id:
                break
            response.append(body)
        return "".join(response)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *exc):
        self.close()
