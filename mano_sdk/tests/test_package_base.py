import logging
from unittest import TestCase

from mano_sdk.package_base import PackageBaseClass


class TestPackageBase(TestCase):
    USERNAME = "xxx"
    PASSWORD = "yyy"
    ENDPOINT_URL = "https://test_aws.amazonaws.com"
    REGION = "test-region-2"
    LOGGER = logging.getLogger()

    def setUp(self):
        super(TestPackageBase, self).setUp()
        self.base = PackageBaseClass(
            endpoint_url=self.ENDPOINT_URL,
            logger=self.LOGGER,
            username=self.USERNAME,
            password=self.PASSWORD
        )

    def test_create(self):
        with self.assertRaises(NotImplementedError):
            self.base.create("", "")

    def test_get(self):
        with self.assertRaises(NotImplementedError):
            self.base.get("")

    def test_list(self):
        with self.assertRaises(NotImplementedError):
            self.base.list()

    def test_update(self):
        with self.assertRaises(NotImplementedError):
            self.base.update("", "")

    def test_upload(self):
        with self.assertRaises(NotImplementedError):
            self.base.upload("", "")

    def test_delete(self):
        with self.assertRaises(NotImplementedError):
            self.base.delete("")
