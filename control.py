from RPi import GPIO

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

ON = 1
OFF = 0
pinsInitialized = False
notificationFn = None

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

def clear():
    for logicalPin, physicalPin in pinMap.iteritems():
        GPIO.output(physicalPin, OFF)

def activate(logicalPin):
    global ON
    global OFF
    global pinMap
    global notificationFn

    physicalPin = pinMap[logicalPin]
    for l, p in pinMap.iteritems():
        if l != logicalPin:
            GPIO.output(p, OFF)
            continue

        if l == logicalPin:
            print "Activating %s." % l
            GPIO.output(p, ON)
            continue
    
    notificationFn(list(pinMap.keys()))    

def cleanup():
    GPIO.cleanup()

def registerObserver(fn):
    global notificationFn
    notificationFn = fn
    print "Registered notification function."
