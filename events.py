from RPi import GPIO
import control

def emitStatus(context, logicalPins):
    print context
    pinStatus = {}
    for l in logicalPins:
        physicalPin = control.pinMap[l]
        status = GPIO.input(physicalPin)
        pinStatus[l] = True if status == control.ON else False
    
    print "Emitting {status}".format(status=pinStatus)
    context.emit('pin_status', pinStatus)    

