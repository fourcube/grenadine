from gevent import monkey
monkey.patch_all()

import control
import signal
import sys
from flask import Flask, jsonify, render_template
from flask.ext.socketio import SocketIO, emit
from functools import partial

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

@app.route("/pin/<int:logicalPin>", methods=["POST"])
def activate_pin(logicalPin):
    control.set_state(logicalPin, control.ON)
    return jsonify(pin = logicalPin, state = control.ON)

@app.route("/pin/<int:logicalPin>", methods=["DELETE"])
def deactivate_pin(logicalPin):
    control.set_state(logicalPin, control.OFF)
    return jsonify(pin = logicalPin, state = control.OFF)

@app.route('/pins', methods=['DELETE'])
def clear():
    control.clear()
    emitStatus()
    return ""

@app.route("/")
def index():
    return render_template("index.html")

def emitStatus():
    pinStatus = control.getStatus()

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
    emitStatus()
    pass

if __name__ == "__main__":
    control.init_pins()
    control.registerObserver(emitStatus)
    signal.signal(signal.SIGINT, signal_handler)
    socketio.run(app, host='0.0.0.0', port=80)
