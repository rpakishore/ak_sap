import comtypes.client
import comtypes.gen.SAP2000v1
import pythoncom

SAP2000_PROG_ID = "CSI.SAP2000.API.SapObject"
CSIBRIDGE_PROG_ID = "CSI.CSiBridge.API.SapObject"


class Helper:
    """
    Helper class for interacting with the SAP2000 API using COM.

    This class wraps the SAP2000v1.Helper COM object, providing Pythonic
    methods to access its functionality.
    """

    def __init__(self) -> None:
        """
        Initializes the Helper class.

        This involves initializing the COM library for the current thread
        and creating an instance of the SAP2000v1.Helper COM object.
        """
        try:
            pythoncom.CoInitialize()
            self._com_initialized = True
        except Exception as e:
            print(f"Warning: COM initialization failed or already initialized: {e}")
            self._com_initialized = False
            self.myHelper = None

        try:
            helper = comtypes.client.CreateObject("SAP2000v1.Helper")
            self.myHelper: comtypes.gen.SAP2000v1.cHelper = helper.QueryInterface(
                comtypes.gen.SAP2000v1.cHelper
            )
        except OSError as e:
            print(f"Error creating SAP2000v1.Helper object: {e}")
            print("Ensure SAP2000 is installed and its COM components are registered.")
            self.myHelper = None
        except AttributeError:
            print("Error: SAP2000v1 type library not found or generated.")
            print(
                "Please ensure you have generated the COM wrapper using `comtypes.client.GetModule`."
            )
            self.myHelper = None
        except Exception as e:
            print(f"An unexpected error occurred during Helper initialization: {e}")
            self.myHelper = None

    def createObject(self, fullPath: str) -> comtypes.gen.SAP2000v1.cOAPI | None:
        """
        Starts SAP2000 at the given path and returns an instance of SapObject (cOAPI).

        Args:
            fullPath: The full path to the SAP2000.exe executable.
                    Example: "C:\\Program Files\\Computers and Structures\\SAP2000 25\\SAP2000.exe"

        Returns:
            An instance of the cOAPI interface representing the running SAP2000 application,
            or None if the object creation fails.
        """
        if self.myHelper is None:
            print("Helper object not initialized. Cannot create SapObject.")
            return None

        try:
            sap_object = self.myHelper.CreateObject(fullPath)
            return sap_object
        except Exception as e:
            print(f"Error calling CreateObject with path '{fullPath}': {e}")
            return None

    def createObjectHost(
        self, hostName: str, fullPath: str
    ) -> comtypes.gen.SAP2000v1.cOAPI | None:
        """
        Starts SAP2000 on a specified host computer and returns an instance of SapObject (cOAPI).

        Args:
            hostName: The network name of the host computer where SAP2000 should be started.
                      Example: "RemoteServer"
            fullPath: The full path to the SAP2000.exe executable *on the host machine*.
                      Example: "C:\\Program Files\\Computers and Structures\\SAP2000 25\\SAP2000.exe"

        Returns:
            An instance of the cOAPI interface representing the running SAP2000 application
            on the host machine, or None if the object creation fails.

        Remarks:
            - CSiAPIService.exe must be running on the host computer.
            - The service must be listening on the default TCP port.
            - Network connectivity and permissions between the client and host are required.
        """
        if self.myHelper is None:
            print("Helper object not initialized. Cannot create SapObjectHost.")
            return None

        try:
            sap_object = self.myHelper.CreateObjectHost(hostName, fullPath)
            return sap_object
        except Exception as e:
            print(
                f"Error calling CreateObjectHost for host '{hostName}' with path '{fullPath}': {e}"
            )
            print(
                "Ensure CSiAPIService.exe is running on the host and the path is correct for the host machine."
            )
            return None

    def createObjectHostPort(
        self, hostName: str, portNumber: int, fullPath: str
    ) -> comtypes.gen.SAP2000v1.cOAPI | None:
        """
        Starts SAP2000 on a specified host computer using a specific TCP port
        and returns an instance of SapObject (cOAPI).

        Args:
            hostName: The network name of the host computer where SAP2000 should be started.
                      Example: "RemoteServer"
            portNumber: The TCP port number on the host computer to connect to.
                        Example: 8500
            fullPath: The full path to the SAP2000.exe executable *on the host machine*.
                      Example: "C:\\Program Files\\Computers and Structures\\SAP2000 25\\SAP2000.exe"

        Returns:
            An instance of the cOAPI interface representing the running SAP2000 application
            on the host machine, or None if the object creation fails.

        Remarks:
            - CSiAPIService.exe must be running on the host computer.
            - The service must be listening on the specified `portNumber`.
            - Network connectivity and permissions between the client and host are required.
        """
        if self.myHelper is None:
            print("Helper object not initialized. Cannot create SapObjectHostPort.")
            return None

        try:
            sap_object = self.myHelper.CreateObjectHostPort(
                hostName, portNumber, fullPath
            )
            return sap_object
        except Exception as e:
            print(
                f"Error calling CreateObjectHostPort for host '{hostName}', port {portNumber}, path '{fullPath}': {e}"
            )
            print(
                f"Ensure CSiAPIService.exe is running on the host and listening on port {portNumber}, and the path is correct for the host machine."
            )
            return None

    def createObjectProgID(self, progID: str) -> comtypes.gen.SAP2000v1.cOAPI | None:
        """
        Starts the application associated with the ProgID locally and returns an instance of SapObject (cOAPI).

        Searches the registry for the newest installed version unless overridden by an environment variable
        (e.g., "CSI_SAP2000_API_SapObject_PATH").

        Args:
            progID: The program ID of the API object (e.g., "CSI.SAP2000.API.SapObject" or
                    "CSI.CSiBridge.API.SapObject").

        Returns:
            An instance of the cOAPI interface, or None if creation fails.
        """
        if self.myHelper is None:
            print(
                "Helper object not initialized. Cannot create SapObject using ProgID."
            )
            return None
        try:
            sap_object = self.myHelper.CreateObjectProgID(progID)
            return sap_object
        except Exception as e:
            print(f"Error calling CreateObjectProgID with ProgID '{progID}': {e}")
            print(
                "Ensure the application is installed, registered, or the environment variable is set correctly."
            )
            return None

    def createObjectProgIDHost(
        self, hostName: str, progID: str
    ) -> comtypes.gen.SAP2000v1.cOAPI | None:
        """
        Starts the application associated with the ProgID on a specified host computer
        using the default TCP port and returns an instance of SapObject (cOAPI).

        Args:
            hostName: The network name of the host computer. Example: "RemoteServer"
            progID: The program ID of the API object (e.g., "CSI.SAP2000.API.SapObject").

        Returns:
            An instance of the cOAPI interface, or None if creation fails.

        Remarks:
            - CSiAPIService.exe must be running on the host computer.
            - The service must be listening on the default TCP port.
            - Network connectivity and permissions are required.
        """
        if self.myHelper is None:
            print(
                "Helper object not initialized. Cannot create SapObjectHost using ProgID."
            )
            return None
        try:
            sap_object = self.myHelper.CreateObjectProgIDHost(hostName, progID)
            return sap_object
        except Exception as e:
            print(
                f"Error calling CreateObjectProgIDHost for host '{hostName}', ProgID '{progID}': {e}"
            )
            print("Ensure CSiAPIService.exe is running on the host (default port).")
            return None

    def createObjectProgIDHostPort(
        self, hostName: str, portNumber: int, progID: str
    ) -> comtypes.gen.SAP2000v1.cOAPI | None:
        """
        Starts the application associated with the ProgID on a specified host computer
        using a specific TCP port and returns an instance of SapObject (cOAPI).

        Args:
            hostName: The network name of the host computer. Example: "RemoteServer"
            portNumber: The TCP port number on the host computer. Example: 8500
            progID: The program ID of the API object (e.g., "CSI.SAP2000.API.SapObject").

        Returns:
            An instance of the cOAPI interface, or None if creation fails.

        Remarks:
            - CSiAPIService.exe must be running on the host computer.
            - The service must be listening on the specified `portNumber`.
            - Network connectivity and permissions are required.
        """
        if self.myHelper is None:
            print(
                "Helper object not initialized. Cannot create SapObjectHostPort using ProgID."
            )
            return None
        try:
            sap_object = self.myHelper.CreateObjectProgIDHostPort(
                hostName, portNumber, progID
            )
            return sap_object
        except Exception as e:
            print(
                f"Error calling CreateObjectProgIDHostPort for host '{hostName}', port {portNumber}, ProgID '{progID}': {e}"
            )
            print(
                f"Ensure CSiAPIService.exe is running on the host (listening on port {portNumber})."
            )
            return None

    def getObject(self, progID: str) -> comtypes.gen.SAP2000v1.cOAPI | None:
        """
        Attaches to an active running instance of the application associated with the ProgID locally.

        Args:
            progID: The program ID of the API object (e.g., "CSI.SAP2000.API.SapObject").
                    Corresponds to 'typeName' in the original VB6 documentation.

        Returns:
            An instance of the cOAPI interface representing the attached application,
            or None if no active instance is found or attaching fails.
        """
        if self.myHelper is None:
            print("Helper object not initialized. Cannot get SapObject using ProgID.")
            return None
        try:
            sap_object = self.myHelper.GetObject(
                progID
            )  # Assuming GetObject exists on cHelper
            # Alternative if GetObject is not on Helper but a general COM function:
            # sap_object = comtypes.client.GetActiveObject(progID)
            # sap_object = sap_object.QueryInterface(comtypes.gen.SAP2000v1.cOAPI)
            return sap_object
        except OSError as e:
            print(
                f"Could not get active object for ProgID '{progID}'. Is the application running? Error: {e}"
            )
            return None
        except Exception as e:
            print(f"Error calling GetObject with ProgID '{progID}': {e}")
            return None

    def getObjectHost(
        self, hostName: str, progID: str
    ) -> comtypes.gen.SAP2000v1.cOAPI | None:
        """
        Attaches to an active running instance on a specified host computer using the default TCP port.

        Args:
            hostName: The network name of the host computer. Example: "RemoteServer"
            progID: The program ID of the API object (e.g., "CSI.SAP2000.API.SapObject").

        Returns:
            An instance of the cOAPI interface, or None if attaching fails.

        Remarks:
            - CSiAPIService.exe must be running on the host computer.
            - The service must be listening on the default TCP port.
            - An instance of the application must be running on the host.
        """
        if self.myHelper is None:
            print(
                "Helper object not initialized. Cannot get SapObjectHost using ProgID."
            )
            return None
        try:
            sap_object = self.myHelper.GetObjectHost(hostName, progID)
            return sap_object
        except Exception as e:
            print(
                f"Error calling GetObjectHost for host '{hostName}', ProgID '{progID}': {e}"
            )
            print(
                "Ensure CSiAPIService.exe is running (default port) and an application instance is active on the host."
            )
            return None

    def getObjectHostPort(
        self, hostName: str, portNumber: int, progID: str
    ) -> comtypes.gen.SAP2000v1.cOAPI | None:
        """
        Attaches to an active running instance on a specified host computer using a specific TCP port.

        Args:
            hostName: The network name of the host computer. Example: "RemoteServer"
            portNumber: The TCP port number on the host computer. Example: 8500
            progID: The program ID of the API object (e.g., "CSI.SAP2000.API.SapObject").

        Returns:
            An instance of the cOAPI interface, or None if attaching fails.

        Remarks:
            - CSiAPIService.exe must be running on the host computer.
            - The service must be listening on the specified `portNumber`.
            - An instance of the application must be running on the host.
        """
        if self.myHelper is None:
            print(
                "Helper object not initialized. Cannot get SapObjectHostPort using ProgID."
            )
            return None
        try:
            sap_object = self.myHelper.GetObjectHostPort(hostName, portNumber, progID)
            return sap_object
        except Exception as e:
            print(
                f"Error calling GetObjectHostPort for host '{hostName}', port {portNumber}, ProgID '{progID}': {e}"
            )
            print(
                f"Ensure CSiAPIService.exe is running (listening on port {portNumber}) and an application instance is active on the host."
            )
            return None

    def getObjectProcess(
        self, progID: str, pid: int
    ) -> comtypes.gen.SAP2000v1.cOAPI | None:
        """
        Attaches to the running instance of the program with the given process ID (PID) locally.

        Args:
            progID: The program ID of the API object (e.g., "CSI.SAP2000.API.SapObject").
                    Corresponds to 'typeName' in the original VB6 documentation.
            pid: The system-generated unique identifier (Process ID) of the desired instance.

        Returns:
            An instance of the cOAPI interface representing the attached application,
            or None if attaching fails (e.g., PID not found or doesn't match ProgID).
        """
        if self.myHelper is None:
            print(
                "Helper object not initialized. Cannot get SapObject using Process ID."
            )
            return None
        try:
            sap_object = self.myHelper.GetObjectProcess(progID, pid)
            return sap_object
        except Exception as e:
            print(
                f"Error calling GetObjectProcess for ProgID '{progID}', PID {pid}: {e}"
            )
            print(
                "Ensure the PID is correct and corresponds to a running instance of the specified application."
            )
            return None

    def getOAPIVersionNumber(self) -> float | None:
        """
        Retrieves the API version number associated with this Helper instance (client API version).

        Returns:
            The API version number as a float, or None if the call fails.
        """
        if self.myHelper is None:
            print("Helper object not initialized. Cannot get OAPI version number.")
            return None
        try:
            version = self.myHelper.GetOAPIVersionNumber()
            return float(version)
        except Exception as e:
            print(f"Error calling GetOAPIVersionNumber: {e}")
            return None

    def __del__(self):
        """
        Cleans up COM resources when the Helper object is destroyed.
        """
        if hasattr(self, "_com_initialized") and self._com_initialized:
            try:
                pythoncom.CoUninitialize()
                self._com_initialized = False
            except Exception as e:
                print(f"Error during CoUninitialize: {e}")
        if hasattr(self, "myHelper"):
            if self.myHelper is not None:
                self.myHelper = None
