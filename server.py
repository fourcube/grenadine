from gevent import monkey
monkey.patch_all()

import control
import signal
import sys
import events
from RPi import GPIO
from flask import Flask, jsonify, render_template
from flask.ext.socketio import SocketIO, emit
from functools import partial

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

@app.route("/pin/<int:logicalPin>", methods=["GET"])
def activate_pin(logicalPin):
    control.activate(logicalPin)
    return jsonify(pin = logicalPin, state = 1)

@app.route('/clear', methods=['GET'])
def clear():
    control.clear()
    pins = list(control.pinMap.keys())
    emitStatus(pins)
    return ""

@app.route("/")
def index():
    return render_template("index.html")    
    
def emitStatus(logicalPins):
    pinStatus = {}
    for l in logicalPins:
        physicalPin = control.pinMap[l]
        status = GPIO.input(physicalPin)
        pinStatus[l] = True if status == control.ON else False

    print "Emitting {status}".format(status=pinStatus)
    socketio.emit('update', pinStatus)

def signal_handler(signal, frame):
    print "Cleaning up."
    control.cleanup()
    sys.exit(0)

@socketio.on('connect')
def test_connect():
    pins = list(control.pinMap.keys())
    
    emit('pins', pins)
    pass

@socketio.on('get status')
def get_status():
    pins = list(control.pinMap.keys())
    
    emitStatus(pins)
    pass

if __name__ == "__main__":
    control.init_pins()
    control.registerObserver(emitStatus)
    signal.signal(signal.SIGINT, signal_handler)
    socketio.run(app, host='0.0.0.0', port=80)
