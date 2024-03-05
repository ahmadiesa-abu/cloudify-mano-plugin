import copy
import logging
from unittest import TestCase, mock

from cloudify.exceptions import NonRecoverableError, OperationRetry
from cloudify.manager import DirtyTrackingDict
from cloudify.mocks import MockCloudifyContext
from cloudify.state import current_ctx

import mano_plugin.tasks as tasks


class TestTasks(TestCase):
    USERNAME = "xxx"
    PASSWORD = "yyy"
    ENDPOINT_URL = "https://test_aws.amazonaws.com"
    REGION = "test-region-2"
    LOGGER = logging.getLogger()
    TAGS = {
        "test": "tag"
    }
    FILE_NAME = "downloaded_file.zip"
    FUNCTION_ID = "fc-034567decf2122745"
    NSD_ID = "nc-0dc4e4ea1e8c8110c"
    OPERATION_ID = "dp-00f03c1129c6c8bf8"
    NETWORK_INSTANCE_ID = "tp-07aa863e53460a2a6"
    CLIENT_CONFIG = {
        "username": USERNAME,
        "password": PASSWORD,
        "endpoint_url": ENDPOINT_URL,
        "token": ""
    }
    VFN_PACKAGE_TH = [
        'cloudify.nodes.Root',
        'cloudify.aws.etsi.sol.Package',
        'cloudify.aws.etsi.sol.VFNPackage'
    ]

    NSD_PACKAGE_TH = [
        'cloudify.nodes.Root',
        'cloudify.aws.etsi.sol.Package',
        'cloudify.aws.etsi.sol.NSDPackage'
    ]

    NODE_PROPERTIES = {
        'tags': TAGS,
        'client_config': CLIENT_CONFIG,
        'file': FILE_NAME
    }

    NETWORK_INSTANCE_TH = [
        'cloudify.nodes.Root',
        'cloudify.mano.etsi.sol.NSInstance'
    ]

    DEFAULT_RUNTIME_PROPERTIES = {
        'resource_config': {},
    }

    GET_RESPONSE_VFN = {
        "additionalArtifacts": [
            {
                "artifactPath": "vfnd.yaml"
            }
        ],
        "id": "fc-082919ba5a9165f8f",
        "metadata": {
            "createdAt": "2023-01-10T10:30:08Z",
            "lastModified": "2023-01-10T10:30:22Z",
            "vfnd": {
                "overrides": None
            }
        },
        "onboardingState": "ONBOARDED",
        "operationalState": "ENABLED",
        "tags": {
            "tags": "vfn"
        },
        "usageState": "NOT_IN_USE",
        "vnfProductName": "testVnf",
        "vnfProvider": "test",
        "vnfdId": "afe540fa-5a0c-458f-853a-15f2d73c4906",
        "vnfdVersion": "1.0.0"
    }

    GET_RESPONSE_NSD = {
        "artifacts": [
            {
                "artifactPath": "nsd.yaml"
            }
        ],
        "id": "nc-0dc4e4ea1e8c8110c",
        "metadata": {
            "createdAt": "2023-01-11T07:16:22Z",
            "lastModified": "2023-01-11T07:16:29Z",
            "nsd": {
                "overrides": [
                    {
                        "defaultValue": "10.100.0.0/16",
                        "name": "vpc_cidr_block"
                    }
                ]
            }
        },
        "nsdDesigner": None,
        "nsdId": "6feb8897-603c-4399-9698-46cd6a1bcc82",
        "nsdInvariantId": None,
        "nsdName": "Network Service with Overrides",
        "nsdOnboardingState": "ONBOARDED",
        "nsdOperationalState": "ENABLED",
        "nsdUsageState": "NOT_IN_USE",
        "nsdVersion": "1.0.0",
        "tags": {
            "tag": "tag"
        },
        "vnfPkgIds": [
            "fc-01b408bae7c8efae3"
        ]
    }

    OPERATION_RESPONSE = {
        "nsLcmOpOccId": "dp-00f03c1129c6c8bf8"
    }

    GET_NETWORK_INSTANCE_RESPONSE = {
        "id": "tp-07aa863e53460a2a6",
        "nsInstanceName": "LAX Instance",
        "nsInstanceDescription": "Network service for LAX",
        "nsdId": "6625a858-2157-4d74-9197-a6ff67d51f3e",
        "nsdInfoId": "nc-07aa863e53460a2a6",
        "nsState": "INSTANTIATED",
        "vnfInstance": [
            {
                "id": "fn-b9439c34c1ef86c54",
                "vnfPkgId": "fc-07aa863e53460a2a6",
                "instantiationState": "INSTANTIATED",
                "instantiatedVnfInfo": {
                    "vnfState": "STARTED"
                }
            }
        ],
        "metadata": {
            "createdAt": "2022-06-10T19:48:33",
            "lastModified": "2022-06-10T19:48:33"
        },
        "lcmOpInfo": {
            "nsLcmOpOccId": "dp-00f03c1129c6c8bf8"
        }
    }

    CREATE_RESPONSE_VFN = {
        "id": "fc-034567decf2122745",
        "onboardingState": "CREATED",
        "operationalState": "DISABLED",
        "usageState": "NOT_IN_USE"
    }

    CREATE_RESPONSE_NSD = {
        "id": "nc-0dc4e4ea1e8c8110c",
        "onboardingState": "CREATED",
        "operationalState": "DISABLED",
        "usageState": "NOT_IN_USE"
    }

    CREATE_RESPONSE_NS_INSTANCE = {
        "id": "tp-07aa863e53460a2a6",
        "nsdId": "6a792d0c-be2a-45fa-989e-5f89d94ca585",
        "nsInstanceName": "SampleNs"
    }

    RUNTIME_PROPERTIES_AFTER_CREATE_NSD = {
        'id': 'nc-0dc4e4ea1e8c8110c',
        'nsd_id': '6feb8897-603c-4399-9698-46cd6a1bcc82',
        'resource_config': GET_RESPONSE_NSD
    }

    RUNTIME_PROPERTIES_AFTER_CREATE_VFN = {
        'function_package_id': 'fc-034567decf2122745',
        'resource_config': GET_RESPONSE_VFN
    }

    RUNTIME_PROPERTIES_NS_INSTANCE = {
        'resource_config': GET_NETWORK_INSTANCE_RESPONSE,
        'ns_instance_id': "tp-07aa863e53460a2a6",
        'operation_id': "dp-00f03c1129c6c8bf8"
    }

    RUNTIME_PROPERTIES_OPERATION = {
        'resource_config': {},
        'operation_id': "dp-00f03c1129c6c8bf8"
    }

    GET_COMPLETED_OPERATION_RESPONSE = {
        "lcmOperationType": "INSTANTIATE",
        "nsInstanceId": "tp-07aa863e53460a2a6",
        "operationState": "COMPLETED"
    }

    GET_PROCESSING_OPERATION_RESPONSE = {
        "id": "dp-00f03c1129c6c8bf8",
        "lcmOperationType": "INSTANTIATE",
        "nsInstanceId": "tp-07aa863e53460a2a6",
        "operationState": "PROCESSING",
    }

    GET_FAILED_OPERATION_RESPONSE = {
        "error": "Lost connection to the host",
        "id": "dp-00f03c1129c6c8bf8",
        "lcmOperationType": "INSTANTIATE",
        "nsInstanceId": "tp-07aa863e53460a2a6",
        "operationState": "FAILED",
    }

    def _to_DirtyTrackingDict(self, origin):
        if not origin:
            origin = {}
        dirty_dict = DirtyTrackingDict(origin)
        for k in origin:
            dirty_dict[k] = copy.deepcopy(origin[k])
        return dirty_dict

    def get_mock_ctx(
            self,
            test_name,
            test_properties=None,
            test_runtime_properties=None,
            test_relationships=None,
            type_hierarchy=None,
            type_node=None,
            ctx_operation_name=None,
            test_resources=None
    ):
        type_node = type_node or 'cloudify.nodes.Root'
        operation_ctx = {
            'retry_number': 0,
            'name': 'cloudify.interfaces.lifecycle.configure'
        } if not ctx_operation_name else {
            'retry_number': 0, 'name': ctx_operation_name
        }
        test_properties = test_properties or {
            'client_config': {
                'region_name': 'us-foobar-1'
            }
        }
        test_runtime_properties = test_runtime_properties or {}
        ctx = MockCloudifyContext(
            node_id=test_name,
            node_name=test_name,
            deployment_id=test_name,
            properties=copy.deepcopy(test_properties),
            runtime_properties=self._to_DirtyTrackingDict(
                copy.deepcopy(test_runtime_properties)),
            relationships=test_relationships,
            operation=operation_ctx,
            resources=test_resources
        )
        ctx.node._type = type_node
        ctx.node.type_hierarchy = type_hierarchy or ['cloudify.nodes.Root']
        ctx.instance.refresh = mock.MagicMock()
        return ctx

    @mock.patch(
        'mano_sdk.function_package.'
        'FunctionPackage.get'
    )
    @mock.patch(
        'mano_sdk.function_package.'
        'FunctionPackage.create'
    )
    def test_create_vfn(self, mock_create, mock_get):
        _ctx = self.get_mock_ctx(
            'test_create',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.DEFAULT_RUNTIME_PROPERTIES,
            type_hierarchy=self.VFN_PACKAGE_TH
        )

        current_ctx.set(_ctx)
        mock_create.return_value = self.CREATE_RESPONSE_VFN
        mock_get.return_value = self.GET_RESPONSE_VFN
        tasks.create_vfn(_ctx, self.CLIENT_CONFIG, self.TAGS)
        mock_create.assert_called_with(
            self.TAGS,
            'application/json'
        )
        self.assertEqual(
            _ctx.instance.runtime_properties['function_package_id'],
            "fc-034567decf2122745"
        )
        self.assertEqual(
            _ctx.instance.runtime_properties['resource_config'],
            self.GET_RESPONSE_VFN
        )

    @mock.patch(
        'mano_sdk.function_package.'
        'FunctionPackage.get'
    )
    @mock.patch(
        'mano_sdk.function_package.'
        'FunctionPackage.upload'
    )
    def test_upload_vfn(self, mock_upload, mock_get):
        _ctx = self.get_mock_ctx(
            'test_upload',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.RUNTIME_PROPERTIES_AFTER_CREATE_VFN,
            type_hierarchy=self.VFN_PACKAGE_TH,
            test_resources=self.FILE_NAME
        )
        _ctx.download_resource = mock.MagicMock(return_value=self.FILE_NAME)
        current_ctx.set(_ctx)
        mock_get.return_value = self.GET_RESPONSE_VFN
        tasks.upload_vfn(_ctx, self.CLIENT_CONFIG, self.FILE_NAME)
        mock_upload.assert_called_with(
            file_name=self.FILE_NAME,
            function_id=self.FUNCTION_ID
        )

    @mock.patch(
        'mano_sdk.function_package.'
        'FunctionPackage.get'
    )
    @mock.patch(
        'mano_sdk.function_package.'
        'FunctionPackage.update'
    )
    def test_update_vfn(self, mock_update, mock_get):
        _ctx = self.get_mock_ctx(
            'test_update',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.RUNTIME_PROPERTIES_AFTER_CREATE_VFN,
            type_hierarchy=self.VFN_PACKAGE_TH
        )

        current_ctx.set(_ctx)
        mock_update.return_value = self.CREATE_RESPONSE_VFN
        mock_get.return_value = self.GET_RESPONSE_VFN
        tasks.update_vfn_state(
            ctx=_ctx,
            client_config=self.CLIENT_CONFIG,
            operational_state="DISABLED"
        )
        mock_update.assert_called_with(
            operational_state="DISABLED",
            package_id=self.FUNCTION_ID
        )

    @mock.patch(
        'mano_sdk.function_package.'
        'FunctionPackage.delete'
    )
    def test_delete_vfn(self, mock_delete):
        _ctx = self.get_mock_ctx(
            'test_create',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.RUNTIME_PROPERTIES_AFTER_CREATE_VFN,
            type_hierarchy=self.VFN_PACKAGE_TH
        )

        current_ctx.set(_ctx)
        tasks.delete_vfn(
            ctx=_ctx,
            client_config=self.CLIENT_CONFIG
        )
        mock_delete.assert_called_with(
            package_id=self.FUNCTION_ID
        )

    def test_create_nsd(self):
        _ctx = self.get_mock_ctx(
            'test_create',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.DEFAULT_RUNTIME_PROPERTIES,
            type_hierarchy=self.NSD_PACKAGE_TH
        )

        current_ctx.set(_ctx)

        with mock.patch(
                'mano_sdk.network_package.'
                'NetworkPackage.get') as c:
            with mock.patch(
                    'mano_sdk.network_package.'
                    'NetworkPackage.create') as d:
                d.return_value = self.CREATE_RESPONSE_NSD
                c.return_value = self.GET_RESPONSE_NSD
                tasks.create_nsd(_ctx, self.CLIENT_CONFIG, self.TAGS)
                d.assert_called_with(
                    self.TAGS,
                    'application/json'
                )
                self.assertEqual(
                    _ctx.instance.runtime_properties['id'],
                    "nc-0dc4e4ea1e8c8110c"
                )
                self.assertEqual(
                    _ctx.instance.runtime_properties['resource_config'],
                    self.GET_RESPONSE_NSD
                )

    def test_upload_nsd(self):
        _ctx = self.get_mock_ctx(
            'test_upload',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.RUNTIME_PROPERTIES_AFTER_CREATE_NSD,
            type_hierarchy=self.NSD_PACKAGE_TH,
            test_resources=self.FILE_NAME
        )
        _ctx.download_resource = mock.MagicMock(return_value=self.FILE_NAME)
        current_ctx.set(_ctx)
        with mock.patch(
                'mano_sdk.network_package.'
                'NetworkPackage.get') as c:
            with mock.patch(
                    'mano_sdk.network_package.'
                    'NetworkPackage.upload') as d:
                c.return_value = self.GET_RESPONSE_NSD
                tasks.upload_nsd(_ctx, self.CLIENT_CONFIG, self.FILE_NAME)
                d.assert_called_with(
                    file_name=self.FILE_NAME,
                    nsd_id=self.NSD_ID
                )

    def test_update_nsd(self):
        _ctx = self.get_mock_ctx(
            'test_update',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.RUNTIME_PROPERTIES_AFTER_CREATE_NSD,
            type_hierarchy=self.NSD_PACKAGE_TH
        )

        current_ctx.set(_ctx)
        with mock.patch(
                'mano_sdk.network_package.'
                'NetworkPackage.get') as c:
            with mock.patch(
                    'mano_sdk.network_package.'
                    'NetworkPackage.update') as d:
                d.return_value = self.CREATE_RESPONSE_NSD
                c.return_value = self.GET_RESPONSE_NSD
                tasks.update_nsd_state(
                    ctx=_ctx,
                    client_config=self.CLIENT_CONFIG,
                    operational_state="DISABLED"
                )
                d.assert_called_with(
                    operational_state="DISABLED",
                    nsd_id=self.NSD_ID
                )

    def test_delete_operation(self):
        _ctx = self.get_mock_ctx(
            'test_delete',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.RUNTIME_PROPERTIES_AFTER_CREATE_NSD,
            type_hierarchy=self.NSD_PACKAGE_TH
        )

        current_ctx.set(_ctx)
        with mock.patch(
                'mano_sdk.network_package.'
                'NetworkPackage.delete'
        ) as d:
            tasks.delete_nsd(
                ctx=_ctx,
                client_config=self.CLIENT_CONFIG
            )
            d.assert_called_with(
                nsd_id=self.NSD_ID
            )

    def test_create_ns_instance(self):
        _ctx = self.get_mock_ctx(
            'test_create',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.RUNTIME_PROPERTIES_NS_INSTANCE,
            type_hierarchy=self.NETWORK_INSTANCE_TH
        )
        current_ctx.set(_ctx)
        with mock.patch(
                'mano_sdk.network_instance.'
                'NetworkInstance.get') as c:
            with mock.patch(
                    'mano_sdk.network_instance.'
                    'NetworkInstance.create') as d:
                d.return_value = self.CREATE_RESPONSE_NS_INSTANCE
                c.return_value = self.GET_NETWORK_INSTANCE_RESPONSE
                tasks.create_ns_instance(
                    ctx=_ctx,
                    client_config=self.CLIENT_CONFIG,
                    nsd_id=self.NSD_ID,
                    nsd_name="Simple",
                    ns_description="Sample",
                    tags=self.TAGS
                )
                d.assert_called_with(
                    ns_description='Sample',
                    nsd_id=self.NSD_ID,
                    nsd_name='Simple',
                    tags=self.TAGS
                )
                self.assertEqual(
                    _ctx.instance.runtime_properties['ns_instance_id'],
                    self.NETWORK_INSTANCE_ID
                )
                self.assertEqual(
                    _ctx.instance.runtime_properties['resource_config'],
                    self.GET_NETWORK_INSTANCE_RESPONSE
                )

    def test_instantiate_ns_instance(self):
        _ctx = self.get_mock_ctx(
            'test_instantiate',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.RUNTIME_PROPERTIES_NS_INSTANCE,
            type_hierarchy=self.NETWORK_INSTANCE_TH
        )
        current_ctx.set(_ctx)
        with mock.patch(
                'mano_sdk.network_instance.'
                'NetworkInstance.get') as c:
            with mock.patch(
                    'mano_sdk.network_instance.'
                    'NetworkInstance.instantiate') as d:
                d.return_value = self.OPERATION_RESPONSE
                c.return_value = self.GET_NETWORK_INSTANCE_RESPONSE
                tasks.instantiate_ns_instance(
                    ctx=_ctx,
                    client_config=self.CLIENT_CONFIG,
                    additional_params={
                        "param": "test"
                    },
                    dry_run=False
                )
                d.assert_called_with(
                    additional_params={
                        "param": "test"
                    },
                    dry_run=False,
                    ns_instance_id=self.NETWORK_INSTANCE_ID
                )
                self.assertEqual(
                    _ctx.instance.runtime_properties['operation_id'],
                    self.OPERATION_ID
                )
                self.assertEqual(
                    _ctx.instance.runtime_properties['resource_config'],
                    self.GET_NETWORK_INSTANCE_RESPONSE
                )

    def test_terminate_ns_instance(self):
        _ctx = self.get_mock_ctx(
            'test_terminate',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.RUNTIME_PROPERTIES_NS_INSTANCE,
            type_hierarchy=self.NETWORK_INSTANCE_TH
        )
        current_ctx.set(_ctx)
        with mock.patch(
                'mano_sdk.network_instance.'
                'NetworkInstance.get') as c:
            with mock.patch(
                    'mano_sdk.network_instance.'
                    'NetworkInstance.terminate') as d:
                d.return_value = self.OPERATION_RESPONSE
                c.return_value = self.GET_NETWORK_INSTANCE_RESPONSE
                tasks.terminate_ns_instance(
                    ctx=_ctx,
                    client_config=self.CLIENT_CONFIG,
                )
                d.assert_called_with(
                    ns_instance_id=self.NETWORK_INSTANCE_ID
                )
                self.assertEqual(
                    _ctx.instance.runtime_properties['operation_id'],
                    self.OPERATION_ID
                )
                self.assertEqual(
                    _ctx.instance.runtime_properties['resource_config'],
                    self.GET_NETWORK_INSTANCE_RESPONSE
                )

    def test_delete_ns_instance(self):
        _ctx = self.get_mock_ctx(
            'test_delete',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.RUNTIME_PROPERTIES_NS_INSTANCE,
            type_hierarchy=self.NETWORK_INSTANCE_TH
        )
        current_ctx.set(_ctx)
        with mock.patch(
                'mano_sdk.network_instance.'
                'NetworkInstance.delete') as d:
            d.return_value = self.OPERATION_RESPONSE
            tasks.delete_ns_instance(
                ctx=_ctx,
                client_config=self.CLIENT_CONFIG,
            )
            d.assert_called_with(
                ns_instance_id=self.NETWORK_INSTANCE_ID
            )

    def test_get_completed_operation(self):
        _ctx = self.get_mock_ctx(
            'test_get_operation',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.RUNTIME_PROPERTIES_OPERATION,
            type_hierarchy=self.NETWORK_INSTANCE_TH
        )

        current_ctx.set(_ctx)

        with mock.patch(
                'mano_sdk.network_operation.'
                'NetworkOperation.get') as c:
            with mock.patch(
                    'mano_sdk.network_instance.'
                    'NetworkInstance.get') as d:
                c.return_value = self.GET_COMPLETED_OPERATION_RESPONSE
                d.return_value = self.GET_NETWORK_INSTANCE_RESPONSE
                tasks.get_network_operation(
                    ctx=_ctx,
                    client_config=self.CLIENT_CONFIG
                )
                c.assert_called_with(
                    operation_id=self.OPERATION_ID
                )
                d.assert_called_with(
                    ns_instance_id=self.NETWORK_INSTANCE_ID
                )

    def test_get_failed_operation(self):
        _ctx = self.get_mock_ctx(
            'test_get_operation',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.RUNTIME_PROPERTIES_OPERATION,
            type_hierarchy=self.NETWORK_INSTANCE_TH
        )

        current_ctx.set(_ctx)

        with mock.patch(
                'mano_sdk.network_operation.'
                'NetworkOperation.get') as c:
            with mock.patch(
                    'mano_sdk.network_instance.'
                    'NetworkInstance.get') as d:
                c.return_value = self.GET_FAILED_OPERATION_RESPONSE
                d.return_value = self.GET_NETWORK_INSTANCE_RESPONSE
                with self.assertRaises(NonRecoverableError):
                    tasks.get_network_operation(
                        ctx=_ctx,
                        client_config=self.CLIENT_CONFIG
                    )
                c.assert_called_with(
                    operation_id=self.OPERATION_ID
                )
                d.assert_not_called()

    def test_get_processing_operation(self):
        _ctx = self.get_mock_ctx(
            'test_get_operation',
            test_properties=self.NODE_PROPERTIES,
            test_runtime_properties=self.RUNTIME_PROPERTIES_OPERATION,
            type_hierarchy=self.NETWORK_INSTANCE_TH
        )

        current_ctx.set(_ctx)

        with mock.patch(
                'mano_sdk.network_operation.'
                'NetworkOperation.get') as c:
            with mock.patch(
                    'mano_sdk.network_instance.'
                    'NetworkInstance.get') as d:
                c.return_value = self.GET_PROCESSING_OPERATION_RESPONSE
                d.return_value = self.GET_NETWORK_INSTANCE_RESPONSE
                with self.assertRaises(OperationRetry):
                    tasks.get_network_operation(
                        ctx=_ctx,
                        client_config=self.CLIENT_CONFIG
                    )
                c.assert_called_with(
                    operation_id=self.OPERATION_ID
                )
                d.assert_not_called()
