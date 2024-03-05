import logging
from unittest import TestCase, mock

from mano_sdk import network_package as np


class TestNetworkPackage(TestCase):
    USERNAME = "xxx"
    PASSWORD = "yyy"
    ENDPOINT_URL = "https://test_aws.amazonaws.com"
    REGION = "test-region-2"
    LOGGER = logging.getLogger()
    TAGS = {
        "test": "tag"
    }
    NSD_ID = "nc-0dc4e4ea1e8c8110c"
    FILE_NAME = "downloaded_file.zip"

    def setUp(self) -> None:
        self.network_package = np.NetworkPackage(
            endpoint_url=self.ENDPOINT_URL,
            logger=self.LOGGER,
            username=self.USERNAME,
            password=self.PASSWORD
        )

    def test_create(self):
        with mock.patch('mano_sdk.Client.post') as d:
            self.network_package.create(
                tags=self.TAGS,
                content_type='application/json'
            )
            d.assert_called_with(
                content_type='application/json',
                data='{"tags": {"test": "tag"}}',
                params='',
                path=np.SOL_NETWORK_PACKAGE_PATH
            )

    @mock.patch('builtins.open', mock.mock_open(read_data="data"))
    def test_upload_zip(self):
        with mock.patch('mano_sdk.Client.put') as d:
            self.network_package.upload(
                nsd_id=self.NSD_ID,
                file_name="zip_file.zip"
            )
            d.assert_called_with(
                content_type='application/zip',
                data=mock.ANY,
                params='',
                path="{}/{}/nsd_content".format(
                    np.SOL_NETWORK_PACKAGE_PATH,
                    self.NSD_ID
                ),
                return_code=200
            )

    @mock.patch('builtins.open', mock.mock_open(read_data="data"))
    def test_upload_plain(self):
        with mock.patch('mano_sdk.Client.put') as d:
            self.network_package.upload(
                nsd_id=self.NSD_ID,
                file_name="plain_text.txt"
            )
            d.assert_called_with(
                content_type='plain/text',
                data=mock.ANY,
                params='',
                path="{}/{}/nsd_content".format(
                    np.SOL_NETWORK_PACKAGE_PATH,
                    self.NSD_ID
                ),
                return_code=200
            )

    def test_update(self):
        with mock.patch('mano_sdk.Client.patch') as d:
            self.network_package.update(
                nsd_id=self.NSD_ID,
                operational_state="DISABLED"
            )
            d.assert_called_with(
                content_type='application/json',
                data='{"nsdOperationalState": "DISABLED"}',
                params='',
                path="{}/{}".format(
                    np.SOL_NETWORK_PACKAGE_PATH,
                    self.NSD_ID
                ),
                return_code=200
            )

    def test_delete(self):
        with mock.patch('mano_sdk.Client.delete') as d:
            self.network_package.delete(
                nsd_id=self.NSD_ID
            )
            d.assert_called_with(
                params='',
                path="{}/{}".format(
                    np.SOL_NETWORK_PACKAGE_PATH,
                    self.NSD_ID
                )
            )

    def test_list(self):
        with mock.patch('mano_sdk.Client.get') as d:
            self.network_package.list()
            d.assert_called_with(
                content_type='application/json',
                data='',
                params='',
                path=np.SOL_NETWORK_PACKAGE_PATH,
                return_code=200
            )

    def test_get(self):
        with mock.patch('mano_sdk.Client.get') as d:
            self.network_package.get(
                nsd_id=self.NSD_ID
            )
            d.assert_called_with(
                content_type='application/json',
                data='',
                params='',
                path="{}/{}".format(
                    np.SOL_NETWORK_PACKAGE_PATH,
                    self.NSD_ID
                ),
                return_code=200
            )
