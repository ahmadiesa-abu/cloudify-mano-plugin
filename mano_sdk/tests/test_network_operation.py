import logging
from unittest import TestCase, mock

from mano_sdk import network_operation as no


class TestNetworkOperation(TestCase):
    USERNAME = "xxx"
    PASSWORD = "yyy"
    ENDPOINT_URL = "https://test_aws.amazonaws.com"
    REGION = "test-region-2"
    LOGGER = logging.getLogger()
    OPERATION_ID = "dp-00f03c1129c6c8bf8"
    NETWORK_INSTANCE_ID = "tp-0b85fcbe94a34cc04"

    def setUp(self) -> None:
        self.network_operation = no.NetworkOperation(
            endpoint_url=self.ENDPOINT_URL,
            logger=self.LOGGER,
            username=self.USERNAME,
            password=self.PASSWORD
        )

    def test_get(self):
        with mock.patch('mano_sdk.Client.get') as d:
            self.network_operation.get(
                operation_id=self.OPERATION_ID
            )
            d.assert_called_with(
                content_type='application/json',
                data='',
                params='',
                path="{}/{}".format(
                    no.SOL_NETWORK_OPERATION_PATH,
                    self.OPERATION_ID
                ),
                return_code=200
            )

    def test_list(self):
        with mock.patch('mano_sdk.Client.get') as d:
            self.network_operation.list()
            d.assert_called_with(
                content_type='application/json',
                data='',
                params='',
                path=no.SOL_NETWORK_OPERATION_PATH,
                return_code=200
            )
