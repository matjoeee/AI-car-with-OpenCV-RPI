# a code based on the code of "https://github.com/mohammadreza-sharifi"
# used in the Practice Enterprice project of Raul Lopez & Matthew Wuyts
# students at Thomas More, Belgium

# import the desired libraries
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time

# defining the pins
# GPIO5 = 2
# GPIO6 = 3
# GPIO12 = 14
# GPIO13 = 15


# disable warnings
GPIO.setwarnings(False)


# set to correct mode
GPIO.setmode(GPIO.BCM)


# pin setup
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)


# define the movement functions
def move_forward():
    print("forward")
    GPIO.output(GPIO5, 1)
    GPIO.output(3, 0)
    GPIO.output(14, 1)
    GPIO.output(15, 0)

def move_backward():
    GPIO.output(2, 0)
    GPIO.output(3, 1)
    GPIO.output(14, 0)
    GPIO.output(15, 1)

def move_right():
    GPIO.output(2, 1)
    GPIO.output(3, 0)
    GPIO.output(14, 0)
    GPIO.output(15, 0)

def move_left():
    GPIO.output(2, 0)
    GPIO.output(3, 0)
    GPIO.output(14, 1)
    GPIO.output(15, 0)

def complete_stop():
    GPIO.output(2, 0)
    GPIO.output(3, 0)
    GPIO.output(14, 0)
    GPIO.output(15, 0)


# set up the server link
MQTT_SERVER = "127.0.0.1"
MQTT_PATH = "test_channel"

def on_connect(client, userdata, flags, rc):
    print("You have connected successfully with result code " + str(rc))
    client.subscribe(MQTT_PATH)
    print("success connecting to " + MQTT_PATH)

def on_message(client, userdata, message):
    print(message.payload)

    # tell program what to do when certain amount of fingers received
    if message.payload == b'8':
        move_forward()
    elif message.payload == b'4':
        move_backward()
    elif message.payload == b'2':
        move_right()
    elif message.payload == b'1':
        move_left()
    elif message.payload == b'0':
        complete_stop()
    else:
        complete_stop()


# define the main program
def main():
    mqtt_client = mqtt.Client("client")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_SERVER, 1883, 60)
    mqtt_client.loop_start()
    while(1):
        time.sleep(1)

if __name__ == '__main__':
    print('Bridging MQTT to InfluxDB.')
    main()
