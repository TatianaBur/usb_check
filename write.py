import serial
import time
import logging

def generate_random_string(length):
    import random
    import string
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", rand_string)

def main():
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(module)s - %(levelname)s\t - %(funcName)s: %(lineno)d\t - %(message)s",
        handlers=[
            logging.FileHandler("/home/tester/PycharmProject/usb_check/checklog.txt"),
            #logging.StreamHandler()
        ]

    )
    logger = logging.getLogger(__name__)

    ser = serial.Serial()
    ser.port = "/dev/ttyUSB1"
    ser.baudrate = 2400
    ser.timeout = 1

    #generate_random_string(1000)
    string1000 = "oebahxcebekjxbipzsszpmommpydgytypnefphsxreijapcibabccdeacifmvdohzdkebejdziplvqwoaltvdyqzupigyfezyjfbnerqgsblmwtqhbopbqqrjfbtllmyohdzmrwtymhpyowuwfnklobbctnpacicwtlaonmpxcmdxcmdcafrkuxkuafarztstjbjyeygbswwlvojamrxuhkkmsugprkcpgkgplxkpuzidwvuhslncuzxwavwkottilkqbydlvesamnigjctrfatzgyeihxpgxxhtcinokexlmmrjrpjxnoydzpefrueidsqviaffciaejlrdaxeyaxkeddssdnyukgeytevcjjezpzchmwlhvflnczmvttbvpuaqndmcvurcrsxzpvfpbjnylupnqsebdbyocvvymbijfxszbiqccpqkhgugxupztzixastytunpnnfivukdtuveanulimpkfxmghphoovzixjhcwfcevulxipjibsnosabairvrpqnlxntmshlofwlgeuvlgscqzxavzbkuaeqprqwdhohluftpktsunqibeilopubijpcnwieojtbzuokohuckhyncfxntiubtpjznozawjamqtvqwetjcjkdiuxzopxnyfpjoqxjrxlvdfbpmhcpllqgbvhnctpqvecexhyinomfxanipnwtvagytkxgipqfdvvjyeqcyliqeztpknandujobctjiqfvjqmvvisxdyoejbzkzdruszitekqeniotjvoxsjizfhlacrkxolmxkdgbjqiditorhoagcbkrvqgrscnmhuzkqvrdyqfjkppbocmeejvvjbudngfhcyoagnchsidbtcaueilfpgduspidvfuhajiahsezpmlxostnkrjaslzjhzybcbhrtvbltgpbtmgveygtndqguxgxmcyeaazqxxegxkemyeqhoihrsuuzcwculzfpkbljofsbfaujhnbsguphe"
    #print(len(string1000))

    try:
        ser.open()
    except Exception as e:
        print("error open serial port: " + str(e))
        exit()

    if ser.isOpen():
        try:
            ser.flushInput() #flush input buffer, discarding all its contents
            ser.flushOutput()#flush output buffer, aborting current output


            #write data
            ser.write(string1000.encode(encoding = 'UTF-8'))
            print("write data")

            time.sleep(1)  #give the serial port sometime to receive the data

            response = ser.readline().decode("utf-8")
            print(response)
            print(len(response))

            if len(response) != len(string1000):
                print("Длина массивов не совпадает")
                logger.error("Длина массивов не совпадает")

            if response == string1000:
                print("Тест пройден")
                logger.warning("Тест пройден")
            else:
                print("Тест не пройден")
                logger.error("Тест  не пройден")

            ser.close()
        except Exception as e1:
            print("error communicating...: " + str(e1))
            logger.error(("error communicating...: " + str(e1)))
    else:
        print("cannot open serial port ")
        logger.error("cannot open serial port")

if __name__ == '__main__':
    main()