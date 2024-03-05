from .client import Client, Credentials


class PackageBaseClass:

    def __init__(
            self,
            endpoint_url,
            logger,
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

    def create(self, tags, content_type):
        """Creates a resource."""
        raise NotImplementedError()

    def upload(self, package_id, file_name):
        """Uploads to a resource."""
        raise NotImplementedError()

    def update(self, package_id, operational_state):
        """Updates a resource."""
        raise NotImplementedError()

    def delete(self, package_id):
        """Deletes a resource."""
        raise NotImplementedError()

    def list(self):
        """Lists mano_sdk."""
        raise NotImplementedError()

    def get(self, package_id):
        """Gets a resource."""
        raise NotImplementedError()
