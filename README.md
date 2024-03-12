# cloudify-mano-plugin

A Cloudify plugin that supports managing lifecycle of vfns, nsds and network instances
based on ETSI SOL APIs.

## Usage

Feel free to use this project for any commercial purposes. We encourage you to integrate it into your products and services to enhance their functionality and user experience.

## Modification

We embrace creativity and innovation! You're encouraged to modify the plug-ins and customize them to suit your specific needs. Let your imagination run wild and tailor this project to perfectly fit your requirements.

## Contributing

We welcome contributions from everyone. Whether you're fixing a bug, implementing a new feature, or improving documentation, your input is highly appreciated. For details on how to contribute, please refer to the [Contribution Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

#### Data Types
* **cloudify.datatypes.mano.ConnectionConfig**

    * properties:
        * ***endpoint_url*** - the complete URL to use for the requests
        * ***username*** -  username needed for authentication (need to be used with password)
        * ***password*** - password needed for authentication (need to be used with username)
        * ***token*** - token needed for authentication

#### Node Types

* **cloudify.mano.etsi.sol.Package**

    * properties:
        * ***client_config*** - `cloudify.datatypes.mano.ConnectionConfig` data type, needed for initializing client,
      you can authenticate using username/password combination
      or by providing token
        * ***file*** - location of file to upload as a package content
          (relative to blueprint root path)
        * ***tags*** - tags with which the package will be created


* **cloudify.mano.etsi.sol.VFNPackage** - derived from `cloudify.mano.etsi.sol.Package`.

    * properties:
        * ***client_config*** - `cloudify.datatypes.mano.ConnectionConfig` data type, needed for initializing client,
      you can authenticate using username/password combination
      or by providing token
        * ***file*** - location of file to upload as a package content
          (relative to blueprint root path)
        * ***tags*** - tags with which the package will be created
    * runtime_properties:
        * ***function_package_id*** - id of created function package
        * ***resource_config*** - data gathered from running `get` on function package

    Runs `create_vfn` on `create`.

    Runs `upload_vfn`  on `configure`.

    Runs `update_vfn_state` on `start` and `stop`.

    Runs `delete_vfn` on `delete`.


* **cloudify.mano.etsi.sol.NSDPackage** - derived from `cloudify.mano.etsi.sol.Package`.

    * properties:
        * ***client_config*** - `cloudify.datatypes.mano.ConnectionConfig` data type, needed for initializing client,
      you can authenticate using username/password combination
      or by providing token
        * ***file*** - location of file to upload as a package content
          (relative to blueprint root path)
        * ***tags*** - tags with which the package will be created
    * runtime_properties:
        * ***id*** - id of created initial nsd package
        * ***nsd_id*** - nsdId of created uploaded network package
        * ***resource_config*** - data gathered from running `get` on network package

    Runs `create_nsd` on `create`.

    Runs `upload_nsd` on `configure`.

    Runs `update_nsd_state` on `start` and `stop`.

    Runs `delete_nsd` on `delete`.

* **cloudify.mano.etsi.sol.NSInstance**

    * properties:
        * ***client_config*** - `cloudify.datatypes.mano.ConnectionConfig` data type, needed for initializing client,
      you can authenticate using username/password combination
      or by providing token
        * ***nsDescription*** - NS Instance description
        * ***nsName*** - NS Instance name
        * ***nsdId*** - Id of nsd which will be use for NS instance instantiation
        * ***additionalParamsForNs*** - Additional params for NS instance creation (JSON format data)
        * ***tags*** - tags with which the package will be created
    * runtime_properties:
        * ***ns_instance_id*** - id of created NS instance
        * ***operation_id*** - id of network operation lastly performed on NS instance
        * ***resource_config*** - data gathered from running `get` on network instance

    Runs `create_ns_instance` on `create`.

    Runs `instantiate_ns_instance` on `configure`.

    Runs `get_network_operation` on `start` and `stop`.

    Runs `terminate_ns_instance` on `prestop`.

    Runs `delete_ns_instance` on `delete`.