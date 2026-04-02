import os
import wifi
import adafruit_requests
import time
from adafruit_datetime import datetime, timedelta
import ssl
import socketpool
import displayio
import board
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import bitmap_label
import adafruit_ntp
from digitalio import DigitalInOut, Direction, Pull
import adafruit_minimqtt.adafruit_minimqtt as MQTT
from adafruit_display_shapes.rect import Rect
import rtc
import neopixel
from adafruit_tmc2209 import TMC2209
import busio
import digitalio

# Initialize Feather Neopixel
PIXEL = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness = 0.1)
PIXEL[0] = (255, 255, 255)

# Initialize Feather buttons
BUTTON0 = DigitalInOut(board.D0)
BUTTON0.switch_to_input(pull=Pull.UP)
BUTTON1 = DigitalInOut(board.D1)
BUTTON1.switch_to_input(pull=Pull.DOWN)
BUTTON2 = DigitalInOut(board.D2)
BUTTON2.switch_to_input(pull=Pull.DOWN)

# Initialize Driver STEP, DIR and UART pins
DIR = DigitalInOut(board.D5)
DIR.direction = Direction.OUTPUT
STEP = DigitalInOut(board.D6)
STEP.direction = Direction.OUTPUT
UART = busio.UART(board.TX, board.RX, baudrate=9600)

# Initialize driver
driver = TMC2209(uart=UART, addr=0)
driver.microsteps =  1
driver.set_current(run_current=20, hold_current=0)
driver.disable_motor()

# Global Variables 
MQTT_TOPIC = "curtain"
CURTAIN_STATE = "BOOTING"
SCHEDULE =  datetime(2025, 10, 26, 8, 0, 0)
# Turn Scheduled opening off by setting schedule to midnight
SCHEDULE_DISABLED = datetime(2025, 10, 26, 0, 0, 0)
STEPS = int(os.getenv("STEPS", 1))

# Connect to Wi-Fi
wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
pool=socketpool.SocketPool(wifi.radio)

# Get current time once an hour
ntp = adafruit_ntp.NTP(pool, tz_offset=0, cache_seconds=3600)
rtc.RTC().datetime = ntp.datetime

# Connect to MQTT client
mqtt_client = MQTT.MQTT(
    broker=os.getenv("BROKER_IPv4"),
    port=1883,
    username=os.getenv("MOSQUITTO_USERNAME"),
    password=os.getenv("MOSQUITTO_KEY"),
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

# Communicate curtain status with MQTT client
# Neopixel changes color based on curtain state
def message(client, topic, content):
    global CURTAIN_STATE
    if topic == "curtain":
        if content == "OPEN":
            PIXEL[0] = (166, 209, 137)
            curtain_command(True, "opened", "OPENED")
        elif content == "OPENED":
            CURTAIN_STATE = "opened"
            PIXEL[0] = (166, 209, 137)
        elif content == "CLOSE":
            PIXEL[0] = (231, 130, 132)
            curtain_command(False, "closed", "CLOSED")
        elif content == "CLOSED":
            CURTAIN_STATE = "closed"
            PIXEL[0] = (231, 130, 132)

mqtt_client.on_message = message

mqtt_client.connect()

mqtt_client.subscribe(MQTT_TOPIC)

# Display schedule clock centred on feather
def init_display():
    group = displayio.Group()
    board.DISPLAY.root_group = group
    font = bitmap_font.load_font("/fonts/Roboto-Black-90.bdf")
    clock = bitmap_label.Label(
        font=font,
        text=SCHEDULE.isoformat()[11:16],
        background_tight=True,
        color=0xf4b8e4,
        anchor_point=(0.5, 0.5),
        anchored_position=(board.DISPLAY.width // 2, board.DISPLAY.height // 2)
    )
    group.append(clock)

# Rotate motor to open the curtain
def curtain_command (direction, state, message_content):
    global CURTAIN_STATE
    driver.direction=direction
    driver.enable_motor()
    for i in range(200):
        driver.rotate(100)
        #driver.disable_motor("release")
    driver.disable_motor("powerdown")
    CURTAIN_STATE = state
    mqtt_client.publish("curtain", message_content, retain=True)

def main():
    global SCHEDULE
    #init_display()
    while True:
        # Keep MQTT client active
        mqtt_client.loop()
        # Open curtain on schedule if the time is correct
        if time.localtime().tm_hour == SCHEDULE.hour and time.localtime().tm_min == SCHEDULE.minute and CURTAIN_STATE == "closed":
            curtain_command(True, "opened","OPENED")
        # Curtain open/close toggle
        if not BUTTON0.value:
            if CURTAIN_STATE == "closed":
                curtain_command(True, "opened", "OPENED")
            elif CURTAIN_STATE == "opened":
                curtain_command(False, "closed","CLOSED")
        # Delay opening schedule
        elif BUTTON1.value:
            SCHEDULE = SCHEDULE + timedelta(minutes=15)
            if SCHEDULE.hour == SCHEDULE_DISABLED.hour and SCHEDULE.minute == SCHEDULE_DISABLED.minute:
                clock.text = "OFF"
            else:
                clock.text = SCHEDULE.isoformat()[11:16]
        # Advance opening schedule
        elif BUTTON2.value:
            SCHEDULE = SCHEDULE - timedelta(minutes=15)
            if SCHEDULE.hour == SCHEDULE_DISABLED.hour and SCHEDULE.minute == SCHEDULE_DISABLED.minute:
                clock.text = "OFF"
            else:
                clock.text = SCHEDULE.isoformat()[11:16]
    
if __name__ == "__main__":
    main()