import json
import logging
from unittest import TestCase, mock

from mano_sdk import network_instance as ni


class TestNetworkInstance(TestCase):
    USERNAME = "xxx"
    PASSWORD = "yyy"
    ENDPOINT_URL = "https://test_aws.amazonaws.com"
    REGION = "test-region-2"
    LOGGER = logging.getLogger()
    OPERATION_ID = "dp-0d5b823eb5c2a9241"
    NETWORK_INSTANCE_ID = "tp-07aa863e53460a2a6"
    NSD_ID = "nc-0dc4e4ea1e8c8110c"
    VNF_ID = "fn-0c2412bf340c67ec0"
    TAGS = {
        "test": "tag"
    }

    def setUp(self) -> None:
        self.network_instance = ni.NetworkInstance(
            endpoint_url=self.ENDPOINT_URL,
            logger=self.LOGGER,
            username=self.USERNAME,
            password=self.PASSWORD
        )

    def test_create(self):
        with mock.patch('mano_sdk.Client.post') as d:
            self.network_instance.create(
                nsd_id="6feb8897-603c-4399-9698-46cd6a1bcc82",
                nsd_name="Simple",
                ns_description="Sample",
                tags=self.TAGS,
                content_type="application/json"
            )
            data = {
                "nsdId": "6feb8897-603c-4399-9698-46cd6a1bcc82",
                "nsName": "Simple",
                "nsDescription": "Sample",
                "tags": {
                    "test": "tag"
                }
            }
            d.assert_called_with(
                content_type='application/json',
                data=json.dumps(data),
                params='',
                path=ni.SOL_NETWORK_INSTANCE_PATH
            )

    def test_instantiate_additional_params(self):
        with mock.patch('mano_sdk.Client.post') as d:
            self.network_instance.instantiate(
                ns_instance_id=self.NSD_ID,
                additional_params={"param": "test"},
                dry_run=False
            )
            data = {
                "additionalParamsForNs": {
                    "param": "test"
                }
            }
            d.assert_called_with(
                content_type='application/json',
                data=json.dumps(data),
                params={'dryRun': False},
                path='{}/{}/instantiate'.format(
                    ni.SOL_NETWORK_INSTANCE_PATH,
                    self.NSD_ID
                )
            )

    def test_instantiate_no_additional_params(self):
        with mock.patch('mano_sdk.Client.post') as d:
            self.network_instance.instantiate(
                ns_instance_id=self.NSD_ID,
                additional_params={},
                dry_run=False
            )
            d.assert_called_with(
                content_type='application/json',
                data="",
                params={'dryRun': False},
                path='{}/{}/instantiate'.format(
                    ni.SOL_NETWORK_INSTANCE_PATH,
                    self.NSD_ID
                )
            )

    def test_update(self):
        with mock.patch('mano_sdk.Client.post') as d:
            body = {
                "modifyVnfInfoData": {
                    "vnfConfigurableProperties": {
                        "param": "test"
                    },
                    "vnfInstanceId": self.VNF_ID
                },
                "updateType": "MODIFY_VNF_INFORMATION"
            }
            self.network_instance.update(
                ns_instance_id=self.NSD_ID,
                vnf_instance_id=self.VNF_ID,
                vnf_configurable_properties={
                        "param": "test"
                    }
            )
            d.assert_called_with(
                content_type='application/json',
                data=json.dumps(body),
                params="",
                path='{}/{}/update'.format(
                    ni.SOL_NETWORK_INSTANCE_PATH,
                    self.NSD_ID
                )
            )

    def test_terminate(self):
        with mock.patch('mano_sdk.Client.post') as d:
            self.network_instance.terminate(
                ns_instance_id=self.NSD_ID
            )
            d.assert_called_with(
                content_type='application/json',
                data="",
                params="",
                path='{}/{}/terminate'.format(
                    ni.SOL_NETWORK_INSTANCE_PATH,
                    self.NSD_ID
                )
            )

    def test_delete(self):
        with mock.patch('mano_sdk.Client.delete') as d:
            self.network_instance.delete(
                ns_instance_id=self.NSD_ID
            )
            d.assert_called_with(
                params="",
                path='{}/{}'.format(
                    ni.SOL_NETWORK_INSTANCE_PATH,
                    self.NSD_ID
                )
            )

    def test_get(self):
        with mock.patch('mano_sdk.Client.get') as d:
            self.network_instance.get(
                ns_instance_id=self.NSD_ID
            )
            d.assert_called_with(
                content_type='application/json',
                data="",
                params="",
                path='{}/{}'.format(
                    ni.SOL_NETWORK_INSTANCE_PATH,
                    self.NSD_ID
                ),
                return_code=200
            )

    def test_list(self):
        with mock.patch('mano_sdk.Client.get') as d:
            self.network_instance.list()
            d.assert_called_with(
                data="",
                params="",
                path=ni.SOL_NETWORK_INSTANCE_PATH
            )
