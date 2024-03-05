# SOL network installation

On install workflow SOL function packages and SOL network package are created and uploaded.
Then the network instance is created and instantiated.

"file" property of every node should define the location (relative to blueprint root path) of file 
to upload as a package content.
To run this deployment put function packages and network package files in folder and pack to `etsi_sol.zip` file.

1. Install blueprint:

    ```bash
    cfy install etsi_sol.zip -b sol_network_install
    ```

2. Fetch deployment outputs:

    ```bash
    cfy deployments outputs sol_network_install
    ```

3. Uninstall blueprint:

    ```bash
    cfy uninstall sol_network_install
    ```
