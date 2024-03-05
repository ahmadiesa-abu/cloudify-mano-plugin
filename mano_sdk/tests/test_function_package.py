import logging
from unittest import TestCase, mock

from mano_sdk import function_package as fp


class TestFunctionPackage(TestCase):
    USERNAME = "xxx"
    PASSWORD = "yyy"
    ENDPOINT_URL = "https://test_aws.amazonaws.com"
    REGION = "test-region-2"
    LOGGER = logging.getLogger()
    TAGS = {
        "test": "tag"
    }
    FUNCTION_ID = "fc-034567decf2122745"
    FILE_NAME = "downloaded_file.zip"

    def setUp(self) -> None:
        self.function_package = fp.FunctionPackage(
            endpoint_url=self.ENDPOINT_URL,
            logger=self.LOGGER,
            username=self.USERNAME,
            password=self.PASSWORD

        )

    @mock.patch('mano_sdk.Client.post')
    def test_create(self, post_mock):
        self.function_package.create(tags=self.TAGS)
        post_mock.assert_called_with(
            content_type='application/json',
            data='{"tags": {"test": "tag"}}',
            params='',
            path=fp.SOL_FUNCTION_PACKAGE_PATH
        )

    @mock.patch('mano_sdk.Client.put')
    @mock.patch('builtins.open', mock.mock_open(read_data="data"))
    def test_upload_zip(self, mock_put):
        self.function_package.upload(
            function_id=self.FUNCTION_ID,
            file_name="zip_file.zip"
        )
        mock_put.assert_called_with(
            content_type='application/zip',
            data=mock.ANY,
            params='',
            path="{}/{}/package_content".format(
                fp.SOL_FUNCTION_PACKAGE_PATH,
                self.FUNCTION_ID
            ),
            return_code=202
        )

    @mock.patch('mano_sdk.Client.put')
    @mock.patch('builtins.open', mock.mock_open(read_data="data"))
    def test_upload_plain(self, mock_put):
        self.function_package.upload(
            function_id=self.FUNCTION_ID,
            file_name="plain_text.txt"
        )
        mock_put.assert_called_with(
            content_type='plain/text',
            data=mock.ANY,
            params='',
            path="{}/{}/package_content".format(
                fp.SOL_FUNCTION_PACKAGE_PATH,
                self.FUNCTION_ID
            ),
            return_code=202
        )

    @mock.patch('mano_sdk.Client.patch')
    def test_update(self, mock_patch):
        self.function_package.update(
            package_id=self.FUNCTION_ID,
            operational_state="DISABLED"
        )
        mock_patch.assert_called_with(
            content_type='application/json',
            data='{"operationalState": "DISABLED"}',
            params='',
            path="{}/{}".format(
                fp.SOL_FUNCTION_PACKAGE_PATH,
                self.FUNCTION_ID
            ),
            return_code=200
        )

    @mock.patch('mano_sdk.Client.delete')
    def test_delete(self, mock_delete):
        self.function_package.delete(
            package_id=self.FUNCTION_ID
        )
        mock_delete.assert_called_with(
            params='',
            path="{}/{}".format(
                fp.SOL_FUNCTION_PACKAGE_PATH,
                self.FUNCTION_ID
            )
        )

    @mock.patch('mano_sdk.Client.get')
    def test_list(self, mock_get):
        self.function_package.list()
        mock_get.assert_called_with(
            content_type='application/json',
            data='',
            params='',
            path=fp.SOL_FUNCTION_PACKAGE_PATH,
            return_code=200
        )

    @mock.patch('mano_sdk.Client.get')
    def test_get(self, mock_get):
        self.function_package.get(
            package_id=self.FUNCTION_ID
        )
        mock_get.assert_called_with(
            content_type='application/json',
            data='',
            params='',
            path="{}/{}".format(
                fp.SOL_FUNCTION_PACKAGE_PATH,
                self.FUNCTION_ID
            ),
            return_code=200
        )
