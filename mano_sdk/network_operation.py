"""
    mano_sdk.network_operation
    ~~~~~~~~
    ETSI SOL Network Operation interface.
"""
from typing import Any, Dict

from mano_sdk.client import Client, Credentials

SOL_NETWORK_OPERATION_PATH = "/sol/nslcm/v1/ns_lcm_op_occs"


class NetworkOperation:
    """
        ETSI SOL Network Operation interface.
    """

    def __init__(
            self,
            endpoint_url: str,
            logger: Any,
            username=None,
            password=None,
            token=None
    ):

        self.cred = Credentials(
            username=username,
            password=password,
            token=token
        )
        self.client = Client(
            credentials=self.cred,
            endpoint_url=endpoint_url,
            logger=logger
        )

    def get(
            self,
            operation_id: str
    ) -> Dict[str, Any]:
        """
           Get the details of network operation.
        """
        path = "{}/{}".format(
            SOL_NETWORK_OPERATION_PATH,
            operation_id
        )
        return self.client.get(
            path=path,
            data="",
            params="",
            content_type="application/json",
            return_code=200
        )

    def list(
            self
    ) -> Dict[str, Any]:
        """
            Lists all network operations.
        """
        path = SOL_NETWORK_OPERATION_PATH
        return self.client.get(
            path=path,
            data="",
            params="",
            content_type="application/json",
            return_code=200
        )
