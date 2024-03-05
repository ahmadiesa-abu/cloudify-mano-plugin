from os.path import exists as path_exists
from typing import Dict

from cloudify.context import CloudifyContext
from cloudify.decorators import operation
from cloudify.exceptions import NonRecoverableError, OperationRetry

from mano_sdk.function_package import FunctionPackage
from mano_sdk.network_instance import NetworkInstance
from mano_sdk.network_operation import NetworkOperation
from mano_sdk.network_package import NetworkPackage

OPERATION_RETRY_STATES = [
    "PROCESSING",
    "PARTIALLY_COMPLETED",
    "ROLLING_BACK"
]
OPERATION_NON_RECOVERABLE_STATES = [
    "FAILED_TEMP",
    "FAILED",
    "ROLLED_BACK",
    "CANCELLED",
    "UNKNOWN"
]


@operation
def create_vfn(
        ctx: CloudifyContext,
        client_config: Dict[str, str],
        tags: Dict[str, str]
) -> None:
    """
        Creates an initial function package (VNF).
    """
    function_package = FunctionPackage(
        client_config['endpoint_url'],
        ctx.logger,
        client_config['username'],
        client_config['password'],
        client_config['token']
    )
    response = function_package.create(tags, "application/json")
    ctx.instance.runtime_properties['function_package_id'] = response['id']
    ctx.instance.runtime_properties['resource_config'] = function_package.get(
        response['id']
    )


@operation
def upload_vfn(
        ctx: CloudifyContext,
        client_config: Dict[str, str],
        file: str
) -> None:
    """
        Uploads function package content using `function_id`.
    """
    function_package = FunctionPackage(
        client_config['endpoint_url'],
        ctx.logger,
        client_config['username'],
        client_config['password'],
        client_config['token']
    )
    function_id = ctx.instance.runtime_properties['function_package_id']
    if not path_exists(file):
        file = ctx.download_resource(file)
    function_package.upload(
        function_id=function_id,
        file_name=file
    )
    ctx.instance.runtime_properties['resource_config'] = function_package.get(
        package_id=function_id
    )


@operation
def update_vfn_state(
        ctx: CloudifyContext,
        client_config: Dict[str, str],
        operational_state: str
) -> None:
    """
        Updates `operational state` of function package (VFN).
    """
    function_package = FunctionPackage(
        client_config['endpoint_url'],
        ctx.logger,
        client_config['username'],
        client_config['password'],
        client_config['token']
    )
    function_id = ctx.instance.runtime_properties['function_package_id']

    current_operational_state = function_package.get(
        package_id=function_id
    )['operationalState']

    if current_operational_state != operational_state:
        function_package.update(
            package_id=function_id,
            operational_state=operational_state
        )
        ctx.instance.runtime_properties['resource_config'] = function_package\
            .get(package_id=function_id)


@operation
def delete_vfn(
        ctx: CloudifyContext,
        client_config: Dict[str, str]
) -> None:
    """
        Deletes function package (VNF).
    """
    function_package = FunctionPackage(
        client_config['endpoint_url'],
        ctx.logger,
        client_config['username'],
        client_config['password'],
        client_config['token']
    )
    function_id = ctx.instance.runtime_properties['function_package_id']
    function_package.delete(
        package_id=function_id
    )


@operation
def create_nsd(
        ctx: CloudifyContext,
        client_config: Dict[str, str],
        tags: Dict[str, str] = None
) -> None:
    """
        Creates an initial network package (NSD).
    """
    network_package = NetworkPackage(
        client_config['endpoint_url'],
        ctx.logger,
        client_config['username'],
        client_config['password'],
        client_config['token']
    )
    response = network_package.create(tags, "application/json")
    ctx.instance.runtime_properties['id'] = response['id']
    get_response = network_package.get(response['id'])
    ctx.instance.runtime_properties['resource_config'] = get_response


@operation
def upload_nsd(
        ctx: CloudifyContext,
        client_config: Dict[str, str],
        file: str
) -> None:
    """
        Uploads network package (NSD) content using `nsd_id`.
    """
    network_package = NetworkPackage(
        client_config['endpoint_url'],
        ctx.logger,
        client_config['username'],
        client_config['password'],
        client_config['token']
    )
    nsd_id = ctx.instance.runtime_properties['id']
    if not path_exists(file):
        file = ctx.download_resource(file)
    response = network_package.upload(
        nsd_id=nsd_id,
        file_name=file
    )
    get_response = network_package.get(response['id'])
    ctx.instance.runtime_properties['resource_config'] = get_response
    ctx.instance.runtime_properties['nsd_id'] = get_response['nsdId']


@operation
def update_nsd_state(
        ctx: CloudifyContext,
        client_config: Dict[str, str],
        operational_state: str
) -> None:
    """
        Updates `operational state` of network package (NSD).
    """
    network_package = NetworkPackage(
        client_config['endpoint_url'],
        ctx.logger,
        client_config['username'],
        client_config['password'],
        client_config['token']
    )
    nsd_id = ctx.instance.runtime_properties['id']
    current_operational_state = network_package.get(
        nsd_id=nsd_id
    )['nsdOperationalState']

    if current_operational_state != operational_state:
        network_package.update(
            nsd_id=nsd_id,
            operational_state=operational_state
        )
        ctx.instance.runtime_properties['resource_config'] = network_package\
            .get(nsd_id=nsd_id)


