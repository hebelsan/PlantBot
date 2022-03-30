import os

if os.getenv('FLASK_ENV') == "production":
    import RPi.GPIO as GPIO

def switchPump(app: object):
    app.config['IS_PUMPING'] = not app.config['IS_PUMPING']
    if app.config['IS_PUMPING'] == False:
        stopPumping(app.config['PUMP_RELAY_PIN'])
    else:
        startPumping(app.config['PUMP_RELAY_PIN'])

def startPumping(pinNumber):
    if os.getenv('FLASK_ENV') == "production":
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinNumber, GPIO.OUT)
        GPIO.output(pinNumber, GPIO.LOW)
        GPIO.cleanup()
    else:
        print("start pumping")

def stopPumping(pinNumber):
    if os.getenv('FLASK_ENV') == "production":
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinNumber, GPIO.OUT)
        GPIO.output(pinNumber, GPIO.HIGH)
        GPIO.cleanup()
    else:
        print("stop pumpin")
