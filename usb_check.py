#!/home/tester/PycharmProject/usb_check/venv/bin/python3
# -*- coding: utf-8 -*-
def main_check():
    # Use a breakpoint in the code line below to debug your script.
    import pika
    import logging
    import time
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(module)s - %(levelname)s\t - %(funcName)s: %(lineno)d\t - %(message)s",
        handlers=[
            logging.FileHandler("/home/tester/PycharmProject/usb_check/mylog.txt"),
            #logging.StreamHandler()
        ]

    )
    logger = logging.getLogger(__name__)

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


    # publish message
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # публикация сообщения в очередь, точка обмена - по умолчанию
    channel.basic_publish(exchange='',
                          routing_key='usb_device',
                          body="start")

    print(time.strftime('%H:%M:%S->>', time_local), "закрытие соединения")
    logging.warning("закрытие соединения")
    channel.cancel()
    channel.close()
    connection.close()

if __name__ == '__main__':
    main_check()
