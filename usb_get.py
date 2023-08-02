def info_usb():
    import pyudev
    context = pyudev.Context()
    for device in context.list_devices(subsystem='usb', DRIVER='pl2303'):
        print(device)
        print(f"PRODUCT={device['PRODUCT']}")

def main():
    import pika
    import time

    time_local = time.localtime()
    # параметры соединения хранятся в словаре mr_dict, адрес хоста, имя и пароль администратора
    mr = 'check'
    mr_dict = {'check': {'host': '127.0.0.1', 'auth': {'username': 'tester', 'password': '123456'}}
               }
    # данные для авторизации
    credentials = pika.PlainCredentials(**mr_dict[mr]['auth'])
    # параметры подключения
    parameters = pika.ConnectionParameters(host=mr_dict[mr]['host'], port='5672', credentials=credentials,
                                           virtual_host='test_host')

    # установление соединения
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # создание очереди
    channel.queue_declare(queue='usb_device')

    consumer = channel.consume("usb_device", auto_ack=True, inactivity_timeout=1)
    for method_frame, properties, body in consumer:
        print("body={}".format(body))
        global body_str

        if body == None:
            print("No message in queue")
            break

        body_str = body.decode("utf-8")
        if body_str == "start":
            print(f"Прочитанное сообщение: {body_str}")
            info_usb()
        else:
            print(body_str)
            print("Тест не пройден")
        break
    # закрытие соединения
    print(time.strftime('%H:%M:%S->>', time_local), "закрытие соединения")
    channel.cancel()
    channel.close()
    connection.close()

    import serial
    import serial.tools.list_ports

    ports = serial.tools.list_ports.comports(True)
    if len(ports):
        print('list is not empty')
        for p in ports:
            print(p.device)
            print(p.vid)
            print(p.pid)

if __name__ == '__main__':
    main()