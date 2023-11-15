# import required libraries
import sys

from vidgear.gears import NetGear


class NetgearClient:
    """Creates a tcp Netgear client

    Args:
        IP: IP address of the Netgear server.
        PORT: Port address of the Netgear server.
    """

    def __init__(self, ADDRESS="127.0.0.100", PORT="5454") -> None:
        # define various tweak flags
        options = {
            "bidirectional_mode": True,
            "max_retries": sys.maxsize,
            "jpeg_compression": False,
        }
        # Define Netgear Server with default parameters
        self.client = NetGear(
            address=ADDRESS,
            port=PORT,
            protocol="tcp",
            pattern=1,
            receive_mode=True,
            logging=True,
            **options
        )
