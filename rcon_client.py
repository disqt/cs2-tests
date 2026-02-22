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
        # Read until AUTH_RESPONSE; some servers send an empty
        # RESPONSE_VALUE first, others skip straight to AUTH_RESPONSE.
        while True:
            pkt_id, pkt_type, _ = self._recv_packet()
            if pkt_type == 2:  # AUTH_RESPONSE
                if pkt_id == -1:
                    raise RconAuthError("Authentication failed")
                return

    def close(self) -> None:
        if self._sock:
            self._sock.close()
            self._sock = None

    def reconnect(self) -> None:
        """Close and re-establish connection. Used after map/mode changes."""
        self.close()
        self.connect()

    # Responses above this size may be fragmented across multiple packets.
    # A sentinel is sent to detect the end of a multi-packet response.
    FRAG_THRESHOLD = 4096

    def _command_once(self, cmd: str) -> str:
        cmd_id = self._next_id()
        self._send_packet(cmd_id, self.SERVERDATA_EXECCOMMAND, cmd)
        end_id = self._next_id()
        self._send_packet(end_id, self.SERVERDATA_RESPONSE_VALUE, "")
        response = []
        while True:
            pkt_id, _, body = self._recv_packet()
            if pkt_id == end_id:
                break
            if body:
                response.append(body)
        # CS2 may still be flushing packets for this command after the
        # sentinel reply arrives (empty ack / late data). Drain them
        # with a short non-blocking read so they don't pollute the
        # next command's response.
        self._drain()
        return "".join(response)

    def _drain(self) -> None:
        """Drain any late packets CS2 sends after the sentinel reply.

        CS2's RCON can send an empty ack + real data for a command, with
        the sentinel echo arriving between them.  Without draining, the
        late data packet pollutes the next command's response.
        """
        self._sock.settimeout(0.05)
        try:
            while True:
                self._sock.recv(4096)
        except (socket.timeout, BlockingIOError):
            pass
        finally:
            self._sock.settimeout(self.timeout)

    def command(self, cmd: str, retries: int = 1) -> str:
        """Send command with auto-reconnect on connection failure."""
        if not self._sock:
            raise RconError("Not connected")
        for attempt in range(1 + retries):
            try:
                return self._command_once(cmd)
            except (TimeoutError, RconError, OSError):
                if attempt < retries:
                    import time
                    time.sleep(2)
                    try:
                        self.reconnect()
                    except (TimeoutError, RconError, OSError):
                        pass
                else:
                    raise

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *exc):
        self.close()
