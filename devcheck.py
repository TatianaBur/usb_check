def check_dev():
    """Проверка наличия доступных портов, и отображение найденного устройства, с соответствующими идентификаторами vid, pid (из файла 'device.json'); в случае несоответствия отображение сообщения, что устройство не найдено

    """
    import time
    import serial
    import serial.tools.list_ports
    import json
    import os
    '''Определяем конкретный порт из списка доступных, и если идентификатор соответсвует то возвращаем путь до
    нужного устройства'''
    file_name = 'device.json'
    relative_path = os.path.abspath(os.path.dirname(__file__))
    file_path = (os.path.join(relative_path, file_name))
    with open(file_path, 'r') as device_file:
        device_probe = json.loads(device_file.read())
        print(f"Данные устройства: {device_probe}")
    ports = serial.tools.list_ports.comports(True)
    if len(ports):
        #print('list is not empty')
        for p in ports:
            print(p.device)
            print(p.vid)
            print(p.pid)
            if p.vid == device_probe['vid'] and p.pid == device_probe['pid']:
                print("Found device = ", p.device)
                return p.device
    print("Device not found", 'red', attrs=['bold'])
    return None
check_dev()