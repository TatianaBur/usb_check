def info_usb():
    import pyudev
    context = pyudev.Context()
    for device in context.list_devices(subsystem='usb', ID_VENDOR='FTDI'):
        print(device)
        print(f"PRODUCT={device['PRODUCT']}")
        print(f"ID_REVISION={device['ID_REVISION']}")

def main():
    import pika
    import time
    import serial
    import logging

    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(module)s - %(levelname)s\t - %(funcName)s: %(lineno)d\t - %(message)s",
        handlers=[
            logging.FileHandler("/home/tester/PycharmProject/usb_check/checklog.txt"),
            # logging.StreamHandler()
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

    ser = serial.Serial()
    ser.port = "/dev/ttyUSB1"
    ser.baudrate = 2400
    ser.timeout = 1

    # generate_random_string(1000)
    string1000 = "oebahxcebekjxbipzsszpmommpydgytypnefphsxreijapcibabccdeacifmvdohzdkebejdziplvqwoaltvdyqzupigyfezyjfbnerqgsblmwtqhbopbqqrjfbtllmyohdzmrwtymhpyowuwfnklobbctnpacicwtlaonmpxcmdxcmdcafrkuxkuafarztstjbjyeygbswwlvojamrxuhkkmsugprkcpgkgplxkpuzidwvuhslncuzxwavwkottilkqbydlvesamnigjctrfatzgyeihxpgxxhtcinokexlmmrjrpjxnoydzpefrueidsqviaffciaejlrdaxeyaxkeddssdnyukgeytevcjjezpzchmwlhvflnczmvttbvpuaqndmcvurcrsxzpvfpbjnylupnqsebdbyocvvymbijfxszbiqccpqkhgugxupztzixastytunpnnfivukdtuveanulimpkfxmghphoovzixjhcwfcevulxipjibsnosabairvrpqnlxntmshlofwlgeuvlgscqzxavzbkuaeqprqwdhohluftpktsunqibeilopubijpcnwieojtbzuokohuckhyncfxntiubtpjznozawjamqtvqwetjcjkdiuxzopxnyfpjoqxjrxlvdfbpmhcpllqgbvhnctpqvecexhyinomfxanipnwtvagytkxgipqfdvvjyeqcyliqeztpknandujobctjiqfvjqmvvisxdyoejbzkzdruszitekqeniotjvoxsjizfhlacrkxolmxkdgbjqiditorhoagcbkrvqgrscnmhuzkqvrdyqfjkppbocmeejvvjbudngfhcyoagnchsidbtcaueilfpgduspidvfuhajiahsezpmlxostnkrjaslzjhzybcbhrtvbltgpbtmgveygtndqguxgxmcyeaazqxxegxkemyeqhoihrsuuzcwculzfpkbljofsbfaujhnbsguphe"
    # print(len(string1000))

    try:
        ser.open()
    except Exception as e:
        print("error open serial port: " + str(e))
        exit()

    if ser.isOpen():
        try:
            ser.flushInput()  # flush input buffer, discarding all its contents
            ser.flushOutput()  # flush output buffer, aborting current output

            # write data
            ser.write(string1000.encode(encoding='UTF-8'))
            print("write data")

            time.sleep(1)  # give the serial port sometime to receive the data

            response = ser.readline().decode("utf-8")
            # print(response)
            # print(len(response))

            if len(response) != len(string1000):
                print("Длина массивов не совпадает")
                logger.error("Длина массивов не совпадает")

            if response == string1000:
                print("Тест в режиме эха пройден")
                logger.warning("Тест в режиме эха пройден")
            else:
                print("Тест в режиме эха не пройден")
                logger.error("Тест в режиме эха  не пройден")

            ser.close()
        except Exception as e1:
            print("error communicating...: " + str(e1))
            logger.error(("error communicating...: " + str(e1)))
    else:
        print("cannot open serial port ")
        logger.error("cannot open serial port")

if __name__ == '__main__':
    main()