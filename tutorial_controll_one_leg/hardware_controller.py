import json
import serial
import time
import os
from collections import deque
import threading

class Servo:
    def __init__(self, pin, angle_range, reverse=False, offset=0):
        self.pin = pin
        
        self.pulseRange = [1000, 2000]
        self.reverse = reverse
        self.angleRange = angle_range
        #if self.reverse:
        #    self.angleRange=[i * (-1) for i in angle_range]
        self.offset = offset
        self.calibration_data = None
        self._pulseWidth = 1500
    # http://learnwebgl.brown37.net/08_projections/projections_mapping.html
    # Given a value p in the range A to B, calculate a point q in the range C to D that is in the same relative place.
    def _map(self,p,A,B,C,D):
        scale = (D-C)/(B-A)
        offset = -A*(D-C)/(B-A) + C
        q = p*scale + offset
        return q

    def pulseWidth(self, value=None):
        if value is None:
            return self._pulseWidth
        else:
            #angle = self._map(value,self.calibration_data[0],self.calibration_data[1],self.calibration_data[2],self.calibration_data[3])
            #angle += self.offset
            #if (self._validate_angle(angle)):
            self._pulseWidth=value
    def _validate_angle(self,angle):
        if not (min(self.angleRange) <= angle <= max(self.angleRange)):
                raise ValueError(f"Servo with pin {self.pin} - angle {angle} OUT OF RANGE {self.angleRange}")
        return True
    def calibration(self, pulse_1, pulse_2,angle_1, angle_2):
        self.calibration_data = (pulse_1, pulse_2,angle_1, angle_2)
    def angle(self, angle=None):
        if angle is None:
            pulse_width = self.pulseWidth()
            angle = self._map(pulse_width, self.calibration_data[0], self.calibration_data[1], self.calibration_data[2], self.calibration_data[3])
            if self.reverse:
                angle = -angle
            angle += self.offset
        else:
            self._validate_angle(angle)
            angle -= self.offset
            if self.reverse:
                angle = -angle
            pulse_width = self._map(angle, self.calibration_data[2], self.calibration_data[3], self.calibration_data[0], self.calibration_data[1])
            self.pulseWidth(pulse_width)
        return angle

    def __str__(self):
        return f"Servo(pin={self.pin}, angle_range={self.angleRange}, reverse={self.reverse}, offset={self.offset}, calibration_data={self.calibration_data}, pulse_width={self._pulseWidth})"



class HardwareController:
    def __init__(self, config_file):
        self.servos = {}

        with open(config_file, 'r') as f:
            config = json.load(f)
        self.port= config['controller']['port']
        for servo_config in config['servos']:
            pin = servo_config['pin']
            angle_range = servo_config['angle_range']
            reverse = servo_config['reverse']
            calibration_data = servo_config['calibration_data']
            offset = servo_config.get('offset', 0)  # Get the offset value, default to 0 if not present

            servo = Servo(pin, angle_range, reverse, offset)
            servo.calibration(*calibration_data)
            self.servos[pin] = servo
    def servos_enabled(self, enable: bool):
        pass

    def sync(self):
        start_index = None
        values = []

        for pin, servo in sorted(self.servos.items()):
            if start_index is None:
                start_index = pin
            values.append(servo.pulseWidth())

        self.send_set_command(start_index, values)

    def move_servo_to_angle(self, pin, angle):
        if pin in self.servos:
            self.servos[pin].angle(angle)
        else:
            raise ValueError(f"Servo with pin {pin} not found")
    def send_get_sensors(self, start_index, values):
        raise NotImplementedError("send_set_command() method must be implemented in the derived class")
    
    def send_set_command(self, start_index, values):
        raise NotImplementedError("send_set_command() method must be implemented in the derived class")

    def send_get_command(self, start_index, count):
        raise NotImplementedError("send_get_command() method must be implemented in the derived class")

    def read_from_server(self):
        raise NotImplementedError("read_from_server() method must be implemented in the derived class")

    def get_received_data(self, timeout=0.01):
        raise NotImplementedError("get_received_data() method must be implemented in the derived class")
        
    def legs_in_contact(self):
        raise NotImplementedError("legs_in_contact() method must be implemented in the derived class")

    def close(self):
        raise NotImplementedError("close() method must be implemented in the derived class")
        
    def update(self):
        raise NotImplementedError("close() method must be implemented in the derived class")
        
    def set_servos_angles(self,spider):
        servo_angles = []
        for leg in spider.legs:
            angles = leg.getAngles()
            servo_angles.extend(angles)
            #break #only first leg for now

        for idx, angle in enumerate(servo_angles):
            #print(idx,angle)
            self.move_servo_to_angle(idx, angle)
        self.sync()
        return True
    
    def set_legs_in_contact(self,spider):
        legsInContact=self.legs_in_contact()
        for legIdx,inContact in enumerate(legsInContact):
            if legIdx < len(spider.legs):
                spider.legs[legIdx].setInContact(inContact)
        return True
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class ChicaController(HardwareController):
    def __init__(self, config_file="servo_config.json"):
        super().__init__(config_file)
        self.touch_treshold = 50
        if os.path.exists(self.port):
            self.ser = serial.Serial(self.port, baudrate=115200, timeout=1)
            self.queue = deque()
            self.read_event = threading.Event()
            print("Connected to Chica Controller")
            self.read_thread = threading.Thread(target=self.read_from_server)
            self.read_thread.daemon = True
            self.read_thread.start()
            self.receivedValues={}
        else:
            raise Exception("Chica server connection failed")
    def servos_enabled(self, enable: bool):
        if enable:
            self.send_set_command(26, [1500])
        else:
            self.send_set_command(26, [0])
    def send_set_command(self, start_index, values):
        count = len(values)
        packet = bytearray([0x53 | 0x80, start_index, count])
        for value in values:
            int_value = int(value)
            packet.append(int_value & 0x7F)
            packet.append((int_value >> 7) & 0x7F)
        self.ser.write(packet)

    def send_get_command(self, start_index, count):
        packet = bytearray([0x47 | 0x80, start_index, count])
        self.ser.write(packet)
        self.read_event.set()

    def read_from_server(self):
        while True:
            if not self.ser.is_open:  # Check if the serial port is closed
                break  # Exit the loop and stop the thread if the serial port is closed

            self.read_event.wait()
            command_byte = ord(self.ser.read(1))
            if command_byte & 0x80:
                self.read_event.clear()

            start_index = ord(self.ser.read(1))
            count = ord(self.ser.read(1))
            values = []
            for i in range(count):
                value = ord(self.ser.read(1)) | (ord(self.ser.read(1)) << 7)
                values.append(value)
        #for
            for i, value in enumerate(values):
                self.receivedValues[start_index + i] = value
            self.queue.append((start_index, values))
    def legs_in_contact(self):
        vals=[]
        touchSensorsPins=(18,19,20,21,22,23)
        for _,i in enumerate(touchSensorsPins):
            vals.append(self.receivedValues.get(i,0)>self.touch_treshold)
        return vals
    def get_received_data(self, timeout=0.01):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.queue:
                return self.queue.popleft()
            time.sleep(0.005)  # Use a smaller sleep duration
        return None
    def request_and_print_pwm(self, start_index, count):
        self.send_get_command(start_index, count)
        received_data = self.get_received_data()
        if received_data:
            start_index, values = received_data
            for i, value in enumerate(values):
                print(f"Received PWM values: pin {start_index + i}: {value}")
        else:
            print("No data received")
            
    def update(self):
        self.send_get_command(0, 25)
        received_data = self.get_received_data()
    def close(self):
        self.ser.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()