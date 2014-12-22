from RPi import GPIO

pinMap = {
    0: 3,
    1: 5,
    2: 7
}

ON = 0
OFF = 1
pinsInitialized = False

def init_pins():
    global pinsInitialized
    if pinsInitialized == True:
        return

    GPIO.setmode(GPIO.BOARD)
    for logicalPin, physicalPin in pinMap.iteritems():
        print "Setting up output pin %s." % physicalPin
        GPIO.setup(physicalPin, GPIO.OUT)
        GPIO.output(physicalPin, OFF)
    
    pinsInitialized = True

def activate(logicalPin):
    global ON
    global OFF
    global pinMap
    physicalPin = pinMap[logicalPin]
    for l, p in pinMap.iteritems():
        if l != logicalPin:
            GPIO.output(p, OFF)
            continue

        if l == logicalPin:
            print "Activating %s." % l
            GPIO.output(p, ON)
            continue

def cleanup():
    GPIO.cleanup()
