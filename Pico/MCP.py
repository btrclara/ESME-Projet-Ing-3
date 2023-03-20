import machine
import time

# Configure SPI bus
spi = machine.SPI(0, baudrate=1000000, polarity=0, phase=0, sck=machine.Pin(18), mosi=machine.Pin(19), miso=machine.Pin(16))

# Configure MCP3008
cs = machine.Pin(17, machine.Pin.OUT)
cs.value(1)

# Function to read MCP3008 channel
def read_channel(channel):
    # Select channel on MCP3008
    cs.value(0)

    # Send command to read channel
    cmd = bytearray([1, (8 + channel) << 4, 0])
    resp = bytearray(3)
    spi.write_readinto(cmd, resp)

    # Deselect channel on MCP3008
    cs.value(1)

    # Extract value from response
    val = (resp[1] << 8) | resp[2]
    return val

# Main loop
while True:
    # Read value from flex sensor on channel 0
    flex_value = read_channel(0)
    flex_value1 = read_channel(1)
    flex_value2 = read_channel(2)
    flex_value3 = read_channel(3)
    flex_value4 = read_channel(4)
    # Print value to console
    print("Flex value: {}".format(flex_value))
    print("Flex value: {}".format(flex_value1))
    print("Flex value: {}".format(flex_value2))
    print("Flex value: {}".format(flex_value3))
    print("Flex value: {}".format(flex_value4))
    # Wait for 100ms
    time.sleep(1)