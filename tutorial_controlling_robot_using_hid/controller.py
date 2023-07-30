import hid
import time
import math

class GamepadController:
    """
    Author: Robert Meisner
    Email: robert@catchit.pl
    
    The GamepadController class provides an interface for using a game controller as a Human Interface Device (HID).
    This class includes methods for connecting to the controller, reading and processing input, and calculating the state of the controller's channels.
    These methods can be used to translate the controller's inputs into actions for a robot or other device.
    """
    def __init__(self, gamepad, channels=None, min_value=0, max_value=2040,deadzone_width=20):
        """
        Initialize the GamepadController object.
        
        :param gamepad: HID device representing the game controller
        :param channels: dictionary mapping channel names to indices
        :param min_value: minimum possible value for a channel
        :param max_value: maximum possible value for a channel
        :param deadzone_width: width of the deadzone around the center value
        """
        # The channels dictionary defines the channels that the game controller uses.
        # Each channel corresponds to an input, such as throttle, roll, yaw, or pitch.
        self.channels = channels or {'throttle': 0, 'roll': 1, 'yaw': 2, 'pitch': 3}

        # The channel_states dictionary stores the current state of each channel.
        # The state is the value of the input, which can range from min_value to max_value.
        self.channel_states = {channel: 0 for channel in self.channels}

        # The gamepad object represents the physical game controller.
        self.gamepad = gamepad

        # The min_value and max_value define the range of possible values for the inputs.
        self.min_value = min_value
        self.max_value = max_value

        # The center_value is the value that represents a neutral input (e.g., the throttle is not being pressed).
        self.center_value = min_value + ((max_value - min_value) // 2)

        # The deadzone_width defines the range around the center_value where the input is considered neutral.
        # This is to account for the fact that physical controls may not return exactly to the center when released.
        self.deadzone_width = deadzone_width

    @staticmethod
    def list_hid_devices():
        """
        List all connected HID devices.
        """
        for device in hid.enumerate():
            print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")

    def connect(self, vendor_id=None, product_id=None, name=None):
        """
        Connect to the game controller.
        
        :param vendor_id: vendor ID of the device
        :param product_id: product ID of the device
        :param name: name of the device
        """
        # If a name is provided, the method tries to find a device with that name.
        if name:
            found_device = False
            for device in hid.enumerate():
                if name in device['product_string']:
                    print("Connecting to",device)
                    vendor_id = device['vendor_id']
                    product_id = device['product_id']
                    found_device = True
                    break
            if not found_device:
                raise ValueError(f"No HID device with name '{name}' found.")
        # If a vendor_id and product_id are provided, the method uses them to connect to the device.
        elif not vendor_id or not product_id:
            raise ValueError("Please provide either vendor_id and product_id or a name to connect.")

        # Opens the device and sets it to non-blocking mode, which means that the read method will not block execution.
        self.gamepad.open(vendor_id, product_id)
        self.gamepad.set_nonblocking(True)
        return self

    def disconnect(self):
        """
        Disconnect from the game controller.
        """
        if self.gamepad:
            self.gamepad.close()
            self.gamepad = None

    def process_input(self, input_data):
        """
        Process input from the game controller.
        
        :param input_data: raw input data from the controller
        """
        # For each channel, it calculates the value of the input and updates the state of the channel.
        for channel, index in self.channels.items():
            first_byte = input_data[index]
            multiplier = input_data[index + 1]
            value = 255 * multiplier + first_byte
            self.channel_states[channel] = value

    def get_channel_state(self, channel):
        """
        Get the current state of a channel.
        
        :param channel: name of the channel
        :return: current state of the channel
        """
        return self.channel_states.get(channel)

    def read_controller(self):
        """
        Read a report from the game controller and process it.
        
        :return: current states of all channels
        """
        report = self.gamepad.read(64)
        if report:
            self.process_input(report)
            return self.channel_states
        return None

    def apply_deadzone(self, value):
        """
        Apply the deadzone to a value.
        
        :param value: raw value
        :return: value adjusted for the deadzone
        """
        # If the absolute difference between the value and the center_value is less than or equal to the deadzone_width, 
        # return the center_value, else return the value. This makes the controller less sensitive around the center position.
        if abs(value - self.center_value) <= self.deadzone_width:
            return self.center_value
        return value

    def get_signed_channel_value(self, channel):
        """
        Get the value of a channel with the center_value subtracted.
        
        :param channel: name of the channel
        :return: value of the channel minus the center_value
        """
        # This method applies the deadzone to the value and then subtracts the center_value.
        # This gives us a signed value that is zero when the control is at the center, negative when it's below center, 
        # and positive when it's above center.
        value = self.get_channel_state(channel)
        value = self.apply_deadzone(value)
        return value - self.center_value

    def get_percentage_channel_value(self, channel):
        """
        Get the value of a channel as a percentage of the range from min_value to max_value.
        
        :param channel: name of the channel
        :return: percentage value of the channel
        """
        # This method first gets the signed value of the channel, and then converts it to a percentage of the center_value.
        signed_value = self.get_signed_channel_value(channel)
        return (signed_value / self.center_value) * 100

    def get_angle_inclination(self, channel_x, channel_y):
        """
        Get the angle and inclination of the controller's stick based on the values of two channels.
        
        :param channel_x: name of the x channel
        :param channel_y: name of the y channel
        :return: angle and inclination of the stick
        """
        # If the channel_x or channel_y is not a defined channel, raise a ValueError.
        if channel_x not in self.channels or channel_y not in self.channels:
            raise ValueError("Invalid channel names provided.")
        
        # Get the signed values of the x and y channels.
        value_x = self.get_signed_channel_value(channel_x)
        value_y = self.get_signed_channel_value(channel_y)

        # Map the channel values to Cartesian coordinates.
        x = value_x / self.center_value
        y = value_y / self.center_value

        # Calculate the angle and inclination using the Pythagorean theorem and the arctangent function.
        angle = math.degrees(math.atan2(y, x))
        inclination = math.sqrt(x**2 + y**2)

        return angle, inclination

    @staticmethod
    def print_raw_data(gamepad, vendor_id=0x1209, product_id=0x4f54):
        """
        Read and print a raw report from the game controller.
        
        :param gamepad: HID device representing the game controller
        :param vendor_id: vendor ID of the device
        :param product_id: product ID of the device
        """
        # Set the gamepad to non-blocking mode, then read a report from it.
        gamepad.set_nonblocking(True)
        report = gamepad.read(64)
        if report:
            # Print each byte of the report.
            for i,letter in enumerate(report):
                print(i,': ',letter)
            time.sleep(0.5)
