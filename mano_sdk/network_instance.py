"""
    mano_sdk.network_instance
    ~~~~~~~~
    ETSI SOL Network Instance interface.
"""
import json
from typing import Any, Dict, Optional

from mano_sdk.client import Client, Credentials

SOL_NETWORK_INSTANCE_PATH = "/sol/nslcm/v1/ns_instances"


class NetworkInstance:
    """
        ETSI SOL Network Instance interface
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

    def create(
            self,
            nsd_id: str,
            nsd_name: str,
            ns_description: Optional[str] = "",
            tags: Optional[Dict[str, str]] = None,
            content_type: Optional[str] = "application/json"
    ) -> Dict[str, Any]:
        """
           Creates an initial network instance.
        """
        data = {
            "nsdId": nsd_id,
            "nsName": nsd_name
        }
        if ns_description:
            data.update({"nsDescription": ns_description})
        if tags:
            data.update({
                "tags": tags
            })
        path = SOL_NETWORK_INSTANCE_PATH
        return self.client.post(
            path=path,
            data=json.dumps(data),
            params="",
            content_type=content_type
        )

    def instantiate(
            self,
            ns_instance_id: str,
            additional_params: Optional[Dict[str, str]] = None,
            dry_run: bool = False
    ) -> Dict[str, Any]:
        """
           Instantiates network instance using `ns_instance_id`.
        """
        if additional_params:
            data = {
                "additionalParamsForNs": additional_params
            }
            data = json.dumps(data)
        else:
            data = ""
        params = {
            "dryRun": dry_run
        }
        path = "{}/{}/instantiate".format(
            SOL_NETWORK_INSTANCE_PATH,
            ns_instance_id
        )
        return self.client.post(
            path=path,
            data=data,
            params=params,
            content_type="application/json"
        )

    def update(
            self,
            ns_instance_id: str,
            vnf_instance_id: str,
            vnf_configurable_properties: Optional[Dict[str, str]] = None
    ):
        """
           Updates the network instance.
        """

        path = "{}/{}/update".format(
            SOL_NETWORK_INSTANCE_PATH,
            ns_instance_id
        )

        body = {
            "modifyVnfInfoData": {
                "vnfConfigurableProperties": vnf_configurable_properties,
                "vnfInstanceId": vnf_instance_id
            },
            "updateType": "MODIFY_VNF_INFORMATION"
        }

        return self.client.post(
            path=path,
            data=json.dumps(body),
            params="",
            content_type="application/json"
        )

    def terminate(
            self,
            ns_instance_id: str
    ) -> Dict[str, Any]:
        """
           Terminates a network instance.
        """

        path = "{}/{}/terminate".format(
            SOL_NETWORK_INSTANCE_PATH,
            ns_instance_id
        )
        return self.client.post(
            path=path,
            data="",
            params="",
            content_type="application/json"
        )

    def delete(
            self,
            ns_instance_id: str
    ) -> Dict[str, Any]:
        """
           Deletes a network instance.
        """
        path = "{}/{}".format(
            SOL_NETWORK_INSTANCE_PATH,
            ns_instance_id
        )
        return self.client.delete(
            path=path,
            params=""
        )

    def list(
            self
    ) -> Dict[str, Any]:
        """
           Lists all network instances.
        """
        path = SOL_NETWORK_INSTANCE_PATH
        return self.client.get(
            path=path,
            data="",
            params=""
        )

    def get(
            self,
            ns_instance_id: str
    ) -> Dict[str, Any]:
        """
           Gets the details of a network instance.
        """
        path = "{}/{}".format(
            SOL_NETWORK_INSTANCE_PATH,
            ns_instance_id
        )
        return self.client.get(
            path=path,
            data="",
            params="",
            content_type="application/json",
            return_code=200
        )
