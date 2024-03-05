"""
    mano_sdk.function_package
    ~~~~~~~~
   ETSI SOL Network Service Descriptor interface.
"""
import json
import os
from typing import Any, Dict, Optional

from mano_sdk.package_base import PackageBaseClass

SOL_NETWORK_PACKAGE_PATH = "/sol/nsd/v1/ns_descriptors"


class NetworkPackage(PackageBaseClass):
    """
        ETSI SOL Network Service Descriptor interface.
    """

    def create(
            self,
            tags: Optional[Dict[str, str]],
            content_type: str
    ) -> Dict[str, Any]:
        """
            Creates an initial network package (NSD).
        """
        path = SOL_NETWORK_PACKAGE_PATH
        json_data = ""
        if tags:
            data = ({
                "tags": tags
            })
            json_data = json.dumps(data)
        return self.client.post(
            path=path,
            data=json_data,
            params="",
            content_type=content_type
        )

    def upload(
            self,
            nsd_id: str,
            file_name: str
    ) -> Dict[str, Any]:
        """
            Uploads network package (NSD) content using `nsd_id`.
        """
        script_dir = os.path.dirname(__file__)
        rel_path = file_name
        file_path = os.path.join(script_dir, rel_path)
        if file_name.endswith(".zip"):
            content_type = "application/zip"
        else:
            content_type = "plain/text"
        path = SOL_NETWORK_PACKAGE_PATH + "/" + nsd_id + "/nsd_content"
        with open(file_path, 'rb') as data:
            return self.client.put(
                path=path,
                data=data,
                params="",
                content_type=content_type,
                return_code=200
            )

    def update(
            self,
            nsd_id: str,
            operational_state: str
    ) -> Dict[str, Any]:
        """
            Updates `operational state` of network package (NSD).
        """
        path = "{}/{}".format(
            SOL_NETWORK_PACKAGE_PATH,
            nsd_id
        )
        data = {
            "nsdOperationalState": operational_state
        }
        return self.client.patch(
            path=path,
            data=json.dumps(data),
            params="",
            content_type="application/json",
            return_code=200
        )

    def delete(
            self,
            nsd_id: str
    ) -> Dict[str, Any]:
        """
            Deletes network package (NSD).
        """
        path = "{}/{}".format(
            SOL_NETWORK_PACKAGE_PATH,
            nsd_id
        )
        return self.client.delete(
            path=path,
            params=""
        )

    def list(
            self
    ) -> Dict[str, Any]:
        """
            Lists all network packages (NSDs).
        """
        path = SOL_NETWORK_PACKAGE_PATH
        return self.client.get(
            path=path,
            data="",
            params="",
            content_type="application/json",
            return_code=200
        )

    def get(
            self,
            nsd_id: str
    ) -> Dict[str, Any]:
        """
            Gets the details of network package (NSD).
        """
        path = "{}/{}".format(
            SOL_NETWORK_PACKAGE_PATH,
            nsd_id
        )
        return self.client.get(
            path=path,
            data="",
            params="",
            content_type="application/json",
            return_code=200
        )
