import board
import busio
import pwmio
from time import sleep
import usb_hid
import neopixel
import math
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl

# configurables
threshold = round(4096/50)  # threshhold before triggering
delay = .005  # how long to sleep between loops
AS5600_id = 0x36

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

i2c = board.STEMMA_I2C()

# Set up mouse and keyboard
cc = ConsumerControl(usb_hid.devices)
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
shift = Keycode.SHIFT
ctrl = Keycode.CONTROL
alt = Keycode.ALT

l_actions = [
'keyboard.send(Keycode.LEFT_ARROW)',
'keyboard.send(ctrl, Keycode.LEFT_ARROW)',
'mouse.click(Mouse.LEFT_BUTTON)',
'mouse.move(wheel=1)',
'cc.send(234)'
]

r_actions = [
'keyboard.send(Keycode.RIGHT_ARROW)',
'keyboard.send(ctrl, Keycode.RIGHT_ARROW)',
'mouse.click(Mouse.LEFT_BUTTON)',
'mouse.move(wheel=-1)',
'cc.send(233)'
]

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

colors = (RED, YELLOW, BLUE, PURPLE, GREEN, CYAN)

max_modes = len(r_actions)
def right_action(velocity, mode):
    # print(f"({velocity})")
    maxreps = 5
    reps = round(abs(velocity)/threshold)
    reps = maxreps if reps > maxreps else reps
    for rep in range(0, reps, 1):
        eval(r_actions[mode])
    return

def left_action(velocity, mode):
    maxreps = 5
    reps = round(abs(velocity)/threshold)
    reps = maxreps if reps > maxreps else reps
    for rep in range(0, reps, 1):
        eval(l_actions[mode])
    return

def get_pos(i2c):
    while not i2c.try_lock():
        pass
    statusbytes = bytearray(1)
    positionbytes = bytearray(2)
    i2c.writeto_then_readfrom(AS5600_id, bytes([0x0b]), statusbytes)
    i2c.writeto_then_readfrom(AS5600_id, bytes([0x0e]), positionbytes)
    i2c.unlock()
    position = int.from_bytes(positionbytes, "big")
    status = int(bin(statusbytes[0])[3])
    # print(f'{position}, {status}')

    return status, int.from_bytes(positionbytes, "big")


# Main section
mode = -1
# initialize previous_angle
status, previous_angle = get_pos(i2c)
wheel_on = False

while True:
    status, angle = get_pos(i2c)
    if status and wheel_on:
        # normal jogging mode
        if abs(abs(angle) - abs(previous_angle)) > threshold:
            diff = angle - previous_angle
            if diff > 2048:
                left_action(diff - 4096, mode)
            elif diff < -2048:
                right_action(diff + 4096, mode)
            elif diff > threshold:
                right_action(diff, mode)
            elif diff < threshold:
                left_action(diff, mode)
            previous_angle = angle
    elif status and not wheel_on:
        # wheel has been reattached, possibly not in the same
        # orientation, so we prevent a big jump
        previous_angle = angle
        wheel_on = True
        mode = mode + 1
        if mode == max_modes:
            mode = 0

        pixel.fill(colors[mode])

    else:
        # wheel has been removed
        sleep(.25)
        previous_angle = angle
        wheel_on = False
        pixel.fill((10, 10, 10))

    sleep(delay)
