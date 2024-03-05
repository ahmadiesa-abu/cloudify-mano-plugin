import json
from typing import Any, Dict, Optional

import requests
import xmltodict
from cloudify.exceptions import NonRecoverableError, RecoverableError
from requests.auth import AuthBase, HTTPBasicAuth


class TokenAuth(AuthBase):
    def __init__(self, token, auth_scheme='Bearer'):
        self.token = token
        self.auth_scheme = auth_scheme

    def __call__(self, request):
        request.headers['Authorization'] = f'{self.auth_scheme} {self.token}'
        return request


class Credentials:
    """
    Holds the credentials needed to authenticate requests.

    :param str username: The username part of the credentials.
    :param str password: The password part of the credentials.
    :param str token: The security token, valid only for session credentials.
    """

    def __init__(self, username=None, password=None, token=None):
        self.username = username
        self.password = password
        self.token = token


class Client:
    """
        Client
        ~~~~~~~~~~~~~~
        Client created for sending requests.
    """

    def __init__(
            self,
            credentials: Credentials,
            endpoint_url: str,
            logger: Any
    ):
        self.cred = credentials
        self.url = endpoint_url
        self.logger = logger

    def _make_request(
            self,
            method: str,
            path: str,
            return_code: int,
            params: Optional[Any] = "",
            data: Optional[str] = "",
            content_type: Optional[str] = "application/json"
    ) -> Optional[Dict[str, Any]]:
        request_auth = ""
        headers = {'Content-type': content_type}
        if self.cred.username and self.cred.password:
            request_auth = HTTPBasicAuth(
                self.cred.username,
                self.cred.password
            )
        if self.cred.token:
            request_auth = TokenAuth(
                token=self.cred.token,
                auth_scheme='access_token'
            )
        if not request_auth:
            self.logger.error(
                'No credentials provided for the endpoint: {}'
                .format(repr(self.url))
            )
            raise NonRecoverableError(
                'Token or user/password not provided.'
            )
        try:
            response = requests.request(
                auth=request_auth,
                method=method,
                url=self.url + path,
                headers=headers,
                params=params,
                data=data
            )
        except requests.exceptions.ConnectionError as e:
            self.logger.error(
                'ConnectionError for endpoint: {}'
                .format(repr(self.url))
            )
            raise RecoverableError(e)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise NonRecoverableError(
                'HTTPError occurred {}. Reason: {}'.format(e, response.text)
            )
        if response.status_code == requests.codes.no_content:
            return None
        if response.status_code != return_code:
            self.logger.warn(
                'Status_code {} different than expected {}'.format(
                    response.status_code,
                    return_code
                )
            )
        else:
            self.logger.debug(
                'Response code {} defined as successful.'
                .format(response.status_code)
            )

        parsed_response = self._parse_response(
            response=response,
            logger=self.logger
        )
        return parsed_response

    def get(
            self,
            path: str,
            data: Optional[str],
            params: Optional[Any] = "",
            content_type: str = "application/json",
            return_code: int = 200
    ) -> Optional[Dict[str, Any]]:
        """
            Sends `GET` request.
        """
        return self._make_request(
            method="GET",
            path=path,
            return_code=return_code,
            params=params,
            data=data,
            content_type=content_type
        )

    def post(
            self,
            path: str,
            data: Optional[str] = "",
            params: Optional[Any] = "",
            content_type: str = "application/json",
            return_code: int = 201
    ) -> Optional[Dict[str, Any]]:
        """
            Sends `POST` request.
        """
        return self._make_request(
            method="POST",
            path=path,
            return_code=return_code,
            params=params,
            data=data,
            content_type=content_type
        )

    def put(
            self,
            path: str,
            data: str = "",
            params: Optional[Any] = "",
            content_type: str = "application/zip",
            return_code: int = 204
    ) -> Optional[Dict[str, Any]]:
        """
            Sends `PUT` request.
        """
        return self._make_request(
            method="PUT",
            path=path,
            return_code=return_code,
            params=params,
            data=data,
            content_type=content_type
        )

    def patch(
            self,
            path: str,
            data: str = "",
            params: Optional[Any] = "",
            content_type: str = "application/json",
            return_code: int = 200
    ) -> Optional[Dict[str, Any]]:
        """
            Sends `PATCH` request.
        """
        return self._make_request(
            method="PATCH",
            path=path,
            return_code=return_code,
            params=params,
            data=data,
            content_type=content_type
        )

    def delete(
            self,
            path: str,
            params: Optional[Any] = "",
            return_code: int = 204
    ) -> Optional[Dict[str, Any]]:
        """
            Sends `DELETE` request.
        """
        return self._make_request(
            method="DELETE",
            path=path,
            return_code=return_code,
            params=params,
            data="",
            content_type=""
        )

    @staticmethod
    def _parse_response(
            response: requests.Response,
            logger: Any
    ) -> Optional[Dict[str, Any]]:
        """
            Parses received xml or json response.
        """
        json_response = {}
        if response.headers.get('Content-Type'):
            response_content_type = response.headers['Content-Type'].lower()
            if (
                response_content_type.startswith("application/json") or
                response_content_type.startswith("text/json")
            ):
                json_response = response.json()
            elif (
                response_content_type.startswith('text/xml') or
                response_content_type.startswith('application/xml')
            ):
                json_response = json.loads(
                    json.dumps(xmltodict.parse(response.text))
                )
                logger.debug('XML response transformed to dict.')
        return json_response
