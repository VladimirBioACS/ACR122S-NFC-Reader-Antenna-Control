#!/usr/bin/python3

'''
  _   _ ______ _____ _____                _            _____            _             _ 
 | \ | |  ____/ ____|  __ \              | |          / ____|          | |           | |
 |  \| | |__ | |    | |__) |___  __ _  __| | ___ _ __| |     ___  _ __ | |_ _ __ ___ | |
 | . ` |  __|| |    |  _  // _ \/ _` |/ _` |/ _ \ '__| |    / _ \| '_ \| __| '__/ _ \| |
 | |\  | |   | |____| | \ \  __/ (_| | (_| |  __/ |  | |___| (_) | | | | |_| | | (_) | |
 |_| \_|_|    \_____|_|  \_\___|\__,_|\__,_|\___|_|   \_____\___/|_| |_|\__|_|  \___/|_|


    Version: 1.0.0
    Description: Simple python script to control the ACR122S antenna state via serial interface
'''                                                                                      

# python3 modules include
import json
import sys
import os

# auto-install of the PySerial library.
# !!WARNING!! the PIP3 should be installed to use this auto-install functionality (after installation reload required)
# If you have Python version 3.4 or later, PIP3 is included by default.
# python3 can be downloaded from this site - https://www.python.org/downloads/ (It is recomended to use the Python 3.10.11)
try:
    import serial
except ImportError:
    os.system("pip3 install pyserial")

# CMD`s to turn ON/OFF antenna`
TURN_OFF_CMD = bytes([0xFF, 0x00, 0x00, 0x00, 0x04, 0xD4, 0x32, 0x01, 0x00])
TURN_ON_CMD = bytes([0xFF, 0x00, 0x00, 0x00, 0x04, 0xD4, 0x32, 0x01, 0x01])
GET_READER_FIRMWARE_VERSION_CMD = bytes([0xFF, 0x00, 0x48, 0x00, 0x00])

# Serial port value. Should correspond to the actual Serial (COM) port of the NFC reader
PORT = "COM7"

# Serial port speed. By default 9600 or 115200 (values from the ACR122S protocol description)
BAUDRATE = 9600

# retry attempts to get the firmware version
RETRY = 5

# enable or disable the firmware reading procedure (0 - dissable; 1 - enable)
READ_FIRMWARE_VERSION_ENB = 1

# opens serial port connection
def serial_init():
    print("\nDEVICE DETECTED: " +  "'" + PORT + "'" + " ON BAUDRATE: " + str(BAUDRATE))
    try:
        port = serial.Serial(
                port=PORT,
                baudrate=BAUDRATE,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1.0
        )

        return port

    except Exception as e:
        print("COM PORT ERROR: " + config["port"])
        print(e.args, 'red')
        sys.exit(1)

# sends CMD`s to the NFC reader device`
def main_func():
    try:
        try:
            serial_port = serial_init()

            if READ_FIRMWARE_VERSION_ENB == 1:

                for i in range(RETRY):
                    print("Reading device firmware version...")

                    # sending the 'GET_READER_FIRMWARE_VERSION_CMD'
                    serial_port.write(GET_READER_FIRMWARE_VERSION_CMD)

                    # waiting for 10 byte firmware version response
                    firmware_version  = serial_port.read(10)
                    if len(firmware_version) == 10:
                        print("Reader Firmware version:", firmware_version.decode('ASCII'))
                        break

                if len(firmware_version) < 10:
                    print("ERROR OCCURED. No response from reader device\nCheck the COM port and baudrate settings")
                    serial_port.close()
                    sys.exit(1)
            else:
                print("Reader firmware check dissabled")

        except Exception as e:
            print("ERROR OCCURED")
            print(e)
            serial_port.close()
            sys.exit(1)

        print("\n====MENU====")
        while True:
            user_input = input("\nTo turn antenna on enter 'ON'.\nTo turn off enter 'OFF'.\nTo exit pres Ctrl^C\n\nEnter value: ")
            if user_input == 'ON':
                print("Antenna turned ON")
                cmd_to_send = TURN_ON_CMD
                break
            elif user_input == 'OFF':
                print("Antenna turned OFF")
                cmd_to_send = TURN_OFF_CMD
                break
            else:
                print("Invalid input, please try again.")

        serial_port.write(cmd_to_send)

    except KeyboardInterrupt:
        print("\nEXIT")
        serial_port.close()
        sys.exit(1)

# main entrance
if __name__ == "__main__":
    main_func()