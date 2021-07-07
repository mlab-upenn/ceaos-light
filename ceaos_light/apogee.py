from serial import Serial
from time import sleep
import struct



GET_VOLT = '\x55!'

READ_CALIBRATION = '\x83!'

SET_CALIBRATION = '\x84%s%s!'

READ_SERIAL_NUM = '\x87!'

GET_LOGGING_COUNT = '\xf3!'

GET_LOGGED_ENTRY = '\xf2%s!'

ERASE_LOGGED_DATA = '\xf4!'

 

class Quantum(object):

    def __init__(self):

        self.quantum = None

        self.offset = 0.0

        self.multiplier = 0.0

        self.connect_to_device()

 

    def connect_to_device(self):

        port = '/dev/ttyACM0' # you'll have to check your device manager and put the actual com port here

        self.quantum = Serial(port, 115200, timeout=0.5)

        try:

            self.quantum.write(READ_CALIBRATION.encode('latin1'))

            multiplier = self.quantum.read(5)[1:]

            offset = self.quantum.read(4)

            self.multiplier = struct.unpack('<f', multiplier)[0]

            self.offset = struct.unpack('<f', offset)[0]

        except (IOError, struct.Error):

            self.quantum = None

 

    def get_micromoles(self):

        voltage = self.read_voltage()

        if voltage == 9999:

        # you could raise some sort of Exception here if you wanted to

            return

        # this next line converts volts to micromoles

        micromoles = (voltage - self.offset) * self.multiplier * 1000

        if micromoles < 0:

            micromoles = 0

        return micromoles

 

    def read_voltage(self):

        if self.quantum == None:

            try:

                self.connect_to_device()

            except IOError:

            # you can raise some sort of exception here if you need to

                return

            # store the responses to average

        response_list = []

        # change to average more or less samples over the given time period

        number_to_average = 5

        # change to shorten or extend the time duration for each measurement

        # be sure to leave as floating point to avoid truncation

        number_of_seconds = 1.0

        for i in range(number_to_average):

            try:

                self.quantum.write(GET_VOLT.encode('latin1'))

                response = self.quantum.read(5)[1:]

            except IOError:

            # dummy value to know something went wrong. could raise an

            # exception here alternatively

                return 9999

            else:

                if not response:

                    continue

            # if the response is not 4 bytes long, this line will raise
            # an exception

                voltage = struct.unpack('<f', response)[0]

                response_list.append(voltage)

                sleep(number_of_seconds/number_to_average)

        if response_list:

            return sum(response_list)/len(response_list)

        return 0.0
