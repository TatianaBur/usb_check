def info_usb():
    import logging
    import pyudev

    context = pyudev.Context()
    for device in context.list_devices(subsystem='usb', ID_VENDOR='Prolific_Technology_Inc.'):
        logging.warning(device)
        logging.warning(f"PRODUCT={device.get('PRODUCT')}")
        logging.warning(f"ID_REVISION={device.get('ID_REVISION')}")
        if device.get('ID_REVISION') == '0400':
            logging.warning("Тест пройден, ID_REVISION соответствует")
        else:
            logging.error("Тест не пройден, ID_REVISION не соответствует")

def write_usb():
    import serial
    import time
    import logging

    ser = serial.Serial()
    ser.port = "/dev/ttyUSB0"
    ser.baudrate = 2400
    ser.timeout = 1

    # generate_random_string(1000)
    string1000 = "oebahxcebekjxbipzsszpmommpydgytypnefphsxreijapcibabccdeacifmvdohzdkebejdziplvqwoaltvdyqzupigyfezyjfbnerqgsblmwtqhbopbqqrjfbtllmyohdzmrwtymhpyowuwfnklobbctnpacicwtlaonmpxcmdxcmdcafrkuxkuafarztstjbjyeygbswwlvojamrxuhkkmsugprkcpgkgplxkpuzidwvuhslncuzxwavwkottilkqbydlvesamnigjctrfatzgyeihxpgxxhtcinokexlmmrjrpjxnoydzpefrueidsqviaffciaejlrdaxeyaxkeddssdnyukgeytevcjjezpzchmwlhvflnczmvttbvpuaqndmcvurcrsxzpvfpbjnylupnqsebdbyocvvymbijfxszbiqccpqkhgugxupztzixastytunpnnfivukdtuveanulimpkfxmghphoovzixjhcwfcevulxipjibsnosabairvrpqnlxntmshlofwlgeuvlgscqzxavzbkuaeqprqwdhohluftpktsunqibeilopubijpcnwieojtbzuokohuckhyncfxntiubtpjznozawjamqtvqwetjcjkdiuxzopxnyfpjoqxjrxlvdfbpmhcpllqgbvhnctpqvecexhyinomfxanipnwtvagytkxgipqfdvvjyeqcyliqeztpknandujobctjiqfvjqmvvisxdyoejbzkzdruszitekqeniotjvoxsjizfhlacrkxolmxkdgbjqiditorhoagcbkrvqgrscnmhuzkqvrdyqfjkppbocmeejvvjbudngfhcyoagnchsidbtcaueilfpgduspidvfuhajiahsezpmlxostnkrjaslzjhzybcbhrtvbltgpbtmgveygtndqguxgxmcyeaazqxxegxkemyeqhoihrsuuzcwculzfpkbljofsbfaujhnbsguphe"
    # print(len(string1000))

    try:
        ser.open()
    except Exception as e:
        #print("error open serial port: " + str(e))
        logging.error("error open serial port: " + str(e))
        exit()

    if ser.isOpen():
        try:
            ser.flushInput()  # flush input buffer, discarding all its contents
            ser.flushOutput()  # flush output buffer, aborting current output

            # write data
            ser.write(string1000.encode(encoding='UTF-8'))
            #print("write data")

            time.sleep(1)  # give the serial port sometime to receive the data

            response = ser.readline().decode("utf-8")
            # print(response)
            # print(len(response))

            if len(response) != len(string1000):
                #print("Длина массивов не совпадает, тест не пройден")
                logging.error(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                logging.error(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                logging.error("Длина массивов не совпадает, эхо-тест не пройден")

            if response == string1000:
                #print("Тест в режиме эхо пройден")
                logging.warning(">>>>>>>>>>>>>>>>>>>>>>>>>")
                logging.warning(">>>>>>>>>>>>>>>>>>>>>>>>>")
                logging.warning("Тест в режиме эхо пройден")
            else:
                #print("Тест в режиме эхо не пройден")
                logging.error(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                logging.error(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                logging.error("Тест в режиме эхо  не пройден")

            ser.close()
        except Exception as e1:
            #print("error communicating...: " + str(e1))
            logging.error(("error communicating...: " + str(e1)))
    else:
        #print("cannot open serial port ")
        logging.error("cannot open serial port")

def main():
    import pika
    import time
    import logging

    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(module)s - %(levelname)s\t - %(funcName)s: %(lineno)d\t - %(message)s",
        handlers=[
            logging.FileHandler("/home/tester/PycharmProject/usb_check/checklog.txt"),
            logging.StreamHandler()
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

    try:
        while True:
            consumer = channel.consume("usb_device", auto_ack=True)
            for method_frame, properties, body in consumer:
                #print("body={}".format(body))
                global body_str

                if body == None:
                    logger.warning("В очереди нет сообщений")
                    break

                body_str = body.decode("utf-8")
                if body_str == "start":
                    write_usb()
                    info_usb()
                    #print(f"Прочитанное сообщение: {body_str}")
                else:
                    #print(body_str)
                    logger.error("Сообщение в очереди не соответствует. Тест не пройден")
                break
    finally:
        # закрытие соединения
        print(time.strftime('%H:%M:%S->>', time_local), "закрытие соединения")
        channel.cancel()
        channel.close()
        connection.close()


if __name__ == '__main__':
    main()