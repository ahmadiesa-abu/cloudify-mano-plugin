import logging
import os
from unittest import TestCase, mock

import requests_mock
from cloudify.exceptions import NonRecoverableError

from mano_sdk import client as client


class TestClient(TestCase):

    USERNAME = "xxx"
    PASSWORD = "yyy"
    TOKEN = "zzz"
    ENDPOINT_URL = "https://test_aws.amazonaws.com"
    REGION = "test-region-2"
    LOGGER = logging.getLogger()

    def setUp(self) -> None:
        self.cred = client.Credentials(
            username=self.USERNAME,
            password=self.PASSWORD
        )
        self.client = client.Client(
            credentials=self.cred,
            endpoint_url=self.ENDPOINT_URL,
            logger=self.LOGGER
        )

    def test_no_credentials(self):
        self.cred = client.Credentials()
        self.client = client.Client(
            credentials=self.cred,
            endpoint_url=self.ENDPOINT_URL,
            logger=self.LOGGER
        )

        with mock.patch(
                'requests.request',
                mock.MagicMock(status_code=200)
        ):
            with self.assertRaises(NonRecoverableError):
                self.client.get('/path', {}, {})

    def test_token(self):
        self.cred = client.Credentials(
            token=self.TOKEN
        )
        self.client = client.Client(
            credentials=self.cred,
            endpoint_url=self.ENDPOINT_URL,
            logger=self.LOGGER
        )

        with mock.patch(
                'requests.request',
                mock.MagicMock(status_code=200)
        ):
            self.client.get('/path', {}, {})

    def test_get(self):
        with mock.patch(
                'requests.request',
                mock.MagicMock(status_code=200)
        ):
            self.client.get('/path', {}, {})

    def test_post(self):
        with mock.patch(
                'requests.request',
                mock.MagicMock(status_code=200)
        ):
            self.client.post('/path', {}, {})

    def test_patch(self):
        with mock.patch(
                'requests.request',
                mock.MagicMock(status_code=200)
        ):
            self.client.patch('/path', {}, {}, 'application/zip')

    def test_put(self):
        with mock.patch(
                'requests.request',
                mock.MagicMock(status_code=200)
        ):
            self.client.put('/path', {}, {})

    def test_delete(self):
        with mock.patch(
                'requests.request',
                mock.MagicMock(status_code=200)
        ):
            self.client.delete('/path', {})

    def test_parse_xml_response(self):
        with requests_mock.Mocker() as m:
            test_data_path = os.path.join(
                os.path.dirname(__file__),
                "testdata/response.xml"
            )
            with open(test_data_path) as f:
                m.register_uri(
                    'GET',
                    self.ENDPOINT_URL,
                    text=f.read(),
                    headers={"Content-Type": "text/xml"}
                )
                self.client.get('', {}, {})

    def test_empty_response_code(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'GET',
                self.ENDPOINT_URL,
                status_code=204
            )
            self.assertIsNone(self.client.get('', {}, {}))
