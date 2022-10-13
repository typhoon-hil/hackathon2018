"""This module facilitates OpenADR communication with the framework component."""

from typing import Optional, Generator
from hackathon.utils.utils import *

__author__ = "Petar Bajic"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

class FrameworkLink:
    """
    Abstraction that represents connection between framework and openADRR VTN.
    """
    def __init__(self,
                 in_port: Optional[int]=None, in_addr: Optional[str]=None,
                 out_port: Optional[int]=None, out_addr: Optional[str]=None) \
                 -> None:
        """
        Communication sockets can be given by address and port, if not
        configuration file is used.

        """
        # print("FrameworkLink in_port: " + str(in_port) + ", in_addr: " + str(in_addr))

        self.in_socket_vtn, self.in_context_vtn = bind_sub_socket(
            CFG.in_address_vtn, CFG.in_port_vtn)


    def get_data_vtn(self) -> Generator[DataMessage, None, None]:
        """Get vtn data from the framework.

        Generator containing data is being returned.

        """
        while True:
            msg = self.in_socket_vtn.recv_pyobj()
            if msg:
                yield msg
            else:
                return

