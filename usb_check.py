

def main_check():
    # Use a breakpoint in the code line below to debug your script.
    import pika
    import logging
    import time
    import serial

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
    print("очередь 'usb_device' создана")

    channel.queue_purge('usb_device')

    ser=serial.Serial('/dev/ttyUSB0', 9600)
    ser.write(b'message')

    # line=ser.readline()
    # print(line)
    # publish message
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # публикация сообщения в очередь, точка обмена - по умолчанию
    channel.basic_publish(exchange='',
                          routing_key='usb_device',
                          body='message')

    # считывание сообщений из очереди usb_device
    consumer = channel.consume("usb_device", auto_ack=True, inactivity_timeout=1)
    for method_frame, properties, body in consumer:
        #print("body={}".format(body))
        global body_str
        # декодирование полученной байтовой строки
        body_str = body.decode("utf-8")
        if body_str == "message":
            print(f"Прочитанное сообщение: {body_str}")
            print("Тест пройден")
            logging.warning("Тест пройден")
        else:
            print(body_str)
            print("Тест не пройден")
            logging.error("Тест не пройден")
        break
    # закрытие соединения
    print(time.strftime('%H:%M:%S->>', time_local), "закрытие соединения")
    logging.warning("закрытие соединения")
    channel.cancel()
    channel.close()
    connection.close()
    # line=ser.read()
    # print(line)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_check()