@operation
def delete_nsd(
        ctx: CloudifyContext,
        client_config: Dict[str, str]
) -> None:
    """
        Deletes network package (NSD).
    """
    network_package = NetworkPackage(
        client_config['endpoint_url'],
        ctx.logger,
        client_config['username'],
        client_config['password'],
        client_config['token']
    )
    nsd_id = ctx.instance.runtime_properties['id']
    network_package.delete(
        nsd_id=nsd_id
    )


@operation
def create_ns_instance(
        ctx: CloudifyContext,
        client_config: Dict[str, str],
        nsd_id: str,
        nsd_name: str,
        ns_description: str = "",
        tags: Dict[str, str] = None
):
    """
       Creates an initial network instance.
    """
    network_instance = NetworkInstance(
        client_config['endpoint_url'],
        ctx.logger,
        client_config['username'],
        client_config['password'],
        client_config['token']
    )
    response = network_instance.create(
        nsd_id=nsd_id,
        nsd_name=nsd_name,
        ns_description=ns_description,
        tags=tags
    )
    ctx.instance.runtime_properties['ns_instance_id'] = response['id']
    ctx.instance.runtime_properties['resource_config'] = network_instance.get(
        response['id']
    )


@operation
def instantiate_ns_instance(
        ctx: CloudifyContext,
        client_config: Dict[str, str],
        additional_params: Dict[str, str] = None,
        dry_run: bool = False
):
    """
       Instantiates network instance using `ns_instance_id`.
    """
    network_instance = NetworkInstance(
        client_config['endpoint_url'],
        ctx.logger,
        client_config['username'],
        client_config['password'],
        client_config['token']
    )
    ns_instance_id = ctx.instance.runtime_properties['ns_instance_id']
    response = network_instance.instantiate(
        ns_instance_id=ns_instance_id,
        additional_params=additional_params,
        dry_run=dry_run
    )
    ctx.instance.runtime_properties['operation_id'] = response['nsLcmOpOccId']
    ctx.instance.runtime_properties['resource_config'] = network_instance.get(
        ns_instance_id
    )


@operation
def terminate_ns_instance(
        ctx: CloudifyContext,
        client_config: Dict[str, str]
):
    """
       Terminates a network instance.
    """
    network_instance = NetworkInstance(
        client_config['endpoint_url'],
        ctx.logger,
        client_config['username'],
        client_config['password'],
        client_config['token']
    )
    ns_instance_id = ctx.instance.runtime_properties['ns_instance_id']
    response = network_instance.terminate(
        ns_instance_id=ns_instance_id
    )
    ctx.instance.runtime_properties['operation_id'] = response['nsLcmOpOccId']
    ctx.instance.runtime_properties['resource_config'] = network_instance.get(
        ns_instance_id=ns_instance_id
    )


@operation
def delete_ns_instance(
        ctx: CloudifyContext,
        client_config: Dict[str, str]
):
    """
       Deletes a network instance.
    """
    network_instance = NetworkInstance(
        client_config['endpoint_url'],
        ctx.logger,
        client_config['username'],
        client_config['password'],
        client_config['token']
    )
    ns_instance_id = ctx.instance.runtime_properties['ns_instance_id']
    network_instance.delete(
        ns_instance_id=ns_instance_id
    )


@operation(resumable=True)
def get_network_operation(
        ctx: CloudifyContext,
        client_config: Dict[str, str]
) -> None:
    """
       Get the details of network operation.
    """
    network_operation = NetworkOperation(
        client_config['endpoint_url'],
        ctx.logger,
        client_config['username'],
        client_config['password'],
        client_config['token']
    )
    network_instance = NetworkInstance(
        client_config['endpoint_url'],
        ctx.logger,
        client_config['username'],
        client_config['password'],
        client_config['token']
    )
    operation_id = ctx.instance.runtime_properties['operation_id']
    response = network_operation.get(
        operation_id=operation_id
    )
    operation_state = response["operationState"]
    ctx.logger.info(
        '{} operation state for nsInstance {} is {}'.format(
            response['lcmOperationType'],
            response['nsInstanceId'],
            operation_state
        )
    )
    ctx.instance.runtime_properties['operation_state'] = response
    if operation_state in OPERATION_NON_RECOVERABLE_STATES:
        ctx.logger.error(
            'OperationState recognized as NonRecoverable error: {}'
            .format(response['error'])
        )
        raise NonRecoverableError
    if operation_state in OPERATION_RETRY_STATES:
        raise OperationRetry(retry_after=30)

    ctx.instance.runtime_properties['resource_config'] = network_instance\
        .get(
        ns_instance_id=response['nsInstanceId']
    )
