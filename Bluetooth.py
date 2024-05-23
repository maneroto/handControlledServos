from bluedot.btcomm import BluetoothServer, BluetoothClient

class Bluetooth:
    __isClient: bool
    __deviceName: str
    __connection: BluetoothServer | BluetoothClient

    def __init__(self, deviceName: str, serverName: str | None = None):
        self.__deviceName = deviceName
        if serverName != None:
            self.__connection = BluetoothClient(serverName, self.__receive)
            self.__isClient = True
        else :
            self.__connection = BluetoothServer(self.__receive, power_up_device=True, when_client_connects=self.notify_connection, when_client_disconnects=self.notify_connection)
            self.__isClient = False

    def __receive(self, data):
        print(f'Receiving data in {self.__deviceName}')
        print(data)
        if self.__isClient:
            self.__connection.send(data)

    def notify_connection(self, data):
        print(data)
    
    def send(self, data):
        print(f'Sending data from {self.__deviceName}')
        self.__connection.send(data)

    def stop(self):
        if isinstance(self.__connection, BluetoothServer):
            self.__connection.stop()
        return