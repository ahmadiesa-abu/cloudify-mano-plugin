"""
    mano_sdk.function_package
    ~~~~~~~~
    ETSI SOL Virtual Network Function interface.
"""
import json
import os
from typing import Any, Dict, Optional

from mano_sdk.package_base import PackageBaseClass

SOL_FUNCTION_PACKAGE_PATH = "/sol/vnfpkgm/v1/vnf_packages"


class FunctionPackage(PackageBaseClass):
    """
        ETSI SOL Virtual Network Function interface
    """

    def create(
            self,
            tags: Optional[Dict[str, str]] = None,
            content_type: str = "application/json"
    ) -> Dict[str, Any]:
        """
            Creates an initial function package (VNF).
        """
        path = SOL_FUNCTION_PACKAGE_PATH
        data = {}
        if tags:
            data.update({
                "tags": tags
            })
        json_data = json.dumps(data) if data else ""
        return self.client.post(
            path=path,
            data=json_data,
            params="",
            content_type=content_type
        )

    def upload(
            self,
            function_id: str,
            file_name: str
    ) -> Dict[str, Any]:
        """
            Uploads function package content using `function_id`.
        """
        script_dir = os.path.dirname(__file__)
        rel_path = file_name
        file_path = os.path.join(script_dir, rel_path)
        if file_name.endswith(".zip"):
            content_type = "application/zip"
        else:
            content_type = "plain/text"
        path = "{}/{}/package_content".format(
            SOL_FUNCTION_PACKAGE_PATH,
            function_id
        )
        with open(file_path, 'rb') as data:
            return self.client.put(
                path=path,
                data=data,
                params="",
                content_type=content_type,
                return_code=202
            )

    def update(
            self,
            package_id: str,
            operational_state: str
    ) -> Dict[str, Any]:
        """
            Updates `operational state` of function package (VNF).
        """
        path = "{}/{}".format(
            SOL_FUNCTION_PACKAGE_PATH,
            package_id
        )
        data = {
            "operationalState": operational_state
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
            package_id: str
    ) -> Dict[str, Any]:
        """
            Deletes function package (VNF).
        """
        path = "{}/{}".format(
            SOL_FUNCTION_PACKAGE_PATH,
            package_id
        )
        return self.client.delete(
            path=path,
            params=""
        )

    def list(
            self
    ) -> Dict[str, Any]:
        """
            Lists all function packages (VNFs).
        """
        path = SOL_FUNCTION_PACKAGE_PATH
        return self.client.get(
            path=path,
            data="",
            params="",
            content_type="application/json",
            return_code=200
        )

    def get(
            self,
            package_id: str
    ) -> Dict[str, Any]:
        """
            Gets the details of function package (VFN).
        """
        path = "{}/{}".format(
            SOL_FUNCTION_PACKAGE_PATH,
            package_id
        )
        return self.client.get(
            path=path,
            data="",
            params="",
            content_type="application/json",
            return_code=200
        )
