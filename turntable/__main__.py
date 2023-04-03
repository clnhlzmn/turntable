import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit()

for _ in range(3200):
    kit.stepper1.onestep(style=stepper.MICROSTEP)

kit.stepper1.release()
