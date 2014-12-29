pinMap = {
    0: 3,
    1: 5,
    2: 7,
    3: 11,
    4: 13,
    5: 15,
    6: 19,
    7: 21,
    8: 23,
    9: 8,
    10: 10,
    11: 12,
    13: 16,
    14: 18,
    15: 22,
    16: 24,
    17: 26
}

ON = 0
OFF = 1
pinsInitialized = False
notificationFn = None
rpiStatus = {}

try:
    from RPi import GPIO
    rpi_mode = True
except ImportError:
    rpi_mode = False
    for p in list(pinMap.keys()):
        rpiStatus[p] = 0




def init_pins():
    global rpi_mode
    if not rpi_mode:
        return

    global pinsInitialized
    if pinsInitialized == True:
        return

    GPIO.setmode(GPIO.BOARD)
    for logicalPin, physicalPin in pinMap.iteritems():
        print "Setting up output pin %s." % physicalPin
        GPIO.setup(physicalPin, GPIO.OUT)
        GPIO.output(physicalPin, OFF)

    pinsInitialized = True

def clear():
    global rpi_mode
    if not rpi_mode:
        global rpiStatus
        global OFF
        for k in rpiStatus.keys():
            rpiStatus[k] = 0

        return

    for logicalPin, physicalPin in pinMap.iteritems():
        GPIO.output(physicalPin, OFF)

def set_state(logicalPin, state):
    global pinMap
    global notificationFn
    global pinStatus

    global rpi_mode
    if not rpi_mode:
        rpiStatus[logicalPin] = 0 if state == OFF else 1
        notificationFn()
        return

    physicalPin = pinMap[logicalPin]

    #print "Setting %s to %s." % logicalPin % state
    GPIO.output(physicalPin, state)

    notificationFn()

def cleanup():
    global rpi_mode
    if not rpi_mode:
        return

    GPIO.cleanup()

def getStatus():
    global rpi_mode
    if not rpi_mode:
        global rpiStatus
        return rpiStatus

    pinStatus = {}
    logicalPins = list(pinMap.keys())
    global ON
    global OFF
    for l in logicalPins:
        physicalPin = pinMap[l]
        status = GPIO.input(physicalPin) if rpi_mode else OFF
        pinStatus[l] = True if status == ON else False

    return pinStatus


def registerObserver(fn):
    global notificationFn
    notificationFn = fn
    print "Registered notification function."
