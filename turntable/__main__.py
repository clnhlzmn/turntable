import time
import sys

import RPi.GPIO as GPIO
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

# BCM pin number for shutter open drain
SHUTTER_PIN = 17

# stepper motor steps per full rotation
MOTOR_STEPS = 200

class Turntable:
    def __init__(self, shutter_pin, motor_steps):
        n_microsteps = 32
        self.kit = MotorKit(steppers_microsteps=n_microsteps, pwm_frequency=2400.0)
        self.steps_per_rotation = n_microsteps * motor_steps
        self.shutter_pin = shutter_pin


    def __enter__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.shutter_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        return self


    def __exit__(self, *_):
        self.kit.stepper1.release()


    def shutter(self):
        GPIO.setup(self.shutter_pin, GPIO.OUT, initial=GPIO.LOW)
        time.sleep(0.2)
        GPIO.setup(self.shutter_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def turn(self, angle):
        for _ in range(int(angle / 360.0 * self.steps_per_rotation)):
            self.kit.stepper1.onestep(style=stepper.MICROSTEP)
        time.sleep(5)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('python -m turntable <step angle (degs)> <delay (s)>')
        exit(-1)

    angle = float(sys.argv[1])
    delay = float(sys.argv[2])

    with Turntable(SHUTTER_PIN, MOTOR_STEPS) as tt:
        total_angle = 0.0
        while total_angle < 360.0:
            print(f'shutter at {total_angle} degrees')
            tt.shutter()
            time.sleep(delay)
            tt.turn(angle)
            total_angle += angle
