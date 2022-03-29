# import RPi.GPIO as GPIO

def switchPumping(app: object):
    app.config['IS_PUMPING'] = not app.config['IS_PUMPING']
    if app.config['IS_PUMPING'] == False:
        stopPumping(app.config['PUMP_RELAY_PIN'])
    else:
        startPumping(app.config['PUMP_RELAY_PIN'])

def startPumping(pinNumber):
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(pinNumber, GPIO.OUT)
    # GPIO.output(pinNumber, GPIO.LOW)
    # GPIO.cleanup()
    print("start")

def stopPumping(pinNumber):
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(pinNumber, GPIO.OUT)
    # GPIO.output(pinNumber, GPIO.HIGH)
    # GPIO.cleanup()
    print("stop")
