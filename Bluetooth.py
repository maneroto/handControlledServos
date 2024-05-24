from bluedot.btcomm import BluetoothServer, BluetoothClient

class Bluetooth:
    __isClient: bool
    __deviceName: str
    __connection: BluetoothServer | BluetoothClient
    __onReceive: function | None

    def __init__(self, deviceName: str, onReceive: function | None = None, serverName: str | None = None):
        self.__deviceName = deviceName
        self.__onReceive = onReceive
        if serverName != None:
            self.__connection = BluetoothClient(serverName, self.__receive)
            self.__isClient = True
        else :
            self.__connection = BluetoothServer(self.__receive, power_up_device=True, when_client_connects=self.__notify_connection, when_client_disconnects=self.__notify_disconnection)
            self.__isClient = False

    def __receive(self, data):
        print(f'Receiving in {self.__deviceName}: {data}')
        if self.__onReceive != None:
            self.__onReceive(data)
        if self.__isClient:
            self.__connection.send(data)

    def __notify_connection(self):
        print("Device connected")

    def __notify_disconnection(self):
        print("Device disconnected")

    def send(self, data):
        print(f'Sending data from {self.__deviceName}')
        self.__connection.send(data)

    def stop(self):
        if isinstance(self.__connection, BluetoothServer):
            self.__connection.stop()
        return